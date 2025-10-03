import uvicorn
from fastapi import FastAPI, Body

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

BOOKS = [
    Book(1, "1984", "George Orwell", "Dystopian novel", 5),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Classic novel", 5),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "Jazz Age novel", 4),
    Book(4, "Moby Dick", "Herman Melville", "Adventure at sea", 4),
    Book(5, "Pride and Prejudice", "Jane Austen", "Romantic classic", 5),
    Book(6, "War and Peace", "Leo Tolstoy", "Epic historical novel", 5)
]

app = FastAPI()

@app.get('/books')
def get_books():
    return BOOKS