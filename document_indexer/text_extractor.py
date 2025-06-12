import os
import re
from docx import Document
import PyPDF2
import io
import csv

def extract_text(file_path: str, max_sentences_per_chunk: int = 15) -> list[str]:
    """
    Extracts text content from the provided file path and returns it as a list of chunks,
    where each chunk has at most max_sentences_per_chunk. Supports PDF, CSV, and DOCX files.

    Args:
        file_path (str): The path to the file from which to extract text.
        max_sentences_per_chunk (int): The maximum number of sentences allowed in each text chunk.

    Returns:
        list[str]: A list of text chunks, or an empty list if an error occurs.
    """
    file_extension = file_path.split(".")[-1].lower()
    full_text = ""
    chunks = []

    try:
        if file_extension == "pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    full_text += page.extract_text() or ""

        elif file_extension == "csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    full_text += ' '.join(row) + '\n'

        elif file_extension == "docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                full_text += para.text + '\n'
        else:
            print(f"Unsupported file type: {file_extension}")
            return []
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while extracting text from '{file_path}': {e}")
        return []
    finally:
        # Delete the document after extraction
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file '{file_path}': {e}")

    if not full_text:
        return []

    # Split the text into sentences
    # This regex attempts to split on periods, question marks, and exclamation points,
    # followed by a space or end of string, while trying to avoid splitting on abbreviations.
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', full_text)

    current_chunk_sentences = []
    for sentence in sentences:
        if sentence.strip():  # Ensure sentence is not just whitespace
            current_chunk_sentences.append(sentence.strip())
            if len(current_chunk_sentences) >= max_sentences_per_chunk:
                chunks.append(" ".join(current_chunk_sentences))
                current_chunk_sentences = []

    # Add any remaining sentences as the last chunk
    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))

    return chunks

# Example usage:

# Dynamically pick the first (or only) file in the folder
def get_file_in_folder(folder_path):
    files = os.listdir(folder_path)
    files = [file for file in files if not file.startswith('.')]  # Exclude hidden files like .DS_Store (Mac)
    if not files:
        return "no file"
    raise FileNotFoundError("No files found in the folder.")
    
    if len(files) > 1:
        return "no file"
    print("Warning: More than one file found. Using the first file.")
    return os.path.join(folder_path, files[0])

# Example usage:
# folder_path = "uploaded_files"
# file_to_process = get_file_in_folder(folder_path)

# text_chunks = extract_text(file_to_process, max_sentences_per_chunk=15)



# if text_chunks:
#     print(f"\n--- Extracted Content in {len(text_chunks)} Chunks ---")
#     for i, chunk in enumerate(text_chunks):
#         print(f"\nChunk {i+1}:")
#         print(chunk)
# else:
#     print("No content extracted or an error occurred.")

# file_to_process = "uploaded_files/Obidokun_Tunji_David.pdf"  # Replace with your actual file path
# text_chunks = extract_text(file_to_process, max_sentences_per_chunk=15)

# if text_chunks:
#     print(f"\n--- Extracted Content in {len(text_chunks)} Chunks ---")
#     print(text_chunks)
#     for i, chunk in enumerate(text_chunks):
#         print(f"\nChunk {i+1}:")
#         print(chunk)
# else:
#     print("No content extracted or an error occurred.")