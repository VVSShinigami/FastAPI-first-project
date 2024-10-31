from fastapi import FastAPI, HTTPException, Request, status, Form
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(title='Description of the book',
                             max_length=100,
                             min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "e15f27fe-71b0-40e3-8838-16fbf2c64381",
                "title": "Computer Science",
                "author": "Kolyasik",
                "description": "A very nice description of a book",
                "rating": "75"
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: str = Field(
        None, title="description of the book", max_length=100, min_length=1
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey? why do you want {exception.books_to_return}"
                 f"books? You need to read more!"}
    )
    

@app.post("/books/login")
async def book_login(book_id: int, username: str = None, password: str = None):
    if username == 'FastAPIUser' and password == "test1234!":
        return BOOKS[book_id]
    return "Invalid User"



@app.get("/")
async def read_all_books(books_to_return: int | None = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_book_no_api()
    
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/кфешт/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1 
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_book_no_api():
    book_1 = Book(id="e673b4f2-e9bd-422f-8276-0b2995e02fee",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="eba9ce05-8fca-4f64-aa4a-026f8bb53889",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="98bb70f1-28fd-409e-8ec9-eb8b95420b2d",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=90)
    book_4 = Book(id="eb7b17e5-8006-415f-9939-8b739f31de0b",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=80)
    book_5 = Book(id="28afcc9a-522a-48dc-a8c0-048ce51960d2",
                  title="Title 5",
                  author="Author 5",
                  description="Description 5",
                  rating=20)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header-Error":
                                  "Nothing to be seen at the UUID"})













