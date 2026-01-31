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

class SignUp(Resource):
    def post(self):
        data=request.get_json()
        full_name=data.get("full_name")
        email=data.get("email")
        phone_number=data.get("phone_number")
        country=data.get("country")
        password=generate_password_hash(data.get("password"))
        if "@" in email and full_name and full_name!=" " and phone_number and phone_number!=" " and country and country!=" " and password and password!=" ":
            user=User.query.filter_by(email=email).first()
            if user:
                return make_response({"msg":f"{email} is already registered"},400)
            new_user=User(full_name=full_name, email=email, phone_number=phone_number, password=password, country=country)
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(),201)
        return make_response({"msg":"Invalid data entries"},400)
api.add_resource(SignUp,'/signup')




if __name__=="__main__":
    app.run(debug=True)