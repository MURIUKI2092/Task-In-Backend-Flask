from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
import re
import validators
from flask_login import login_required
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from src.database import User,db
regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
auth= Blueprint("auths",__name__,url_prefix="/api/v1/auth")

@auth.post("/register")
def User_register():
    username= request.json["username"]
    email=request.json['email']
    role=request.json.get("role"," ")
    password=request.json['password']
    
    if len(password)<6:
        return jsonify({
            "message":"The password length is short"
            
        }),400
        
    if len(username)<3:
        return jsonify({
            "message":"username is too short"
        }),400
    if not role:
        return jsonify({
            "message":"The user role must be added while registering"
        })
   
        
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
        access = create_access_token(identity=user.id) #create an access token
        
        
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
    
    
#get all the users if and only if you're an admin
@auth.get("/users")

# @jwt_required() #secure the route
def get_all_users():
    try:
        return jsonify({
            "users":User
        })
        
    except:
        return jsonify({
            "message":"There was an error fetching your data from the database"
        })
     
#get a single user by using either the email or the username   
@auth.get('/users/<int:userId>')
# @jwt_required()

def get_single_user(userId):
    try:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        user = User.query.filter_by(id=userId).first()
        print(user)
        print(user)
        if not user:
            return jsonify({
                "message":"The user with those credentials was not found"
            })
        else:
            return jsonify({
                "user":{
                    'username':user.username,
                    'email':user.email,
                    'role':user.role
                }
            }),200
            
    except:
        return jsonify({
            "message":"There was an error querying your user"
        }),400
   

#This method is for deleting all the users from the system
#only the admin is required to do this task
@auth.delete("/users/delete")
@jwt_required()
@login_required

def delete_all_users():
    current_user = get_jwt_identity()
    if current_user.role =="Admin":
        try:
            
            all_users_to_delete= User.query.all()
            if  not all_users_to_delete:
                return jsonify({
                    "message":"There are no users present to perform this task"
                })
            else:
                User.session.delete(all_users_to_delete)
                User.session.commit()
                
                return jsonify ({}),204
            
        except:
            return jsonify({
                "message":"an error occurred while deleting all the user"
            })
    
    else:
        return jsonify({
            "message":"You are not allowed to do that as you're not an admin"
        })
    
@auth.delete("/users/delete/<params>")
@jwt_required()
@login_required

def delete_single_user(params):
    # current_user= get_jwt_identity()
    # if current_user.role =="Admin":
        try:
            
            if validators.email(params):
                user_to_delete= User.query.filter_by(email=params)
            else:
                user_to_delete = User.query.filter_by(username=params)
            if not user_to_delete:
                return jsonify({
                    "message":"The user with that parameter was not found"
                }),404
                
            else:
                User.session.delete(user_to_delete)
                User.session.commit()
                
                return jsonify({}),204
            
        except:
            return jsonify({
                "message":"an error occurred during deleting the single user"
            }),400
    # else:
    #     return jsonify({
    #         "message":"You are not authorized to do that."
    #     })
            

@auth.put("/user/update/<params>")
@auth.patch("/users/update/<params>")  
@login_required
@jwt_required()

def update_single_user(params):
    pass
         