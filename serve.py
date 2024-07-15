from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import openai
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
import os
from dotenv import load_dotenv
from langserve import add_routes

load_dotenv()

openai.api_key=os.getenv('OPENAI_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')

model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# 1. Create prompt template 

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])
 

parser=StrOutputParser()

##Create chain

chain=prompt_template|model|parser


app=FastAPI(title='Langchain server',
            version="1.0",
            description="Language Translator ")

## App defination 

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn  
    uvicorn.run(app,host="127.0.0.1",port=8000)