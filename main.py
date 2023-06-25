import uvicorn
from app import *

if __name__=='__main__':
    print("hello")
    uvicorn.run("app.ourapp:app", host="127.0.0.1", port=8000, log_level="info")