from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi_pagination import Page, add_pagination
from . import models
from .database import engine

from fastapi.security import OAuth2PasswordBearer
from .controllers import auth_controller, character_controller


import logging
from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
# setup loggers
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)# type: ignore[attr-defined]

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.



Page = Page.with_custom_options(# type: ignore[misc]
    size=Query(default=25, ge=1, le=100),
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

add_pagination(app)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_controller.router)
app.include_router(character_controller.router)

@app.get("/token/")
async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


