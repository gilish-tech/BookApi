from fastapi import APIRouter,HTTPException,status, Depends
from blogapp.model import BookSchema, UpdateBookSchema
from fastapi.responses import  JSONResponse
from settings.settings import BOOK_COLLECTION_NAME,get_db, get_current_user
import json
from bson import ObjectId
from pymongo import errors
import pydantic


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
router =  APIRouter(
    tags=["Book"],
    prefix="/books"
)



@router.get("/allbooks")
def getBooks(user = Depends(get_current_user)):
    db =  get_db()  
    book_col = db[BOOK_COLLECTION_NAME]
    books = book_col.find()
    if books is None :
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this id does not exist"
        )   
    all_books = [book for book in books]
    return all_books  

@router.get("/{id}")
def getBook(id:str,user = Depends(get_current_user)):
    db =  get_db()  
    book_col = db[BOOK_COLLECTION_NAME]
    doc_id = ObjectId(id)
    query = {"_id":doc_id}
    book = book_col.find_one(query)
    if book is None :
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this id does not exist"
        )   
    
    return book

@router.post("/")
def addBook(request:BookSchema,user = Depends(get_current_user)):
    db =  get_db()  
    book_col = db[BOOK_COLLECTION_NAME]
    request_body = request.json()
    request_body_obj = json.loads(request_body)
    # request_body_obj["author"] = 
    try:
        print(request_body_obj)
        result = book_col.insert_one(request_body_obj)
        print(result)
        return {"status":status.HTTP_201_CREATED,"details":result.inserted_id}
    except errors.PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to add Book"
        )     
    
          

@router.delete("/{id}")
def delete_book(id,user = Depends(get_current_user)):
    db =  get_db()  
    book_col = db[BOOK_COLLECTION_NAME]
    doc_id = ObjectId(id)
    query = {"_id":doc_id}
    try:
        result = book_col.delete_one(query)
        return {"status": status.HTTP_204_NO_CONTENT,"details":"deleted"}
    except errors.PyMongoError as e:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )  
     
@router.put("/{id}")
def update_book(id,request:UpdateBookSchema,user = Depends(get_current_user)):
    db =  get_db()  
    book_col = db[BOOK_COLLECTION_NAME]
    doc_id = ObjectId(id)
    query = {"_id":doc_id}
    request_body = request.json()
    request_body_obj = json.loads(request_body)
    my_dict_without_none = {k: v for k, v in request_body_obj.items() if v is not None}
    print(my_dict_without_none)
    try:
        result = book_col.update_one(query,{"$set":my_dict_without_none})
        return {"status": status.HTTP_204_NO_CONTENT,"details":"updated"}
    except errors.PyMongoError as e:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )   