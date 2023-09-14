import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_PATH = os.path.join(os.getcwd(), 'data.db')
# Configure the database location, in this case, we're using SQLite for simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH

# Initialize the database with the Flask app
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def home():
    return "Hello, World"


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        output_data = {'name':drink.name, 'description':drink.description}
        output.append(output_data)

    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name":drink.name, "description":drink.description }

@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()

    return {'id':drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error":"drink not available"}
    
    db.session.add(drink)
    db.session.commit()

    return {'message':'Yay'}