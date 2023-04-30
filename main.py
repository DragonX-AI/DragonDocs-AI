from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import openai
import os

app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

# Read the API key from the WSL environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create a homepage route
@app.get("/")
def index():
    return {"ok": True}

@app.post("/api/ai/docs")
async def generateDocs(request: Request, aiReq: str = Form(...)):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="class Log:\n"+aiReq+"Here's what the above class is doing, explained in a concise way:\n1.",
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )
    result = response.choices[0].text
    
    return {"result": result, "request": aiReq}