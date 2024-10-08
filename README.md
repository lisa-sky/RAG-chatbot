# RAG-chatbot Overview🤖
Built a RAG-chatbot that allows users to upload text and PDF files, then ask questions about the content of those files using an Azure OpenAI-powered chatbot. It utilizes document chunking and a vectorstore for efficient context retrieval, providing accurate and concise answers based on the uploaded document.

## 🚀 Chatbot Features
- **File Upload**: Users can upload multiple files in `.txt` and `.pdf` formats.
- **Question-Answering Chatbot**: Users can ask questions related to the uploaded files, and the chatbot provides concise answers using context retrieved from the documents.
- **Document Chunking**: Text from large files is split into smaller chunks for efficient processing.
- **Vectorstore for Context Retrieval**: Uses `Chroma` to store document chunks and retrieve relevant content based on user queries.
- **Azure OpenAI Integration**: The chatbot is powered by Azure OpenAI's `gpt-4o` model for high-quality responses.


## Set-up Instructions🛠️

To run this application using the provided Docker and devcontainer setup, follow these steps:

1. **Open the Project in Visual Studio Code**
   - Launch Visual Studio Code.

2. **Install the Remote - Containers Extension**
   - If you haven’t already, install the **Remote - Containers** extension from the Extensions Marketplace.

3. **Open the Project Folder**
   - Click on **File** > **Open Folder** and select the project folder you cloned.

4. **Reopen the Project in a Container**
   - Click on the green icon in the bottom left corner of VS Code.
   - Select **Open Folder in Container** from the dropdown menu.
   - Wait for the container to build and open your project in the devcontainer environment.

5. **Open the Terminal in VS Code**
   - Go to **View** > **Terminal** or press `` Ctrl + ` `` to open the terminal.

6. **Run the Application**
   - In the terminal, run the following command to start the application:
     ```bash
     streamlit run chatbot.py
     ```

7. **Access the Application**
    - Once the application is running, you can access it in your browser at `http://localhost:8501`.



## Documentation for Changes📄
### 1. **PDF File Parsing**
- **Imported `PyPDFLoader`**: This library is utilized to parse PDF files, enabling the application to handle user-uploaded PDF documents efficiently.
- **Temporary File Handling**: Utilized the `tempfile` module to create temporary files for storing uploaded PDFs, ensuring the application can read and process them without leaving residual files on the filesystem.

### 2. **Multiple File Uploads**
- **Feature Enhancement**: The application now supports uploading multiple files at once. Users can upload both `.txt` and `.pdf` files, expanding the scope of questions they can ask related to the content of these files.

### 3. **Default Tenant Error Prevention**
- **Integration of ChromaDB API**: Added the line `chromadb.api.client.SharedSystemClient.clear_system_cache()` to prevent default tenant errors that could occur when the chatbot interacts with the ChromaDB service. This helps ensure a smoother user experience by mitigating potential connection issues.


