''' Import required packages'''
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.models import Book, Review
from app.schemas import *
from app.utility import send_confirmation_email


Base.metadata.create_all(bind=engine)

app = FastAPI()    # creating app


def get_db():
    '''database connection establishement'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#CRUD Operatins for Book
@app.get("/books/", response_model=list[BookResponse])
def get_books(author: str = None, publication_year: int = None, db: Session = Depends(get_db)):
    '''Read all records for book'''
    if author:
        books = db.query(Book).filter(Book.author == author).all()
    elif publication_year:
        books = db.query(Book).filter(Book.publication_year == publication_year).all()
    else:
        books = db.query(Book).all()
    return books


@app.get("/books/{book_id}/", response_model = BookResponse)
def get_books(book_id: int, db: Session = Depends(get_db)):
    '''Read single record for book'''
    return db.query(Book).filter(Book.id == book_id).first()


@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    '''Create Book'''
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/books/{book_id}/", response_model = BookUpdate)
def update_book(book_id: int, book_update : BookUpdate, db: Session = Depends(get_db)):
    '''update single Book record'''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code = 404, Detail= 'Book not found')
    for key, value in book_update.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    '''delete single book record'''
    db.query(Book).filter(Book.id == book_id).delete()
    db.commit()
    return {"Message": "Book deleted successfully"}


#CRUD opertaions for Reviews
@app.post("/books/{book_id}/reviews/", response_model=ReviewResponse)
def create_review(book_id: int, review: ReviewCreate, background_tasks: BackgroundTasks,
                    db: Session = Depends(get_db)):
    '''Create Review for book using their id'''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    background_tasks.add_task(send_confirmation_email, db_review.id)
    return db_review


@app.get("/books/{book_id}/reviews/", response_model=list[ReviewResponse])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    '''Read reviews for book as per their id'''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_book.reviews


@app.put("/books/{book_id}/reviews/{review_id}/", response_model = ReviewUpdate)
def update_review(book_id: int, review_id: int,
                    review_update:ReviewUpdate, db: Session = Depends(get_db)):
    '''Update single review for single book'''
    db_review = db.query(Review).filter(Review.id == review_id,
                                            Review.book_id == book_id).first()
    if db_review is None:
        raise HTTPException(status_code = 404, detail = "This id is not found")

    for key, value in review_update.dict().items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@app.delete("/books/{book_id}/reviews/{review_id}")
def delete_review(book_id : int, review_id: int, db: Session = Depends(get_db)):
    '''Delete the single review'''
    db_review = db.query(Review).filter(Review.id == review_id, Review.book_id == book_id).first()
    
    if db_review is None:
        raise HTTPException(status_code = 404, detail = "This id is not found")
    
    db.delete(db_review)
    db.commit()
    return {"message":"Review deleted successfully"}
    