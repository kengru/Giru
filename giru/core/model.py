from dataclasses import dataclass
from enum import Enum, unique

from pydantic import BaseModel


@unique
class ReplierType(str, Enum):
    random_text_from_list = "text"
    random_document_from_list = "document"
    random_corrupted_text_from_list = "corrupted_text"


class ReplierConfiguration(BaseModel):
    pattern: str
    type: ReplierType
    data: list[str]

