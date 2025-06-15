from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from typing import Optional
# from embedding import index_document, retrieve_similar_documents
from document_indexer.embedding import index_document, retrieve_similar_documents
from pydantic import BaseModel
from document_indexer.text_extractor import extract_text



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "csv", "docx"}


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class Document(BaseModel):
    doc_id: str
    text_chunks: list[str]

class Text(BaseModel):
    text_chunks: str





@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload_and_index")
async def upload_and_index(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="File type not allowed.")

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract text chunks from the uploaded file
        text_chunks = extract_text(file_path, max_sentences_per_chunk=15)

        if not text_chunks:
            raise HTTPException(status_code=400, detail="No text could be extracted from the file.")

        indexed_docs = []

        # Index each chunk with a unique doc_id
        for chunk in text_chunks:
            doc_id = str(uuid.uuid4())
            index_document(doc_id, chunk)
            indexed_docs.append({"doc_id": doc_id, "chunk": chunk})

        return {
            "message": "File uploaded and indexed successfully",
            "file_path": file_path,
            "indexed_docs": indexed_docs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
def index(doc: Text):
    """
    Endpoint to index or update a document using provided text chunks.
    """
    try:
        doc_id = str(uuid.uuid4())
        result = index_document(doc_id, doc.text_chunks)
        return {"message": "Document indexed successfully",
                "doc_id": doc_id,
                "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/retrieve")
def retrieve(request: QueryRequest):
    try:
        docs = retrieve_similar_documents(request.query, request.top_k)
        return {"results": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
