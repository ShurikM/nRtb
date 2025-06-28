# shared/auth.py

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import uuid

# Replace with Redis or DB later
VALID_SESSION_IDS = {"nissim-rtb"}
VALID_USERS = {"admin": "nissim123"}
DEV_SESSION_ID = "dev-secret-session-id"  # any long, hardcoded string
SESSION_COOKIE_NAME = "session_id"


def verify_session(request: Request):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id == DEV_SESSION_ID:
        return  # always allow this

    if not session_id or session_id not in VALID_SESSION_IDS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing session")


def create_session_cookie_for_user(username: str) -> JSONResponse:
    if username not in VALID_USERS:
        raise HTTPException(status_code=401, detail="Unknown user")

    session_id = f"{username}-{uuid.uuid4()}"
    VALID_SESSION_IDS.add(session_id)

    response = JSONResponse(content={"message": f"Logged in as {username}"})
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_id, httponly=True)
    return response


def validate_credentials(username: str, password: str) -> bool:
    return VALID_USERS.get(username) == password
