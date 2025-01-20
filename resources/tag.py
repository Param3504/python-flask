import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint ,abort
from db import db
from sqlalchemy.exc import SQLAlchemyError , IntegrityError

from models import TagModel , StoreModel ,ItemModel
from schemas import TagSchema , TagAndItemSchema

blp = Blueprint("Tags",__name__,description ="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200 , TagSchema(many=True))
    def get(self , store_id):
      
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()
    
        # store = StoreModel.query.get_or_404(store_id )
        # # raise NameError("error aa rha h ")
        # print("in here tagsi n store")
        # return {"message":"passed"} #as tags are dunamic and need to return .all to get the list 
    # need to remember one thing in blueprint we get the request body only when we check for the request body and if we  are sending response and checking for repsonse only we donot get the rreq body
    
    @blp.arguments(TagSchema)
    @blp.response(201 , TagSchema)
    def post(self , tag_data  , store_id):
        # if(TagModel.query.get(tag_data["name"]) and TagModel.query.get(tag_data[store_id])):
        #     return{"message":"THIS TAG ALREADY EXIT IN THIS STORE "}
        # ABOVE METHOD IS LITTLE LENGTHY WILL TRY DOING DIRECTLY USING SQLA
        
        # AS WE USED UNIQUE = TRUE IN MODEL SO NO ENED TO CHECK HERE 

        # if(TagModel.query.filter(TagModel.store_id==store_id , TagModel.name== tag_data["name"]).first()):
            # abort(500 , message ="this tag already exist in this shop :)")
        tag= TagModel(**tag_data , store_id =store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500 , message =str(e))
        
        return tag
    

@blp.route("/tag/<string:tag_id>")
class Tags(MethodView):
    @blp.response(200 , TagSchema)
    def get(self , tag_id):
        return TagModel.query.get_or_404(tag_id)
    
    @blp.response(202 , description="deelte a tag if no item is tagged with it " , example={"message":"tag deleted"})
    @blp.alt_response(404 , description="Tag not found")
    @blp.alt_response(400 , description="multiple tag not deleted")
    def delete(sel , tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"messsage":"deleted tag "}
        abort(400 ,message="multiple tag found so not deleting ")

    
    
@blp.route("/tag/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(200 , TagSchema)
    def post(self , item_id , tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500 , message="errror in addding tags")
        return tag
    @blp.response(200 , TagAndItemSchema)
    def delete(self , item_id , tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except:
            abort(500 , messsage ="error occured " ,)
        
        return {"message":"item removed from tag","item":item,"tag":tag}
        
