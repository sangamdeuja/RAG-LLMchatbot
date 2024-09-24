import os
from tqdm import tqdm
import PyPDF2
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Initialize Pinecone and OpenAI
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
embeddings = OpenAIEmbeddings()
index_name = os.getenv("INDEX_NAME")
index = pc.Index(index_name)
client = OpenAI()

# Accessing azure container
from azure.storage.blob import BlobServiceClient
container_name=os.getenv("STORAGE_CONTAINER_NAME")
connection_string=os.getenv("CONN_STRING")


blob_service_client=BlobServiceClient.from_connection_string(connection_string)
container_client=blob_service_client.get_container_client(container_name)

class CitedAnswer(BaseModel):
    answer: str = Field(..., description="The answer to the user question, based only on the given sources.")
    citations: list[str] = Field(..., description="The filename of the specific sources which justify the answer.")


def load_processed_files(file_path='processed_files.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if lines: 
                return lines
    else:
        with open(file_path, 'a') as f:
            pass
        return

    
def save_processed_file(filename, file_path='processed_files.txt'):
    with open(file_path, 'a') as f:
        f.write(f"{filename}\n")


def extract_text_from_pdf(blob_data):
    pdf_data = BytesIO(blob_data)
    reader = PyPDF2.PdfReader(pdf_data)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()  
    return text

def process_individual_pdfs():
    # Get list of all blobs in the container
    blobs = container_client.list_blobs()
    processed_files=load_processed_files()

    for blob in blobs:
        if processed_files is None:
            processed_files=[]
        blob_name = blob.name
        # Only process PDF files
        if not blob_name.endswith(".pdf"):
            continue
        # processed_files=load_processed_files()
        if blob_name not in processed_files: 
            save_processed_file(blob_name)
            
            try:
                # Get the blob client and download the blob (PDF file) as binary
                blob_client = container_client.get_blob_client(blob_name)
                blob_data = blob_client.download_blob().readall()

                # Extract text from the PDF
                pdf_text = extract_text_from_pdf(blob_data)

                # If no text found, skip this file
                if not pdf_text.strip():
                    print(f"No text found in {blob_name}, skipping...")
                    continue

                # Create OpenAI embedding for the extracted text
                embedding_response = client.embeddings.create(input=pdf_text, model="text-embedding-ada-002")
                embedding=embedding_response.data[0].embedding
                
                # Upsert the embedding into Pinecone with metadata (like blob name)
                index.upsert([(blob_name, embedding, {"file_name": blob_name, "text": pdf_text})])

                print(f"Successfully processed and embedded {blob_name}")
                
            except Exception as e:
                print(f"Failed to process {blob_name}: {str(e)}")
