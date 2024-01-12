# HR-Query
HR chatbot, utilizing Weaviate as a vector database for efficient storage. Employed Hugging Face for embeddings, and ChatOpenAI for text summarization and answering queries

 <p align="left">
    <p>
      Watch Tutorial on YouTube <a href="https://youtu.be/gkQq2AoGGLY" target="_blank">Building HR ChatBot using Python, OpenAI, Weaviate, Hugging Face and Langchain</a>
    </p>
    
  </p>
  
  <p align="left">
    <p>
       Microservices Architecture Artcile link <a href="https://medium.com/@gaganpreetsingh.parmar/crafting-intelligent-conversations-designing-hr-chatbot-with-llm-langchain-and-microservices-fd295f493ed4" target="_blank">Crafting Intelligent Conversations: Designing HR ChatBot with LLM, Langchain and Microservices</a>
    </p>
    
  </p>

## HIGH Level FLOW

<img width="771" alt="Screenshot 2024-01-09 at 8 18 21 PM" src="https://github.com/gaganpreet-parmar/Chat-Speak/assets/156009742/58a388ef-a7e2-45cb-997b-49aa04257915">

## Get API KEY
1. Go to https://openai.com<br/>
2. Create a new account and get your api key<br/>
3. Go to https://console.weaviate.cloud/<br/>
4. Create a new account and get your api key and weaviate URL. Weaviate provide free cloud sandbox for testing.<br/>

## Get Started
1. Check requirement.txt and install the python libraries.
2. "cd HR-Query/" and create ".env" file. Add below lines. Replace keys and url with one you created for openai and weaviate.<br/>
   YOUR_OPENAI_KEY = "Your OpenAi Key"<br/>
   YOUR_WEAVIATE_KEY= "Your Weaviate Key"<br/>
   YOUR_WEAVIATE_URL="Your Weaviate url"<br/>
3. "pip install python-dotenv" for you haven't done already.

## Run The App
1. cd HR-Query/
2. run command "python weaviateVectorDb.py" to create schema and load initial data.
3. run command "panel serve chatbot.py" on terminal
4. Chatbot will start on link http://localhost:5006/chatbot and you should see below on terminal
   <img width="619" alt="Screenshot 2024-01-09 at 8 59 58 PM" src="https://github.com/gaganpreet-parmar/HR-Query/assets/156009742/fa42ba2c-73f9-46e5-8924-ac1e1c83f010">
5. In case you want to integrate solution to upstream apps like "chat-talk" start the flask rest service using "python getContext.py" and it sould start rest API on
   port 9091.
7. You can curl rest api or use postman<br/>
   curl -X POST -H "Content-Type: application/json" -d '{"id": 1, "content": "your_Question_content_here"}'
   http://localhost:9091/api/resource -u username:password1

For more details on full demo check the youtube video.




