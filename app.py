"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake, DEFAULT_IMAGE
# from forms import AddPetForm, EditPetForm
from secret import SECRET_KEY
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

def get_request_data(json):
  image = json["image"]
  if image == None or image == "":
    image = DEFAULT_IMAGE
  return json["flavor"], json["size"], json["rating"], image

@app.route("/")
def homepage():
  return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
  """Returns JSON object showing all cupcakes"""
  cupcakes = Cupcake.query.all()
  cupcake_data = [cupcake.serialize() for cupcake in cupcakes]
  return jsonify(cupcakes=cupcake_data)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
  """
  Create cupcake with data from the body of the request.
  Responds with JSON like: {cupcake:{id, flavor, size, rating, image}}
  """
  flavor, size, rating, image = get_request_data(request.json)

  new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
  db.session.add(new_cupcake)
  db.session.commit()
  
  response_json = jsonify(cupcake=new_cupcake.serialize())
  return (response_json, 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
  """Returns JSON object of singular cupcake. 404 if not found"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
  """Updates cupcake. 404 if not found. Returns JSON of updated cupcake."""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  flavor, size, rating, image = get_request_data(request.json)
  cupcake.flavor, cupcake.size, cupcake.rating, cupcake.image = flavor, size, rating, image
  return jsonify(cupcake=cupcake.serialize())

if os.environ.get("TESTING") is None:
  connect_db(app)