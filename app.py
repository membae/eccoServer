from models import db, User
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,create_access_token, create_refresh_token,jwt_required,get_jwt_identity
import secrets,datetime,os,json
from datetime import timedelta
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)


migrate = Migrate(app, db)

db.init_app(app)
api=Api(app)
jwt=JWTManager(app)



class Home(Resource):
    def get(self):
        return make_response({"msg":"Homepage here"},200)
api.add_resource(Home,'/')




if __name__=="__main__":
    app.run(debug=True)