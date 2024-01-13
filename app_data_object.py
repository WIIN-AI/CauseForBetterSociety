from dataclasses import dataclass, field
from typing import List, Union
from datetime import datetime
import uuid
from fastapi import File, UploadFile, Form


@dataclass
class AddImageBaseModel:
    file: UploadFile = File(...)
    heading: str = None
    description: str = None
    location: str = None
    email: str = None
    like: bool = False
    user_visibility: bool = False
    uuid_: uuid = str(uuid.uuid4())
    comments: List[str] = field(default_factory=list)
    today_date = datetime.now().strftime("%d-%m-%Y")


print(AddImageBaseModel().email)
