import os
os.environ["TESTING"] = "TRUE"

from unittest import TestCase
from app import app
from models import db, Cupcake, connect_db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

connect_db(app)

with app.app_context():
  db.drop_all()
  db.create_all()


CUPCAKE_DATA = {
  "flavor": "TestFlavor",
  "size": "TestSize",
  "rating": 5,
  "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
  "flavor": "TestFlavor2",
  "size": "TestSize2",
  "rating": 10,
  "image": "http://test.com/cupcake2.jpg"
}

CUPCAKE_DATA_3 = {
  "flavor": "TestPatch1",
  "size": "TestPatchSize",
  "rating": 1,
  "image": ""
}


class CupcakeViewsTestCase(TestCase):
  """Tests for views of API."""

  def setUp(self):
    """Make demo data."""
    with app.app_context():
      db.create_all()

      cupcake = Cupcake(**CUPCAKE_DATA)
      db.session.add(cupcake)
      db.session.commit()

      self.cupcake_id = cupcake.id

  def tearDown(self):
    """Clean up fouled transactions."""
    with app.app_context():
      db.session.rollback()
      db.drop_all()

  def test_list_cupcakes(self):
    with app.test_client() as client:
      resp = client.get("/api/cupcakes")

      self.assertEqual(resp.status_code, 200)

      data = resp.json
      self.assertEqual(data, {
        "cupcakes": [
          {
            "id": self.cupcake_id,
            "flavor": "TestFlavor",
            "size": "TestSize",
            "rating": 5,
            "image": "http://test.com/cupcake.jpg"
          }
        ]
      })

  def test_get_cupcake(self):
    with app.test_client() as client:
      url = f"/api/cupcakes/{self.cupcake_id}"
      resp = client.get(url)

      self.assertEqual(resp.status_code, 200)
      data = resp.json
      self.assertEqual(data, {
        "cupcake": {
          "id": self.cupcake_id,
          "flavor": "TestFlavor",
          "size": "TestSize",
          "rating": 5,
          "image": "http://test.com/cupcake.jpg"
        }
      })

  def test_create_cupcake(self):
    with app.test_client() as client:
      url = "/api/cupcakes"
      resp = client.post(url, json=CUPCAKE_DATA_2)

      self.assertEqual(resp.status_code, 201)

      data = resp.json

      # don't know what ID we'll get, make sure it's an int & normalize
      self.assertIsInstance(data['cupcake']['id'], int)
      del data['cupcake']['id']

      self.assertEqual(data, {
        "cupcake": {
          "flavor": "TestFlavor2",
          "size": "TestSize2",
          "rating": 10,
          "image": "http://test.com/cupcake2.jpg"
        }
      })
  
  def test_update_cupcake(self):
    with app.test_client() as client:
      url = f"/api/cupcakes/{self.cupcake_id}"
      resp = client.patch(url, json=CUPCAKE_DATA_3)

      self.assertEqual(resp.status_code, 200)

      data = resp.json

      self.assertEqual(data, {
        "cupcake": {
          "id": self.cupcake_id,
          "flavor": "TestPatch1",
          "size": "TestPatchSize",
          "rating": 1.0,
          "image": ""
        }
      })

  def test_delete_cupcake(self):
    with app.test_client() as client:
      url = f"/api/cupcakes/{self.cupcake_id}"
      resp = client.delete(url)

      self.assertEqual(resp.status_code, 200)
      self.assertEqual(len(Cupcake.query.all()), 0)

      data = resp.json

      self.assertEqual(data, {"message":"Deleted."})
