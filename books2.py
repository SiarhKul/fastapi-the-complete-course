from typing import Optional

from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, status

import book


class Book():
    id: int
    title: str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The book's id", default=None)
    title: str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str= Field(min_length=1, max_length=100)
    rating:int = Field(gt=-1, lt=6)
    published_date:int = Field(gt=2000)
    model_config = {
        "json_schema_extra": {
            'example': {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A story about teenage angst and alienation.",
                "rating": 4,
                "published_date": 2000,
            }
        }

    }

BOOKS = [
    Book(1, "1984", "George Orwell", "Dystopian novel", 5,2001),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Classic novel", 5,2004),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "Jazz Age novel",3, 2003),
    Book(4, "Moby Dick", "Herman Melville", "Adventure at sea", 4 ,2006),
    Book(5, "Pride and Prejudice", "Jane Austen", "Romantic classic",2, 2008),
    Book(6, "War and Peace", "Leo Tolstoy", "Epic historical novel",1, 2009),
]

app = FastAPI()

@app.get('/books')
async def get_books():
    return BOOKS

@app.post('/create_book')
async def create_book(book:BookRequest):
    new_book= Book(**book.model_dump())
    BOOKS.append( find_book_id( new_book))

@app.get('/books/{book_id}')
async def get_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {'error': 'Book not found'}

@app.get('/books/')
async def find_book_by_rating(book_rating:int):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return


@app.put('/books/update_book')
async def update_boo(book: BookRequest):
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book.id:
            BOOKS[index] = Book(**book.model_dump())

@app.delete('/book/{book_id}')
async def delete_book(book_id:int):
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book_id:
            BOOKS.pop(index)
            break

@app.get('/books/by/{published_date}')
async def find_book_by_published_date(published_date: int):
    published_dates = []
    for b in BOOKS:
        if b.published_date == published_date:
            published_dates.append(b)
    return published_dates



def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) ==0 else BOOKS[-1].id + 1
    return book