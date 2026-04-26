from Database.dbservices import get_job,add_summary,fail_job_id
from PromptsModels.models import Summary
from PromptsModels.prompts import summary_prompt
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

SECRET_KEY=os.getenv("OPENAI_KEY")

model=ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=SECRET_KEY
)

structured_model=model.with_structured_output(Summary)
promptTemplate=summary_prompt

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
async def summary_gen(text):
    return text
    
async def summarize(inqueue,outqueue):

    while True:
        job_id=await inqueue.get()
        try:
            if job_id:
                job= await get_job(job_id)

                status=job.status
                text=job.text
                stage=job.stage

                if stage=="EXTRACT":
                    try:
                        if text and status!="FAILED":
                            summary=await summary_gen(text)
                            await add_summary(job_id,summary,"SUMMARIZE")
                            await outqueue.put(job_id)

                        elif status=="COMPLETED":
                            pass
                        
                        else:
                            await fail_job_id(job_id)
                    except RetryError as e:

                        logging.error(f"An Error Occured during Summarizing stage with job_id: {job_id} due to {e.last_attempt.exception()}")
                        await fail_job_id(job_id)
        finally:
            inqueue.task_done()
                