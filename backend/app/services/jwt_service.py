from app.core.security import create_access_token

def build_token_for_user(user_email: str):
    token = create_access_token({"sub": user_email})
    return token
