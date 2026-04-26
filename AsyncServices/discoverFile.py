import os 
import asyncio
import hashlib  # Add this import
from Database.dbservices import check_job_id, add_job_id
from dotenv import load_dotenv

load_dotenv()

async def discover(outqueue):
    
    dir_length=0
    
    while True:
        path=os.getenv("FOLDER_PATH")
        files=os.listdir(path)
        
        if len(files)!=dir_length:
            dir_length=len(files)
            
            for file in files:
                # Use SHA-256 hash of the filename (or full path) instead of bcrypt
                # Option 1: Hash just the filename
                job_id = hashlib.sha256(file.encode()).hexdigest()
                
                # Option 2: Hash the full file path (more unique)
                # full_path = os.path.join(path, file)
                # job_id = hashlib.sha256(full_path.encode()).hexdigest()
                
                if not await check_job_id(job_id):
                    await add_job_id(job_id, file, "DISCOVER", "PENDING")
                    await outqueue.put(job_id)
        
        await asyncio.sleep(5)  # Add 'await' here