from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional

app = FastAPI()

#---Veri Modeli---
# Kullanıcıdan gelecek verinin şablonu 

class Book(BaseModel):
    id: Optional[int] = None
    title: str #Kitap Adı
    author: str #yazar
    pages: int #sayfa sayısı


#---Sahte Veritabanı---
books_db = [
    {"id":1, "title":"Simyacı","author":"Paulo Coelho","pages":188},
    {"id":2, "title":"1984","author":"George Orwell","pages":328}
]     

#---Endpointler---

#1. Ana Sayfa
@app.get("/")
def home():
    return{"Mesaj": "Kitaplık API çalışıyor"}

#2. Tüm kitapları listele
@app.get("/books",response_model=List[Book])
def get_books():
    return books_db

#3. Yeni kitap ekle
@app.post("/books",response_model=Book)
def add_book(book:Book):
    if len(books_db)>0:
        new_id = books_db[-1]["id"] + 1
    else:
        new_id = 1

    book_data = book.dict()
    book_data["id"] = new_id

    books_db.append(book_data)
    return book_data

#4. Tek Kitap Getir

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id:int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404,detail="Kitap bulunamadı")

#5. Kitap Sil

@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[index]
            return{"Mesaj":"Kitap Silindi"}
    raise HTTPException(status_code=404,detail="Kitap Bulunamadı")


