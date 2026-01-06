from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import User
from app.db.config import sessionDep
from app.schemas.account_schemas import UserOut, UserCreate, PasswordChangeRequest # Maan lete hain ye schemas hain
from app.utils.account_utils import create_tokens, verify_refresh_token, revoke_refresh_token
from app.dependencies.account_dependencies import get_current_user, require_admin
from app.services.services import (
    create_user, authenticate_user, change_password, 
    process_password_reset, reset_password_with_token
)

router = APIRouter(prefix="/account", tags=["Account"])

# --- Helper function for Cookies ---
def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # HTTPS par hi chalega
        samesite="Lax",
        max_age=60 * 60 * 24 * 7  # 7 days
    )

@router.post("/register", response_model=UserOut)
async def register(session: sessionDep, user: UserCreate):
    return await create_user(session, user)

@router.post("/login")
async def login(session: sessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = await create_tokens(session, user)
    
    # Refresh token cookie mein aur Access token body mein
    response = JSONResponse(content={"access_token": tokens["access_token"], "token_type": "bearer"})
    set_refresh_cookie(response, tokens["refresh_token"])
    return response

@router.post("/refresh")
async def refresh_token(session: sessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    user = await verify_refresh_token(session, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Purana token revoke karke naya dena behtar rehta hai (Token Rotation)
    await revoke_refresh_token(session, token)
    new_tokens = await create_tokens(session, user)
    
    response = JSONResponse(content={"access_token": new_tokens["access_token"], "token_type": "bearer"})
    set_refresh_cookie(response, new_tokens["refresh_token"])
    return response

@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return user

@router.post("/change-password")
async def password_change(
    session: sessionDep, 
    data: PasswordChangeRequest, # String ki jagah Schema use karein
    user: User = Depends(get_current_user)
):
    await change_password(session, user, data.new_password)
    return {"msg": "Password changed successfully"}

@router.post("/forgot-password")
async def forgot_password(session: sessionDep, email: str):
    # Isme email verify karke reset link bhejne ka logic hona chahiye
    return await process_password_reset(session, email)

@router.post("/reset-password")
async def reset_password(session: sessionDep, token: str, new_password: str):
    return await reset_password_with_token(session, token, new_password)

@router.post("/logout")
async def logout(session: sessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if token:
        await revoke_refresh_token(session, token)
    
    response = JSONResponse(content={"detail": "Logged out successfully"})
    response.delete_cookie("refresh_token")
    return response

@router.get("/admin")
async def admin(user: User = Depends(require_admin)):
    return {"msg": f"Welcome Admin {user.name}"}