
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token ,jwt_required , get_jwt , get_jwt_identity , create_refresh_token

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("users" , __name__ , description ="operations on users")

@blp.route("/user/register")

class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data):
        # check for unique user name if not send it back :)
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()


        if user:
            abort(500 , message ="username exst try logging in ")

        user = UserModel(username = user_data["username"] , password =pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()
        return {"message":"user created " } ,201
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200 , UserSchema)
    def get(self , user_id ):
        user = UserModel.query.get_or_404(user_id)
        return user
    def delete(self , user_id):

        user = UserModel.query.get_or_404(user_id)

        if not user:
            return {"message":"No such user found already deleted "}
        
        db.session.delete(user)
        db.session.commit()
        return {"message":"user deleted sucessfully  "}

@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data ):
        user = UserModel.query.filter(UserModel.username==user_data["username"]).first()

        if not user :
            abort(404 , message ="no user found check username")
        
        # return {"user":user.password}
        if user and pbkdf2_sha256.verify( user_data["password"] , user.password):
            # generate token and return 
            access_token = create_access_token(identity=str(user.id) , fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token":access_token , "refresh_token":refresh_token} 
        
        abort(401 , message ="Invalid credentials")
            


        # check if user exist 
        # generate acess token 
        # return token 

@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self ):
        jti = get_jwt()['jti'] 
        BLOCKLIST.add(jti)
        return {"message":"logged out sucessfully "}


@blp.route("/user/refresh")

class TokenRefresh(MethodView):

    @jwt_required(refresh=True) 
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity= current_user , fresh=False)
        return {"access_token":new_token}
    
