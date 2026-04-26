
from Database.dbservices import get_job,fail_job_id,add_text
from langchain_community.document_loaders import PyPDFLoader
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s-%(levelname)s-%(message)s"
)

from tenacity import retry, stop_after_attempt, wait_random_exponential,RetryError

@retry(
    stop=stop_after_attempt(6),
    wait=wait_random_exponential(multiplier=1, max=60),
    reraise=False
)
async def loader_1(address):
    loader=PyPDFLoader(address)
    docs=await loader.aload()
    text=""
    for doc in docs:
        text+=doc.page_content
    return text

async def extract(inqueue,outqueue):

    while True :
        job_id=await inqueue.get()

        try:
            if job_id:
                job=await get_job(job_id)
                address=job.file_address
                status=job.status
                stage=job.stage

                if stage=="DISCOVER":

                    try:
                        if status!="FAILED" and address.lower().endswith(".pdf"):
                            text=await loader_1(address)

                            await add_text(job_id,text,"EXTRACT")
                            await outqueue.put(job_id)

                        elif status=="COMPLETED":
                            pass

                        else:
                            await fail_job_id(job_id)

                    except RetryError as e:
                        logging.error(f"An Error Occured during Text Extracting stage with job_id: {job_id} due to {e.last_attempt.exception()}")
                        await fail_job_id(job_id)
        finally:
            inqueue.task_done()