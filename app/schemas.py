'''Import Required models'''
from pydantic import BaseModel


class BookBase(BaseModel):
    '''sceama for books'''
    title: str
    author: str
    publication_year: int

class BookCreate(BookBase):
    '''shema for create book record'''
    pass

class BookResponse(BookBase):
    '''shema for Read book record'''
    id: int

class BookUpdate(BookBase): 
    '''shema for modify book record'''
    pass

class ReviewBase(BaseModel):
    '''shema for reviews'''
    text: str
    rating: float

class ReviewCreate(ReviewBase):
    '''shema for create review record'''
    pass

class ReviewResponse(ReviewBase):
    '''shema for read review record'''
    id: int
    
class ReviewUpdate(ReviewBase):
    '''shema for modify review record'''
    pass