import base64
import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# --- Configuration ---
FLAG     = os.environ.get("JWT_FLAG")
SECRET   = os.environ.get("JWT_SECRET_KEY")
USERNAME = os.environ.get("AUTH_USERNAME")
PASSWORD = os.environ.get("AUTH_PASSWORD")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# POST /token
# Input:  username + password (form data)
# Output: JWT token with the flag embedded in its payload
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != USERNAME or form_data.password != PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = jwt.encode(
        {
            "sub":  form_data.username,
            "exp":  datetime.utcnow() + timedelta(minutes=30),
            "flag": base64.b64encode(FLAG.encode()).decode(),  # encoding != encryption!
            "hint": "encoded != encrypted",
        },
        SECRET,
    )
    return {"access_token": token, "token_type": "bearer"}


# GET /protected
# Input:  Bearer <token> in Authorization header
# Output: protected message if token is valid, 401 otherwise
@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return {"message": "You have access to protected resource"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("SERVER_PORT", "8000")))
