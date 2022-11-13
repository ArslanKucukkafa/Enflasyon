from fastapi import FastAPI
from config import engine
import model
import router
from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]



# generate model to table postgresql
model.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(router.router)

