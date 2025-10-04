from typing import Optional

from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, status

class Book():
    id: int
    title: str
    author:str
    description:str
    rating:int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The book's id", default=None)
    title: str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str= Field(min_length=1, max_length=100)
    rating:int = Field(gt=-1, lt=6)
    model_config = {
        "json_schema_extra": {
            'example': {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A story about teenage angst and alienation.",
                "rating": 4
            }
        }

    }

BOOKS = [
    Book(1, "1984", "George Orwell", "Dystopian novel", 5),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Classic novel", 5),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "Jazz Age novel", 4),
    Book(4, "Moby Dick", "Herman Melville", "Adventure at sea", 4),
    Book(5, "Pride and Prejudice", "Jane Austen", "Romantic classic", 1),
    Book(6, "War and Peace", "Leo Tolstoy", "Epic historical novel", 1)
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




def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) ==0 else BOOKS[-1].id + 1
    return book