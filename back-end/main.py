import logging
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from google.cloud import bigquery
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_google_vertexai import ChatVertexAI
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from pydantic import BaseModel


load_dotenv()
if bool(os.getenv("DEBUG")):
    logging.basicConfig(level=logging.DEBUG, filemode="w", filename="log.txt")
else:
    logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
)

bq_client = bigquery.Client()
llm = ChatVertexAI(model="gemini-1.5-flash-001")

def generate_response(question: str, 
                      stackoverflow_results: List[Dict[str, str]]
) -> AIMessage:
    context = "\n".join([f"Answer: {q['body']}" for q in stackoverflow_results])
    
    messages = [
        SystemMessage(content="You are an AI assistant that answers programming questions using Stack Overflow data."),
        HumanMessage(content=f"User asked: {question}\nHere are some relevant Stack Overflow answers:\n{context}\nProvide a concise and accurate response.")
    ]
    
    return llm(messages)


def query(query: str, limit = 5) -> List[Dict[str, str]]:
    sql = f"""
    SELECT body
    FROM `bigquery-public-data.stackoverflow.posts_answers`
    WHERE id IN (
            SELECT accepted_answer_id
            FROM  `bigquery-public-data.stackoverflow.posts_questions`
            WHERE title LIKE '%{query}%'
            )
    ORDER BY score DESC
    LIMIT {limit};
    """
    results = [dict(row) for row in bq_client.query(sql).result()]
    logging.debug(f"Query executed: {sql}\nResults: {results}")
    return results

class Question(BaseModel):
    question: str

@app.post("/ask")
async def post_ask(question_request: Question):
    question = question_request.question
    try:
        logging.debug(question)
        query_res = query(question)
        #query_res = list(map(lambda row: {"body": row["body"]}, query_res))
        logging.info(f"Decoded results: {query_res}")
        response = generate_response(question, query_res)
        logging.info(f"Generated reponse: {response.content}")
        return {"answer": response.content}
    except Exception as e:
        logging.exception(str(e))
        return {"error": "Unable to process question at this time."}, status.HTTP_500_INTERNAL_SERVER_ERROR

if __name__=="__main__":
    uvicorn.run(app, port=8080)
