from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from pydantic import conint

class Log(BaseModel):
    message: str
    created_at: datetime = Field(default_factory=datetime.now)

class RESTLog(BaseModel):
    message: str
    write_concern: conint(ge=1)
