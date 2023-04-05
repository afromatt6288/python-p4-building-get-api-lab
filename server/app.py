#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods = ['GET','POST'])
def bakeries():
    if request.method == 'GET':
        all_bakeries = Bakery.query.all()
        return_obj = []
        if all_bakeries:
            for bakery in all_bakeries:
                return_obj.append(bakery.to_dict())
            res = make_response(jsonify(return_obj),200)
            return res
        else:
            return_obj = {
                "valid": False,
                "Reason": "Can't query data"
            }
            res = make_response(return_obj,500)
            return res
    elif request.method == 'POST':
        newBakery = Bakery(
            name = request.form.get("name"),
        )
        if newBakery.name != None:
            db.session.add(newBakery)
            db.session.commit()
            all_bakeries = Bakery.query.all()
            new_bakery = all_bakeries[-1]
            res = make_response(jsonify(new_bakery.to_dict()),201)
            return res
        else:
            return_obj = {
                "valid": False,
                "Reason": "Did not input name"
            }
            res = make_response(return_obj,500)
            return res
## Their solution... simpler and less fluff ##
# @app.route('/bakeries')
# def bakeries():

#     bakeries = Bakery.query.all()
#     bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

#     response = make_response(
#         jsonify(bakeries_serialized),
#         200
#     )
#     response.headers['Content-Type'] = 'application/json'
#     return response

@app.route('/bakeries/<int:id>', methods = ['GET','PATCH', 'DELETE'])
def bakery_by_id(id):
    id_bakery = Bakery.query.filter(Bakery.id == id).first()
    if id_bakery:
        if request.method == 'GET':
            res = make_response(jsonify(id_bakery.to_dict()),200)
            return res
        elif request.method == 'PATCH':
            for attr in request.form:
               setattr(id_bakery, attr, request.form.get(attr))
            db.session.add(id_bakery)
            db.session.commit()
            res = make_response(jsonify(id_bakery.to_dict()),200)
            return res
        elif request.method == 'DELETE':
            db.session.delete(id_bakery)
            db.session.commit()
            return_obj = {
                "valid": True,
                "Reason": "Deleted"
            }
            res = make_response(return_obj,500)
            return res
    else:
        return_obj = {
            "valid": False,
            "Reason": "Not valid id"
        }
        res = make_response(return_obj,500)
        return res

## Their solution... simpler and less fluff ##
# @app.route('/bakeries/<int:id>')
# def bakery_by_id(id):

#     bakery = Bakery.query.filter_by(id=id).first()
#     bakery_serialized = bakery.to_dict()

#     response = make_response(
#         jsonify(bakery_serialized),
#         200
#     )
#     response.headers['Content-Type'] = 'application/json'
#     return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_good_by_price = BakedGood.query.order_by(BakedGood.price).all()
    for bg in baked_good_by_price:
        if bg:
            if request.method == 'GET':
                res = make_response(jsonify([bg.to_dict()]),200)
                return res
            elif request.method == 'PATCH':
                for attr in request.form:
                    setattr(bg, attr, request.form.get(attr))
                db.session.add(bg)
                db.session.commit()
                res = make_response(jsonify([bg.to_dict()]),200)
                return res
            elif request.method == 'DELETE':
                db.session.delete(bg)
                db.session.commit()
                return_obj = {
                    "valid": True,
                    "Reason": "Deleted"
                }
                res = make_response(return_obj,500)
                return res
        else:
            return_obj = {
                "valid": False,
                "Reason": "Not valid price"
            }
            res = make_response(return_obj,500)
            return res

## Their solution... simpler and less fluff ##
# @app.route('/baked_goods/by_price')
# def baked_goods_by_price():
#     baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
#     baked_goods_by_price_serialized = [
#         bg.to_dict() for bg in baked_goods_by_price
#     ]
    
#     response = make_response(
#         jsonify(baked_goods_by_price_serialized),
#         200
#     )
#     response.headers['Content-Type'] = 'application/json'
#     return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    return most_expensive.to_dict()

## Their solution... more complicated and more fluff ##
# @app.route('/baked_goods/most_expensive')
# def most_expensive_baked_good():
#     most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
#     most_expensive_serialized = most_expensive.to_dict()

#     response = make_response(
#         jsonify(most_expensive_serialized),
#         200
#     )
#     response.headers['Content-Type'] = 'application/json'
#     return response

if __name__ == '__main__':
    app.run(port=555, debug=True)

