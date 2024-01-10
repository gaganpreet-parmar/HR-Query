import os
from dotenv import load_dotenv
import weaviate
import json
from langchain.vectorstores import Weaviate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader

load_dotenv()

YOUR_WEAVIATE_KEY= os.getenv("YOUR_WEAVIATE_KEY")
YOUR_WEAVIATE_URL= os.getenv("YOUR_WEAVIATE_URL")

def json_print(data):
    print(json.dumps(data, indent=2))

def generateEmbeddings(sentence):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(sentence)

def load_embeddings():
    # specify embedding model (using huggingface sentence transformer)
    embedding_model_name = "all-MiniLM-L6-v2"
    model_kwargs = {"device": "cpu"}
    embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name, 
    model_kwargs=model_kwargs
    )
    print("Loaded embeddings")
    return embeddings

def connectVectorDb():
    # connect Weaviate Cluster
    auth_config = weaviate.AuthApiKey(api_key=YOUR_WEAVIATE_KEY)
    client = weaviate.Client(
        url=YOUR_WEAVIATE_URL,
        auth_client_secret=auth_config,
    )
    client.is_ready()
    print("Loaded Client")
    return client

def createVectorSchema(client,classname):
    schema = {
        "class": classname,
        "description" : "Documents for chatbot",
        "moduleConfig": {
        "text2vec-huggingface": {
          "model": "sentence-transformers/all-MiniLM-L6-v2",
          "options": {
            "waitForModel": True,
            "useGPU": False,
            "useCache": True
            }
          }
        },
        "properties": [
            {
                "name": "content",
                "description": "The content of the paragraph",
                "dataType": ["text"],
            }
        ],
     "vectorizer":"text2vec-huggingface"
    }
    client.schema.create_class(schema)

    print("Created Vector DB Schema")



def ingestDocToWeviate(docs,embeddings,client,classname):

    # Ingest the documents into Weaviate
    """
    vector_db = Weaviate.from_documents(
        docs, embeddings, client=client, by_text=False
    )
    """
    vector_db = Weaviate(client, classname, "content",embedding=embeddings, attributes=["source"])

    # load text into the vectorstore
    text_meta_pair = [(doc.page_content, doc.metadata) for doc in docs]
    texts, meta = list(zip(*text_meta_pair))
    vector_db.add_texts(texts, meta)

    print("Ingested Vector DB")

def loadPdf(file,classname):
    print("Started Loading Vector DB with PDF")

    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = load_embeddings()
    client=connectVectorDb()

    # ingest vector database from data
    ingestDocToWeviate(docs,embeddings,client,classname)

    print("Completed Loading Vector DB with PDF")

def loadTxtDocuments(filePath : str,classname):
    print("Started Loading Vector DB with Txt")
    loader = TextLoader(filePath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    
    # define embedding
    embeddings = load_embeddings()
    client=connectVectorDb()

    # ingest vector database from data
    ingestDocToWeviate(docs,embeddings,client,classname)
    print("Completed Loading Vector DB with Txt")

if __name__ == '__main__':
    
    #print(docs)
    client=connectVectorDb()
    client.schema.delete_all()

    embeddings= load_embeddings()

    schema=createVectorSchema(client,"MyCollection")


    #print(client.schema.get())
    docs=loadTxtDocuments("modi.txt","MyCollection")
    #docs=loadTxtDocuments("infosyshrpolicy.txt","MyCollection")

    json_print(client.query.aggregate("MyCollection").with_meta_count().do())

    """
    #loadPdf("humanRightsStatementInfosys.pdf","MyCollection")

    client=connectVectorDb()
    json_print(client.query.aggregate("MyCollection").with_meta_count().do())

        additional_headers={
        "X-HuggingFace-Api-Key": "YOUR-HUGGINGFACE-API-KEY"
    }
    """
