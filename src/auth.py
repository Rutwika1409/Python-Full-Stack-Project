import os
from supabase import create_client
from src.logic import UserLogic

class AuthLogic:
    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.user_logic = UserLogic()
    
    def sign_up(self, email, password, name):
        try:
            # Create user in Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Create user profile in your users table
                user_result = self.user_logic.create_user(email, name)
                return user_result
            return {"Success": False, "message": "Failed to create user"}
        except Exception as e:
            return {"Success": False, "message": str(e)}
    
    def sign_in(self, email, password):
        try:
            result = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"Success": True, "user": result.user}
        except Exception as e:
            return {"Success": False, "message": str(e)}