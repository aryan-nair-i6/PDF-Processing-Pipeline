
from Database.database import async_session
from sqlalchemy import select
from Database.databasemodels import Jobs

'''
get_job ------------>(job_id)
fail_job_id -------->(job_id)
check_job_id ------->(job_id)
add_job_id --------->(job_id,file,"DISCOVER","PENDING")
add_text ----------->(job_id,text,"EXTRACT")
add_summary -------->(job_id,summary,"SUMMARIZE")
add_collection_name->(job_id,job_id,"LOAD","COMPLETED")

'''

async def get_job(job_id:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))
        job=result.scalars().first()
        return job
    
async def fail_job_id(job_id:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))
        job=result.scalars().first()
        job.status="FAILED"
        db.commit()

async def check_job_id(job_id:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))

        if result:
            job=result.scalars().first()
            if job:
                return True
            else:
                False
        else:
            False

async def add_job_id(job_id:str,file:str,stage:str,status:str):  #filefolder\100M_Offers_-_Alex_Hormozi.pdf

    async with async_session() as db:

        new_job=Jobs(job_id=job_id,file_address=f"filefolder\{file}",stage=stage,status=status)
        db.add(new_job)
        await db.commit()

async def add_text(job_id:str,text:str,stage:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))
        job=result.scalars().first()
        job.text=text
        job.stage=stage
        await db.commit()

async def add_summary(job_id:str,summary:str,stage:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))
        job=result.scalars().first()
        job.summary=summary
        job.stage=stage
        await db.commit()

async def add_collection_name(job_id:str,stage:str,status:str):

    async with async_session() as db:

        result=await db.execute(select(Jobs).filter_by(job_id=job_id))
        job=result.scalars().first()
        job.collection_name=job_id
        job.stage=stage
        job.status=status
        await db.commit()
