from fastapi import FastAPI


from  routers import authentication,books

app =  FastAPI()



# @app.get("/protected")
# def show_me(user = Depends(get_current_user)):
#       print(user)
#       return("KKKKKKKKKKKKKKKKK")
      
# @app.get("/protecteds")
# def show_me():  
#       return "KKKKKKKKKKKKKKKKK"
      


app.include_router(authentication.router)
app.include_router(books.router)





  
      