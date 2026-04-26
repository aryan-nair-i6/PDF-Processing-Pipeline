from Database.databasemodels import Base
from Database.database import sync_engine

Base.metadata.create_all(bind=sync_engine)

# import os 
# from passlib.context import CryptContext

# hasher=CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )

# folder="filefolder"

# files=os.listdir(folder)

# for file in files:
#     print(hasher.hash(file))