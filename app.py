"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "this-is-a-secret-key"
app.config['DEBUG-TB-INTERCEPT_REDIRECTS'] = False

app.debug = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes =[cupcake.serialized() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)
    
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_a_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialized())

@app.route('/api/cupcakes', methods=['POST'])
def create_a_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake=new_cupcake.serialized())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def patch_a_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor',cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialized())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_a_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

@app.route('/')
def show_cupcakes_list():
    return render_template('add_cupcake_form.html')