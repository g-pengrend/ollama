import os, ollama, chromadb, time
from utilities import readtext, getconfig
from tools import chunker, chunk_text_by_sentences, chunk_text_by_words

def process_files_in_folder(folder_path, embedmodel, collection):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            text = readtext(filepath)
            # decide if you want to use chunk by sentence or by words
            chunks = chunk_text_by_words(source_text=text, words_per_chunk=1000, overlap=200)
            #chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=15, overlap=3)
            print(f"Processing {filename} with {len(chunks)} chunks")
            for index, chunk in enumerate(chunks):
                embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
                print(".", end="", flush=True)
                collection.add([filename + str(index)], [embed], documents=[chunk], metadatas={"source": filename})

collectionname="python-rag-ollama"

chroma = chromadb.HttpClient(host="localhost", port=8000)
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
  print('deleting collection')
  chroma.delete_collection("python-rag-ollama")
collection = chroma.get_or_create_collection(name="python-rag-ollama", metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
starttime = time.time()
folder_path = 'SOURCE_DOCUMENTS'
# Check if the directory exists
if not os.path.exists(folder_path):
    # Create the directory
    os.makedirs(folder_path)
    print(f"Directory '{folder_path}' created.")

process_files_in_folder(folder_path, embedmodel, collection)

# with open('sourcedocs.txt') as f:
#   lines = f.readlines()
#   for filename in lines:
#     text = readtext(filename)
#     chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
#     print(f"with {len(chunks)} chunks")
#     for index, chunk in enumerate(chunks):
#       embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
#       print(".", end="", flush=True)
#       collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))

