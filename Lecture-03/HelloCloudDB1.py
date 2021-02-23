from flask import Flask, request, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Init app
app = Flask(__name__)

#Database
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webadmin:XCVmpe99066@node8581-advweb-13.app.ruk-com.cloud:11099/CloudDB"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webadmin:XCVmpe99066@10.100.2.177:5432/CloudDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

#Staff Class/Model
class Product(db.Model):
    id_prodocut = db.Column(db.String(13), primary_key=True, unique=True)
    name_product = db.Column(db.String(50))
    price = db.Column(db.String(50))
    id_type = db.Column(db.String(13) ,db.ForeignKey('id_type'))
    
    def __init__(self, id_prodocut, name_product, price, id_type):
        self.id_prodocut = id_prodocut
        self.name_product = name_product
        self.price = price
        self.id_type = id_type

class Type(db.Model):
    id_type = db.Column(db.String(13), primary_key=True, unique=True)
    name_type = db.Column(db.String(50))
    id_company = db.Column(db.String(13))

    def __init__(self, id_type, name_type, id_company):
        self.id_type = id_type
        self.name_type = name_type
        self.id_company = id_company

# Staff Schema
class StaffSchema(ma.Schema):
    class Meta:
        fields =('id_prodocut', 'name_product', 'price', 'id_type')

# Init Schema 
staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

# Get All Staffs
@app.route('/product', methods=['GET'])
def get_staffs():
    all_staffs = Product.query.all()
    result = staffs_schema.dump(all_staffs)
    return jsonify(result)

# # Get Single Staff
# @app.route('/product/<id>', methods=['GET'])
# def get_staff(id):
#     staff = Product.query.get(id)
#     return staff_schema.jsonify(staff)

# # Create a Staff
# @app.route('/product', methods=['POST'])
# def add_staff():
#     id_prodocut = request.json['id_prodocut']
#     name_product = request.json['name_product']
#     price = request.json['price']
#     id_type = request.json['id_type']

#     new_staff = Product(id_prodocut, name_product, price, id_type)

#     db.session.add(new_staff)
#     db.session.commit()

#     return staff_schema.jsonify(new_staff)

# # Update a Staff
# @app.route('/product/<id>', methods=['PUT'])
# def update_staff(id):
#     staff = Product.query.get(id)
    
#     name_product = request.json['name_product']
#     price = request.json['price']
#     id_type = request.json['id_type']

#     staff.name_product = name_product
#     staff.price = price
#     staff.id_type = id_type

#     db.session.commit()

#     return staff_schema.jsonify(staff)

# # Delete Staff
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_staff(id):
#     staff = Product.query.get(id)
#     db.session.delete(staff)
#     db.session.commit()
    
#     return staff_schema.jsonify(staff)


# Web Root Hello
@app.route('/', methods=['GET'])
def get():
    query = session.query(
       Product.id_prodocut, 
       Product.name_product, 
       Type.id_type,
       Type.name_type, 
    )
    join_query = query.join(Product).join(Type)

    return join_query.filter(Product.id_type  == Type.id_type).all()

    

# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)