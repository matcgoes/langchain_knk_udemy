from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model=ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=groq_api_key)


# 1 Create prompt template
generic_template="Translate the following into {language}. Reply only the translation"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template),
        ("user", "{text}")
    ]
)

# 2 Create output parser
output_parser = StrOutputParser()

# 3 Create chain
chain = prompt | model | output_parser

# 4 Create FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API to translate text using Langchain and Groq"
)

# 5 Add chain routes
add_routes(
    app, 
    chain, 
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)