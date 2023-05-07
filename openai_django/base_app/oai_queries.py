# import settings
from django.conf import settings
import os
import openai
import PyPDF4
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

# OpenAI API Key
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    raise Exception('OpenAI API Key not found')

with open('/Users/siri/Downloads/dmv2023.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF4.PdfFileReader(pdf_file)
    # Get the total number of pages
    num_pages = pdf_reader.numPages
    # Loop through each page and extract the text
    text = ''
    for page in range(num_pages):
        # Get the page object
        pdf_page = pdf_reader.getPage(page)
        # Extract the text from the page
        page_text = pdf_page.extractText()
        # Append the page text to the overall text
        text += page_text
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)

texts = text_splitter.split_text(text)

print(len(texts))

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)
chain = load_qa_chain(OpenAI(), chain_type="stuff")

def get_completion(prompt):
    query = prompt
    
    print(prompt)
    docs = docsearch.similarity_search(query)
    return chain.run(input_documents=docs, question=query)
