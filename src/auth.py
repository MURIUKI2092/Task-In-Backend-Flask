from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
import re
import validators
from flask_jwt_extended import create_access_token,create_refresh_token
from src.database import User,db
regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
auth= Blueprint("auths",__name__,url_prefix="/api/v1/auth")

@auth.post("/register")
def User_register():
    username= request.json["username"]
    email=request.json['email']
    password=request.json['password']
    
    if len(password)<6:
        return jsonify({
            "message":"The password length is short"
            
        }),400
        
    if len(username)<3:
        return jsonify({
            "message":"username is too short"
        }),400
    # if not username.isalnum() or " ":
    #     return jsonify({
    #         "message":"username should be alphanumeric"
    #     }),400
        
    if not re.fullmatch(regex,email):
        return jsonify({
            "message":"The email is not a valid email. check it out"
        }),400
        
    if User.query.filter_by(email = email).first() is not None:
        return jsonify({
            "message":"The user with that email exist in our Db. Kindly change the Email"
        }),409
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "message":"The username is already taken. choose another one"
        }),409
        
    hashed_password= generate_password_hash(password)
    
    user=User(username=username, password=hashed_password,email=email)
    db.session.add(user)
    db.session.commit()
    
    
        
    
    return jsonify({"message": "The user has been added successfully",
                    'user':{
                        'username':username, 'email':email
                    }
                    })
#login route
@auth.post("/login")
def User_login():
    body=request.json.get("body", " ") #obtain the body from the frontend
    password=request.json['password'] #obtain the password
    
    if validators.email(body): #check whether the userlogged in using their registered email address
        user=User.query.filter_by(email=body).first() # if so query db for the user
        
    else:
        user=User.query.filter_by(username=body).first() #else query the db using the db name
        
    if not user: # if no user was found return this message
        return jsonify({
            "message":"The user with those credentials was not found in the database"
        })
    
    is_password_correct=check_password_hash(user.password,password) # if user exists, then check the provided password  with the hashed password
    
    if is_password_correct: # if password is correct
        refresh = create_refresh_token(identity=user.id) #create a refresh token
        access = create_refresh_token(identity=user.id) #create an access token
        
        
        return jsonify({ # return the user object
            'user':{
                'refresh':refresh,
                'access':access,
                'username':user.username,
                'email':user.email
            }
        }),200
        
    return jsonify({ # if the password was wrong return this message
        "message":"Wrong password was provided"
    }),401
    
    
