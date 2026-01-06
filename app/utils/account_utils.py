from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User, RefreshToken
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import uuid
from sqlalchemy import select
from typing import Optional

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Security ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Helpers ---
def create_access_tokens(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        # Hamesha algorithms ko list mein pass karein security ke liye
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# --- Token Management Logic ---
async def create_tokens(session: AsyncSession, user: User):
    # Access token payload mein 'type' add karna security best practice hai
    access_token = create_access_tokens(data={"sub": str(user.id), "type": "access"})
    refresh_token_str = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=expires_at,
        revoked=False 
    )

    try:
        session.add(refresh_token)
        await session.commit()
        await session.refresh(refresh_token)
    except Exception as e:
        await session.rollback()
        raise e

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }

async def verify_refresh_token(session: AsyncSession, token: str) -> Optional[User]:
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token and not db_token.revoked:
        expires_at = db_token.expires_at
        # Ensure timezone awareness
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at > datetime.now(timezone.utc):
            user_stmt = select(User).where(User.id == db_token.user_id)
            user_result = await session.execute(user_stmt)
            return user_result.scalar_one_or_none()
    
    return None

async def revoke_refresh_token(session: AsyncSession, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token:
        db_token.revoked = True
        try:
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            return False
    return False

# --- Utility Functions ---
def create_email_verification_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"sub": str(user_id), "type": "verify", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_password_reset_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"sub": str(user_id), "type": "reset", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token_and_get_user_id(token: str, token_type: str) -> Optional[int]:
    payload = decode_token(token)
    if not payload or payload.get("type") != token_type:
        return None
    sub = payload.get("sub")
    return int(sub) if sub else None

async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()