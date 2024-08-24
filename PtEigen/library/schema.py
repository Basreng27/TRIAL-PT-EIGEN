from ninja import Schema
from datetime import date
from typing import Optional

class BookSchema(Schema):
    code: str
    title: str
    author: str
    stock: int
    
class MemberSchema(Schema):
    code:str
    name:str
    penalty_until: Optional[date] = None