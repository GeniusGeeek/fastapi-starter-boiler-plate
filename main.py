from fastapi import FastAPI

from controller_routes import example_of_authenticated_route, example_of_using_utils, signup, signin, forget_password, reset_password, user_account
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FASTAPI STARTER BOILER PLATE")

app.include_router(signup.router)
app.include_router(signin.router)
app.include_router(example_of_authenticated_route.router)
app.include_router(forget_password.router)
app.include_router(reset_password.router)
app.include_router(example_of_using_utils.router)
app.include_router(user_account.router)







origins = [
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
  return{"welcome to FAST API Boiler Plate"}
