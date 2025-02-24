import logging
import os
from typing import Dict, List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import bigquery
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI
from pydantic import BaseModel

load_dotenv()

if bool(os.getenv("DEBUG")):
    logging.basicConfig(level=logging.DEBUG, filemode="w", filename="log.txt")
else:
    logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

bq_client = bigquery.Client()
llm = ChatVertexAI(model="gemini-1.5-flash-001")


def generate_response(question: str,
                      stackoverflow_results: List[Dict[str, str]]
                      ) -> AIMessage:
    context = "\n".join(
        [f"Answer: {q['body']}" for q in stackoverflow_results])

    messages = [
        SystemMessage(
            content=f"You are an AI assistant that answers programming questio\
                    ns using Stack Overflow data.\nHere are some Stack Overflo\
                    w answers:\n'{context}'"), HumanMessage(
            content=f"User asked: '{question}'\nProvide a concise and accurate\
                     response. If the question isn't programming related, tell\
                     the User to make one.")]

    return llm.invoke(messages)


def query(query: str, limit=5) -> List[Dict[str, str]]:
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
        # query_res = list(map(lambda row: {"body": row["body"]}, query_res))
        logging.info(f"Decoded results: {query_res}")
        response = generate_response(question, query_res)
        logging.info(f"Generated reponse: {response.content}")
        return {"answer": response.content}
    except Exception as e:
        logging.exception(str(e))
        raise HTTPException(
            {"error": "Unable to process question at this time."},
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
