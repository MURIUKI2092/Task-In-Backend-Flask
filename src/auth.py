from flask import Blueprint

auth= Blueprint("auth",__name__,"/api/v1/auth")

@auth.post("/register")
def User_register():
    return "User created"

@auth.get("/me")
def User_login():
    return "user logged in sucessfully"