import os
#from dotenv import load_dotenv
import streamlit as st
import PyPDF2
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from PIL import Image


#import pickle5 as pickle
#from pathlib import Path

st.title('Chatea con tu PDF 💬')
image = Image.open('chatconpdf.png')
st.image(image, width=400)

ke = st.text_input('Ingresa tu clave para comenzar')

#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke

pdfFileObj = open('example.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)


    # upload file
pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

   # extract the text
if pdf is not None:
      from langchain.text_splitter import CharacterTextSplitter
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
         text += page.extract_text()

   # split into chunks
      text_splitter = CharacterTextSplitter(separator="\n",chunk_size=500,chunk_overlap=20,length_function=len)
      chunks = text_splitter.split_text(text)

# create embeddings
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)

# show user input
      st.subheader("Escribe qué quieres saber sobre el documento")
      user_question = st.text_input(" ")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)

        llm = OpenAI(model_name="gpt-4")
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          print(cb)
        st.write(response)
