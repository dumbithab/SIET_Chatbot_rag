import faiss
import numpy as np
from groq import Groq
from pypdf import PDFReader
from sentence_transformer import SentenceTransformer
#load pdfs
def load_pdf (pdf_path):
  reader = PDFReader(str(pdf_path))
  mypage = [ i.extract_text() or "" for i in reader.pages]
  full_text = "\n".join(mypage).strip()
  if not full_text:
    raise ValueError("No readable text found")
  return full_text
#chunking
def create_chunks(full_text, chunksize = 500, overlap =100):
  chunks = []
  start = 0
  while start<learn(full_text):
    end = start + chunksize
    chunk = full_text[start:end] 
    if chunk.strip()
    chunks.append(chunks)
    start = end - overlap
   return chunks
 #embedding
 def build_vectors (chunks, model_name = "all-miniLM-L6-v2"):
   embed_model = SentenceTransformer(model_name)
   embed_vectors = embed_model.encode(chunks, convert_to_numpy = True)
   faiss.normalize_L2(embed_vectors)
   index = faiss.IndexFlatIP(embed_vectors.shape[1])
   
    
    
    

