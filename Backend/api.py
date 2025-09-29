from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

system_prompt = """You are a helpful assistant that generates comments for a given text.
  The comments should be in the same language as the text, even though the observations are in a different language."""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    logger.info('Health check endpoint called')
    return {"message": "OK"}

@app.post("/comments")
async def get_comments(request: Request):
    
    print(request)
    request_body = await request.json()
    
    text = request_body.get("text")
    tone = request_body.get("tone")
    observations = request_body.get("observations")
    
    openai_response = request_openai(text, tone, observations)
    
    return {"comment": openai_response}
  
@app.post("/content")
async def get_content(request: Request):
    logger.info('Content endpoint called')
    request_body = await request.json()
    url = request_body.get("url")
    
    try:
        # Import crowler only when needed
        import crowler
        content = crowler.get_content(url)
        logger.info(f'Content extracted successfully, length: {len(content) if content else 0} characters')
        return {"content": content}
    
    except Exception as e:
        error_message = str(e)
        logger.error(f'Error extracting content: {error_message}')
        raise HTTPException(status_code=500, detail=error_message)

if __name__ == "__main__":
    api_port = int(os.getenv("API_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=api_port)