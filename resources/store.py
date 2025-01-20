import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint ,abort
from db import db
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
blp = Blueprint("store" , __name__ , description ="operations on store")

@blp.route("/store/<string:id>")
class store(MethodView):
    @blp.response(200 , StoreSchema)
    def get(self , id ):   
        store = StoreModel.query.get_or_404(id)
        return store
    
    def delete(self , id):
        store = StoreModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"item deleted succesfully"}
@blp.route("/store")

class store_list(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        store  = StoreModel.query.all()
        return store
    @blp.arguments(StoreSchema)
    @blp.response(200 ,StoreSchema)
    def post(self , request_data):
        store = StoreModel(**request_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500 , message ="same name store already exist")
        except SQLAlchemyError:
            abort(500 , message ="some error occured")

        return store
    
            

        