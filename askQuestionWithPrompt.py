import os
from dotenv import load_dotenv
from weaviateVectorDb import connectVectorDb
from langchain.vectorstores import Weaviate
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

load_dotenv()

YOUR_OPENAI_KEY = os.getenv("YOUR_OPENAI_KEY")

def retrieveDb(chain_type, k, source):
    client=connectVectorDb()
    vectorstore = Weaviate(client, "MyCollection", "content")
    llm=ChatOpenAI(temperature=0,openai_api_key = YOUR_OPENAI_KEY)

    # Build prompt
    template = """Use the following pieces of context to answer the question at the end. 
    Also, check the text below Current conversation and check if you can find anything relevant and use it to answer current question. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum. Keep the answer as concise as possible. 
    Always say "thanks for asking!" at the end of the answer. 
    {context}
    Current conversation:
    {chat_history}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question","chat_history"],template=template,)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

   
    # Run chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    return qa 


if __name__ == '__main__':
    qa=retrieveDb("stuff", 3,"voice")
    question = "Who is Narendra Modi?"
    chat_history=[]
    #result = qa({"question": question, "chat_history": chat_history})
    result = qa({"question": question})
    print(result)