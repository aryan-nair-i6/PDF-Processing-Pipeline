from langchain_openai import OpenAIEmbeddings
from Database.dbservices import get_job,fail_job_id,add_collection_name
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import asyncio
from dotenv import load_dotenv 
load_dotenv()

SECRET_KEY=os.getenv("OPENAI_KEY")

embed_model=OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=SECRET_KEY,
    dimensions=54
)

splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

from tenacity import retry, stop_after_attempt, wait_random_exponential,RetryError
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s-%(levelname)s-%(message)s"
)


@retry(
    stop=stop_after_attempt(6),
    wait=wait_random_exponential(multiplier=1, max=60),
    reraise=False
)
def create_vdb(summary,job_id):
    docs=splitter.split_text(summary)

    vectorstore=Chroma.from_texts(
        texts=docs,
        embedding=embed_model,
        collection_name=job_id,
        persist_directory="vectorstore")

async def load(inqueue):

    while True:
        job_id=await inqueue.get()
        try:
            if job_id:
                job=await get_job(job_id)
                status=job.status
                summary=job.summary
                stage=job.stage

                
                if stage=="SUMMARIZE":
                    try:
                        if summary and status!="FAILED":
                            await asyncio.to_thread(create_vdb, summary, job_id)
                            await add_collection_name(job_id,"LOAD","COMPLETED")
                            
                        elif status=="COMPLETED":
                            pass
                            
                        else:
                            await fail_job_id(job_id)
                    except RetryError as e:
                        logging.error(f"An Error Occured during Loading Vector DB stage with job_id: {job_id} due to {e.last_attempt.exception()}")
                        await fail_job_id(job_id)
        finally:
            inqueue.task_done()
        
                