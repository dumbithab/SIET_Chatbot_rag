import faiss
import numpy as np
from groq import Groq
from pypdf import pdfReader
from sentence_transformers import SentenceTransformer

# loading pdfs
def load_pdf(pdf_path):
  reader=pdfReader(str(pdf_path))
  mypages = [i.extract_text() or "" for i in reader.pages]
  full_text = "\n".join(mypages).strip()
  if not full_text:
    raise valueError("No readable Text Found")
  return full_text


#chunking 
def create_chunks(full_text,chunksize=500,overlap=100):
  chunks=[]
  start=0
  while start<len(full_text):
    end = start + chunksize
    chunk = full_text[start:end]
    if chunk.strip():
      chunks.append(chunk)
      start = end - overlap #500-100=400
    return chunks 

    
    #embedding
    def build_vectors(chunks,model_name= "all-MiniLM-L6-v2"):
      if not chunks:
          raise ValueError("cannot apply embedding without chunks")
      embed_model = SentenceTransformer(model_name)
      embed_vectors = embed_model.encode(chunks,convert_to_numpy=True)
      faiss.normalize_L2(embed_vectors)
      index = faiss.IndexFlatIP(embed_vectors.shape[1])
      index.add(embed_vectors)
      return index, embed_model

    
   #call loadpdf,chunk,embedding
   def load_base(pdf_path= "01_collage_information.pdf"):
       full_text = load_pdf(pdf_path)
       chunks = create_chunks(full_text)
       embed_model,index = build_vector(chunks)
       return  index,embeded_model,chunks

       
       #retrive 
       def retrive_content(question,embed_model,chunks,index,num_chunks=3):
         if not question.strip():
           raise ValueError("Question cannot be blank")
         if num_chunks < 1
           raise ValueError("Request atleast one or more chunks")
         query_embed = embed_model.encode([question],convert_numpy=True)
         faiss.normalize_L2(query_embed)
         sim_score,vec_indices = index.search(query_embed,min(num_chunks,len(chunks)))
         background = ""
         for i in vec_indices[0]:
           if i != -1:
           background += chunks[i]+"\n\n"
        return background 

       #ask:
       def ask_rag(question,embedded_model,chunks,index,api_key,num_chunks=3,model_name = "openai/gpt-oss-120b"):
         key = api_key
         if not key:
           raise ValueError("API key Missing"):
          background = retrive_content(question,embed_model,chunks,index,num_chunks=3)
          prompt = """ you are an proffesional AI assistant.
          Answer user question using ONLY document document background below.
          do not invent or assume facts.
          if information not available,simply say Information Missing.
          Document Background :"""+ background + "user question" + question + "Answer:"
          client = Groq(api_key = key)
          response = client.caht.completions.create(
            model = model_name,
            messages = [{"role":"user",
                         "content":prompt}],
                          temperature = 0.3,
          )
         return response.choice[0].message.content
