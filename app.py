from flask import Flask , request
from database import Description, SessionFactoryPool
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

current_session = None
db_session = SessionFactoryPool.create_new_session()


class todolist(Resource):
    def get(self):
        res = db_session.query(Description).all()
        l = []
        if res is None:
            return {"Success": False}, 200
        for i in res:
            l.append({"id": i.id ,"name": i.name, "description": i.description})

        return l

    def post(self):
        name = request.json['name']
        title = request.json['title']
        desc = Description(name, title)
        db_session.add(desc)
        db_session.commit()
        return {"Success": True}


class todolists(Resource):
    def get(self, id):
        res = db_session.query(Description).get(id)
        if res is None:
            return {"Success": False}, 200
        return {"id": res.id ,"name": res.name, "description": res.description}

    def delete(self, id):
        res = db_session.query(Description).filter(Description.id == id).first()
        if res is None:
            return {"Success": False}, 200
        db_session.delete(res)
        db_session.commit()
        return  {"Success" : True}

api.add_resource(todolist,'/')
api.add_resource(todolists, '/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
