# Chatbot
This repo consist of `RAG` implementaion to `OpenAI model` for your private chatbot. The `pdf` files are stored in `Azure storage` which are retrived by this app and stored as vector embedding in `Pinecone` database.
# Instruction for use
* clone this repo
  ```
  git clone https://github.com/sangamdeuja/RAG-LLMchatbot.git
  ```
* create.env file inside root folder and provide the following credentials
  ```
  STORAGE_ACCOUNT_NAME=your_azure_storage_account_name
  ```
  ```
  STORAGE_CONTAINER_NAME=your_container
  ```
  ```
  CONN_STRING=your_storage_connection_string
  ```
  ```
  PINECONE_API_KEY=your_pinecone_api_key
  ```
  ```
  INDEX_NAME=your_index_name
  ```
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```
* create pinecone account and index in pincone.io and provide detail in above `.env` file
* create azure storage and container and provide and provide detail in above `.env` file
* create openai api key and and provide detail in above `.env` file
* (Optional) If you want to run without docker create virtual env, install packages from requrirements.txt and run the following
  ```
  streamlit run main.py
  ```
* To run in docker, run the following code
  ```
  docker build -t chatbot .
  ```
  ```
  docker run -p 8501:8501 chatbot
  ```


