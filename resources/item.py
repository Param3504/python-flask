
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from schemas import ItemSchema, ItemUpdateSchema , StoreSchema
from flask_jwt_extended import jwt_required , get_jwt
blp = Blueprint("item" , __name__ , description ="operations on item")


@blp.route("/item/<string:id>")
class item(MethodView):
    @jwt_required()
    @blp.response(200 , ItemSchema) 
    def get(self , id):
        item = ItemModel.query.get_or_404(id)
        return item
    @jwt_required()
    def delete(self ,id ): 
        item = ItemModel.query.get_or_404(id)
        jwt =get_jwt()
        if not jwt.get("is_admin"):
            abort(401 , message ="admin privelege required")
        db.session.delete(item)
        db.session.commit() #without this nothing adds or deleted neither updates
        return {"message":"Item deleted succesfully"}
      
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200 , ItemSchema)
    def put(self ,request_body ,id):
        item = ItemModel.query.get(id)
        # if item not exist then we create on e item and then push it to db 

        if item:
            item.price= request_body["price"]
            item.name= request_body["name"]
        else: 
            item = ItemModel(id = id ,**request_body)
        
        db.session.add(item) 
        db.session.commit()
        return item
    
        
        

        
@blp.route("/item")
class item_list(MethodView):
    @jwt_required()
    @blp.response(200 ,ItemSchema(many=True))
    def get(self):
        item = ItemModel.query.all()
        return item
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201  ,ItemSchema)
    def post(self , item_data):
        item =  ItemModel(**item_data)
        try:
           db.session.add(item)#just add to the database but it doesnot get inserted to table u van add multiple rows at once and commit all at once :)
           db.session.commit()
        except SQLAlchemyError:
            abort(500 , message =" an error occured while inserting ")
        
        return item




 

