# Build RAG with Python

## Seamlessly Integrate PDF, Text, and HTML Documents (Currently supports these only)

### Installation Steps

1. **Install Anaconda:**
   - Download and install Anaconda from the [official website](https://www.anaconda.com/products/distribution#download-section).

2. **Create and Activate Conda Environment:**
   - Create a new environment: `conda create -n ollama python=3.10`
   - Activate the environment: `conda activate ollama`

3. **Install the magic tools:**
   - **Debian/Ubuntu:** `sudo apt-get install libmagic1`
   - **Windows:** Use the `python-magic-bin` package which includes the necessary DLLs: `pip install python-magic-bin`
   - **Mac:** `brew install libmagic`

4. **Set up the environment:**
   - Note: the requirements file is for Windows; if on Mac, make sure step 3 is done correctly first.
   - Install all required packages: `pip install -r requirements.txt`

5. **Model Configuration:**
   - Ensure the models listed in `config.ini` are available. For instance, to use `nomic-embed-text`, execute: `ollama pull nomic-embed-text`
   - Update `config.ini` to specify the models you intend to use.

6. **Run ChromaDB:**
   - Start ChromaDB in a separate terminal: `chroma run --host localhost --port 8000 --path ../db`

7. **Prepare Your Documents:**
   - Upload your documents into the `SOURCE_DOCUMENTS` folder.

8. **Customization:**
   - Open `import.py` to choose your preferred chunking strategy in the `process_files_in_folder` function.
   - Modify `utilities.py` to load other document types if needed. Currently, it supports PDF, text, and HTML.

9. **Import Your Documents:**
   - Execute the import script: `python3 import.py`

10. **Generate a Response:**
    - Use the generate script with your input: `python3 generate.py <yourinput>`

### Additional Integrations (Did not implement RAG with this yet)

1. **Gradio Integration:** 
   - Added Gradio with streaming LLM. To run, execute: `python chat_gradio.py`

2. **Streamlit Integration:**
   - Added Streamlit with streaming LLM. To run, execute: `streamlit run chat_streamlit.py`

3. **Pygame Integration:**
   - Added Pygame with streaming LLM. To run, execute: `python instruct_pygame.py`