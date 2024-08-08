import os
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

from langchain.docstore.document import Document
from langchain_community.document_loaders import (UnstructuredHTMLLoader, 
TextLoader, UnstructuredMarkdownLoader, PDFMinerLoader, 
CSVLoader, UnstructuredExcelLoader, Docx2txtLoader, 
)
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# load_dotenv()
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Define the folder for storing database
SOURCE_DIRECTORY = os.path.join(ROOT_DIRECTORY, "SOURCE_DOCUMENTS")

PERSIST_DIRECTORY = os.path.join(ROOT_DIRECTORY, "DB")

# Get a list of all child directories in PERSIST_DIRECTORY
# Check if the folder exists
if not os.path.exists(PERSIST_DIRECTORY):
    # If the folder does not exist, create it
    os.makedirs(PERSIST_DIRECTORY)

DOCUMENT_MAP = {
    ".html": UnstructuredHTMLLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    # ".pdf": UnstructuredFileLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count() or 8

# DEVICE_TYPE = "cuda" if torch.cuda.is_available() else "cpu"
device_type = "cpu"

def file_log(logentry):
    file1 = open("file_ingest.log", "a")
    file1.write(logentry + "\n")
    file1.close()
    print(logentry + "\n")

def load_single_document(file_path: str) -> Document:
    # Loads a single document from a file path
    try:
        file_extension = os.path.splitext(file_path)[1]
        loader_class = DOCUMENT_MAP.get(file_extension)
        if loader_class:
            file_log(file_path + " loaded.")
            loader = loader_class(file_path)
        else:
            file_log(file_path + " document type is undefined.")
            raise ValueError("Document type is undefined")
        return loader.load()[0]
    except Exception as ex:
        file_log("%s loading error: \n%s" % (file_path, ex))
        return None

def load_document_batch(filepaths):
    logging.info("Loading document batch")
    # create a thread pool
    with ThreadPoolExecutor(len(filepaths)) as exe:
        # load files
        futures = [exe.submit(load_single_document, name) for name in filepaths]
        # collect data
        if futures is None:
            file_log(name + " failed to submit")
            return None
        else:
            data_list = [future.result() for future in futures]
            # return data and file paths
            return (data_list, filepaths)
        
def load_documents(source_dir: str) -> list[Document]:
    # Loads all documents from the source documents directory, including nested folders
    paths = []
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            print("Importing: " + file_name)
            file_extension = os.path.splitext(file_name)[1]
            source_file_path = os.path.join(root, file_name)
            if file_extension in DOCUMENT_MAP.keys():
                paths.append(source_file_path)

    # Have at least one worker and at most INGEST_THREADS workers
    n_workers = min(INGEST_THREADS, max(len(paths), 1))
    chunksize = round(len(paths) / n_workers)
    docs = []
    with ProcessPoolExecutor(n_workers) as executor:
        futures = []
        # split the load operations into chunks
        for i in range(0, len(paths), chunksize):
            # select a chunk of filenames
            filepaths = paths[i : (i + chunksize)]
            # submit the task
            try:
                future = executor.submit(load_document_batch, filepaths)
            except Exception as ex:
                file_log("executor task failed: %s" % (ex))
                future = None
            if future is not None:
                futures.append(future)
        # process all results
        for future in as_completed(futures):
            # open the file and load the data
            try:
                contents, _ = future.result()
                docs.extend(contents)
            except Exception as ex:
                file_log("Exception: %s" % (ex))

    return docs

def split_documents(documents: list[Document]) -> tuple[list[Document], list[Document]]:
    # Splits documents for correct Text Splitter
    text_docs, python_docs = [], []
    for doc in documents:
        if doc is not None:
            file_extension = os.path.splitext(doc.metadata["source"])[1]
            if file_extension == ".py":
                python_docs.append(doc)
            else:
                text_docs.append(doc)
    return text_docs, python_docs

def main():
        # Load documents and split in chunks
        logging.info(f"Loading documents from {SOURCE_DIRECTORY}")
        documents = load_documents(SOURCE_DIRECTORY)
        text_documents, python_documents = split_documents(documents)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=800, chunk_overlap=200, add_start_index=True
        )
        texts = text_splitter.split_documents(text_documents)
        texts.extend(python_splitter.split_documents(python_documents))
        logging.info(f"Loaded {len(documents)} documents from {SOURCE_DIRECTORY}")
        logging.info(f"Split into {len(texts)} chunks of text")

        """
        (1) Chooses an appropriate langchain library based on the enbedding model name.  Matching code is contained within fun_localGPT.py.
        
        (2) Provides additional arguments for instructor and BGE models to improve results, pursuant to the instructions contained on
        their respective huggingface repository, project page or github repository.
        """
        embedding_model_name = "nomic-embed-text"
        embeddings = OllamaEmbeddings(model=embedding_model_name, show_progress=True)

        logging.info(f"Loaded embeddings from {embedding_model_name}")

        db = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY,
    )   
        
if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    main()