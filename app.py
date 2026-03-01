from models import db, User, Balance
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,create_access_token, create_refresh_token,jwt_required,get_jwt_identity
import secrets,datetime,os,json
from datetime import timedelta
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash
from decimal import Decimal

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DATABASE_URL",  # this is the environment variable you set in Render
    "sqlite:///app.db"  # fallback for local dev
)

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
        password=(data.get("password"))
        if "@" in email and full_name and full_name!=" " and phone_number and phone_number!=" " and country and country!=" " and password and password!=" ":
            user=User.query.filter_by(email=email).first()
            if user:
                return make_response({"msg":f"{email} is already registered"},400)
            new_user=User(full_name=full_name, email=email, phone_number=phone_number, password=password, country=country)
            db.session.add(new_user)
            db.session.flush()   # 👈 generates new_user.id without committing

        # ✅ Create balance with 0
            balance = Balance(
            user_id=new_user.id,
            balance=0
        )

            db.session.add(balance)
            db.session.commit()
            return make_response(new_user.to_dict(),201)
        return make_response({"msg":"Invalid data entries"},400)
api.add_resource(SignUp,'/signup')

class Login(Resource):
    def post(self):
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        if "@" in email and password:
            user=User.query.filter_by(email=email).first()
            if user:
                if (user.password,password):
                    access_token=create_access_token(identity=user.id)
                    refresh_token=create_refresh_token(identity=user.id)
                    return make_response({"user":user.to_dict(),"access_token":access_token,"refresh_token":refresh_token},200)
                return make_response({"msg":"Incorrect password"},400)
            return make_response({"msg":"email not registered"},404)
        return make_response({"msg":"Invalid data"})
api.add_resource(Login,'/login')


class Get_users(Resource):
    def get(self):
        users=User.query.all()
        return make_response([user.to_dict() for user in users],200)
api.add_resource(Get_users,"/users")

class Get_user(Resource):
    def get(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            return make_response(user.to_dict(),200)
        return make_response({"msg":"user not found"},404)
    
    def patch(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            data=request.get_json()
            for attr in data:
                if attr in ['full_name','email','role','country','phone_number']:
                    setattr(user,attr,data.get(attr))
                    
                if "password" in data:
                    user.password=generate_password_hash(data['password'])
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict(),200)
        return make_response({"msg":"user not found"})
    
    def delete(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({"msg":f"user{user} deleted successfully"})
        return make_response({"msg":f"user {user} not found"})
    
api.add_resource(Get_user,'/user/<int:id>')

class GetBalance(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)

        if not user.balance:
            return {
                "user_id": user.id,
                "balance": "0.00"
            }, 200

        return {
            "user_id": user.id,
            "balance": str(user.balance.balance)
        }, 200
        
    def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        if not user.balance:
            return {"message": "Balance not found"}, 404

        data = request.get_json()
        amount = Decimal(data.get("amount", 0))

        if amount == 0:
            return {"message": "Amount must not be zero"}, 400

        # Convert existing balance to Decimal
        balance_amount = Decimal(user.balance.balance)

        # Prevent negative balance
        if balance_amount + amount < 0:
            return {"message": "Insufficient balance"}, 400

        # Update balance
        user.balance.balance = balance_amount + amount
        db.session.commit()

        return {
            "message": "Balance updated successfully",
            "balance": str(user.balance.balance)
        }, 200
        
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        if not user.balance:
            return {"message": "Balance not found"}, 404

        db.session.delete(user.balance)
        db.session.commit()

        return {"message": "Balance deleted successfully"}, 200

api.add_resource(GetBalance,'/users/<int:user_id>/balance')



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)