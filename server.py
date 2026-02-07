from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os

groq_api_key = "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"

llm = ChatGroq(api_key = groq_api_key, model="qwen/qwen3-32b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{input}")
])


chain = prompt | llm | StrOutputParser()

app = FastAPI(
    title="My lightning AI Langserve API",
    version = "1.0",
    description = "Deployed with one command: lightning deploy server.py --cloud"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(
    app,
    chain,
    path="/api", 
    input_type=str,
    output_type=str,

)


@app.get("/")
def home():
    return {
        "message": "Langserve API is Live",
        "docs": "/docs",
        "playground": "/api/playground",
        "invoke_example": 'curl -X POST "http://localhost:8080/api/invoke" -H "Content-Type: application/json" -d \'{"input": "Hello!"}\''
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)