import chromadb
from dotenv import load_dotenv
import os
from openai_client.client import client



# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


def get_openai_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL, 
        input=text
    )
    return response.data[0].embedding

def index_document(doc_id, document_text):
    embedding = get_openai_embedding(document_text)

    collection.add(
        ids=[doc_id],
        documents=[document_text],
        embeddings=[embedding]
    )
    return {"status": "success", "doc_id": doc_id}

def retrieve_similar_documents(query, top_k=3):
    query_embedding = get_openai_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    documents = results['documents'][0] if results['documents'] else []
    return documents
