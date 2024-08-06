# RAG Builder with Python

## Seamlessly Integrate PDF, Text, and HTML Documents (Supports these formats only currently)

### Installation Steps

1. **Install Anaconda:**
   - Download and install Anaconda from the [Anaconda website](https://www.anaconda.com/products/distribution#download-section).

2. **Create and Activate Conda Environment:**
   - Open a new Anaconda Terminal or Command Prompt. It should look something like this, with the environment name in brackets (`your environment name`):

   Example: ![Anaconda Terminal](./assets/at.png)
   - Create a new environment: `conda create -n ollama python=3.10`
   - Activate the environment: `conda activate ollama`
   - Navigate to the correct path in your anaconda terminal before the next steps.

3. **Install the magic tools:**
   - **Debian/Ubuntu:** `sudo apt-get install libmagic1`
   - **Windows:** Use the `python-magic-bin` package which includes the necessary DLLs: `pip install python-magic-bin`
   - **Mac:** First, install Homebrew by following these steps: 
     - Open the terminal and run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
     - Then, install libmagic using `brew install libmagic`.

4. **Install Microsoft C++ Build Tools (For Windows):**
   - Download and install Microsoft C++ Build Tools from the [Build Tools website](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   - Click on modify
   ![Build Tools](./assets/mbt.png)
   - Install the necessary tools based on the image below:
   ![Build Tools 2](./assets/mbt2.png)

5. **Set up the environment:**
   - Make sure you are in the correct path and environment

   Example: ![Correct Path](./assets/path.png)
   - **Mac:** `python -m pip install -r requirements_mac.txt`
   - **Windows:** `python -m pip install -r requirements_win.txt`

6. **Model Configuration:**
   - Visit the [ollama website](https://ollama.ai/) and follow the installation instructions for your operating system.
   - Ensure the models listed in `config.ini` are available. For example, to use `nomic-embed-text`, run: `ollama pull nomic-embed-text`
   - To use the latest version of `llama2`, run: `ollama pull llama2:latest`
   - Update `config.ini` to specify the models you intend to use.

7. **Run ChromaDB:**
   - Open a separate terminal, ensure it is in the same conda environment i.e.: ollama
   - Start a ChromaDB in the separate terminal: `chroma run --host localhost --port 8000 --path ../db`

8. **Prepare Your Documents:**
   - Create a folder named `SOURCE_DOCUMENTS` if it does not exist.
   - Upload your documents into the `SOURCE_DOCUMENTS` folder.

9. **Customization:**
   - Open `import.py` to choose your preferred chunking strategy in the `process_files_in_folder` function.
   - Modify `utilities.py` to load other document types if needed. Currently, it supports PDF, text, and HTML.

10. **Import Your Documents:**
   - Ensure the NLTK library is installed and the 'punkt' resource is downloaded. If not, run: `python -c "import nltk; nltk.download('punkt')"`
   - Run the import script: `python import.py`

11. **Generate a Response:**
    - Use the generate script with your input: `python generate.py <yourinput>`

### Additional Integrations (RAG integration pending implementation)
#### This setup does not include RAG integration yet. We are working on it and will update the documentation accordingly when ready.

1. **Gradio Integration:** 
   - Added Gradio with streaming LLM. To run, execute: `python chat_gradio.py`

2. **Streamlit Integration:**
   - Added Streamlit with streaming LLM. To run, execute: `streamlit run chat_streamlit.py`

3. **Pygame Integration:**
   - Added Pygame with streaming LLM. To run, execute: `python instruct_pygame.py`

| **Aspect**              | **Gradio**                              | **Streamlit**                            | **Pygame**                              |
|-------------------------|-----------------------------------------|------------------------------------------|----------------------------------------|
| **Primary Use Case**    | Quick prototyping of machine learning models with interactive interfaces. | Building data apps with interactive UI and real-time updates. | Creating interactive games and simulations, including applications with real-time graphics. |
| **Ease of Use**         | High – simple and intuitive API, designed for ML demos and prototyping. | High – straightforward API, good for data apps and dashboards. | Moderate – more complex, requires knowledge of game development and graphics programming. |
| **UI Elements**         | Provides a range of pre-built UI components like sliders, text inputs, and image uploaders. | Offers a variety of UI elements like sliders, buttons, and graphs, with a focus on data visualization. | Customizable UI elements for game interfaces, but requires manual creation of elements. |
| **Integration with LLMs** | Easy – designed to integrate with models and provides built-in support for ML tasks. | Moderate – supports integration with models, but might require more setup compared to Gradio. | Challenging – not natively designed for ML models, requires custom integration and handling. |
| **Real-Time Updates**   | Supported – allows for real-time interaction and feedback. | Supported – handles live updates and interactions effectively. | Supported – handles real-time updates well for games and simulations. |
| **Deployment**          | Easy – Gradio apps can be shared through links or integrated into other platforms. | Easy – Streamlit apps can be deployed as web apps, and integration with cloud services is straightforward. | Complex – typically requires packaging and distribution as standalone applications. |
| **Customizability**     | Moderate – offers customization within predefined components. | High – provides flexibility in designing custom UIs and layouts. | High – allows for complete control over graphics and interactions, but requires more effort. |
| **Performance**         | Good – optimized for handling ML model interactions. | Good – performs well with data-heavy applications and real-time updates. | High – optimized for games and interactive graphics, performance depends on the implementation. |
| **Learning Curve**      | Low – easy to start with for ML applications. | Low to Moderate – easy for data apps, but might need learning for complex interactions. | High – requires learning Pygame library and game development concepts. |
| **Page Navigation Capabilities** | Limited – no native support; workarounds involve using different components or interfaces within the same app. | Limited but Possible – does not support traditional page navigation but can use elements like `st.selectbox` or `st.radio` to switch between views. | Supported but Manual – no built-in page navigation; requires manual coding to handle different screens or states. |