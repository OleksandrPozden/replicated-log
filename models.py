from pydantic import computed_field
from pydantic import BaseModel
from datetime import datetime
from pydantic import conint
from hashlib import sha256

class Log(BaseModel):
    message: str
    created_at: datetime

    @computed_field
    @property
    def hash_id(self) -> str:
        string_to_hash = self.message + str(self.created_at.timestamp())
        return sha256(string_to_hash.encode()).hexdigest()

class RESTLog(BaseModel):
    message: str
    write_concern: conint(ge=1)
