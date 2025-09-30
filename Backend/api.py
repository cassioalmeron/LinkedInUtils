from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from logger import logger
from openairequest import request_openai
from crowler import get_content

load_dotenv()

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
    logger.info('Comments endpoint called')
    request_body = await request.json()
    
    text = request_body.get("text")
    tone = request_body.get("tone")
    observations = request_body.get("observations")
    
    logger.info(f'Processing comment request - text length: {len(text) if text else 0}, tone: {tone}')
    
    try:
        openai_response = request_openai(text, tone, observations)
        logger.info('Comment generated successfully')
        return {"comment": openai_response}
    except Exception as e:
        error_message = str(e)
        logger.error(f'Error generating comment: {error_message}')
        raise HTTPException(status_code=500, detail=error_message)
  
@app.post("/content")
async def get_content(request: Request):
    logger.info('Content endpoint called')
    request_body = await request.json()
    url = request_body.get("url")
    
    try:
        content = get_content(url)
        logger.info(f'Content extracted successfully, length: {len(content) if content else 0} characters')
        return {"content": content}
    
    except Exception as e:
        error_message = str(e)
        logger.error(f'Error extracting content: {error_message}')
        raise HTTPException(status_code=500, detail=error_message)

if __name__ == "__main__":
    api_port = int(os.getenv("API_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=api_port)