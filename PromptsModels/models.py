from pydantic import BaseModel,Field
from typing import Annotated


class Summary(BaseModel):

    summary:Annotated[str,Field(...,description="Summary of the text")]