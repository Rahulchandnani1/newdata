import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("No DATABASE_URL set for Flask application")
    
    engine = create_engine(database_url)
    engine.connect()
except OperationalError as e:
    print(f"OperationalError: {e}")
    raise RuntimeError("Failed to connect to the database. Check your DATABASE_URL.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__ = 'register'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phn = Column(String(80), nullable=False)
    dob = Column(String(15), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phn = data.get('phn')
    dob = data.get('dob')

    new_user = Register(name=name, email=email, phn=phn, dob=dob)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Data submitted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
