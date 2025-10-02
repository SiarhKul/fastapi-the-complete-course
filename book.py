import uvicorn
from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'The Great Gatsby', 'author': 'Author One', 'category': 'science'},
    {'title': 'Sapiens: A Brief History of Humankind', 'author': 'Yuval Noah Harari', 'category': 'non-fiction'},
    {'title': 'Dune', 'author': 'Frank Herbert', 'category': 'science fiction'},
    {'title': '1984', 'author': 'George Orwell', 'category': 'dystopian'},
    {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'fantasy'},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{boot_author}")
async def read_books_by_category(title: str):
    return list(filter(lambda book: book['boot_author'] == title, BOOKS))


@app.get('/books/{boot_author}/')
async def read_query_parms(boot_author: str, category: str):
    filtered_books = [
        book for book in BOOKS
        if book['author'].lower() == boot_author.lower() and book['category'].lower() == category.lower()
    ]

    return filtered_books

@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return BOOKS

@app.put('/books/update_book')
async def update_book(updated_book =Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title')== updated_book.get('title'):
            BOOKS[i] = updated_book

    return updated_book

@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS.get('title') == book_title:
            BOOKS.pop(i)
    return f'Book titled {book_title} deleted'

@app.get('/books/update_by/{author}')
async def read_book_by_author(author:str):
    authors =[]

    for book in  BOOKS:
        if book.get('author').lower() == author.lower():
            authors.append(book)

    return authors

if __name__ == "__main__":
    uvicorn.run(
        "book:app",         # The import string for your app
        host="127.0.0.1",   # The host to bind to
        port=8000,          # The port to listen on
        reload=True         # Equivalent to the --reload flag
    )
