# --- Imports --- ###
# to use current_user i need to use @jwt_required in order to be imported

from flask_jwt_extended import get_jwt_identity
from flask import Flask, abort
from flask import jsonify
from flask import request
from database import db
from models import (
    User,
    Influencer,
    Sponsor,
    Campaign,
    CampaignRequest
)
from models import Campaign
from flask_mail import Message
from flask import Flask, request, make_response
import csv
import io

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    current_user
)
from flask_cors import CORS
from flask_caching import Cache
from celery.schedules import crontab
from config import LocalDevelopmentConfig
from flask_restful import Resource, Api
import workers

from flask_mail import Mail

# Flask app configuration for MailHog
# http://localhost:8025/


app, api, jwt = None, None, None

# ---- Flask app factory ---- #
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins='http://localhost:5173', supports_credentials=True)
    jwt = JWTManager(app)
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    api = Api(app)
    return app, api, jwt
    



app, api, jwt = create_app()
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "support@ds.study.iitm.ac.in"
mail = Mail(app)
# ------- Celery app ------- #

celery = workers.celery

# Update celery app configurations
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
)
celery.conf.timezone = 'Asia/Kolkata'

cache=Cache(app)

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


# ------- Admin user through code ---#
admin_exist = User.query.filter_by(email="admin@gmail.com").first()
if admin_exist is None:
    user = User(email="admin@gmail.com",
                password=generate_password_hash("123"), role="admin")
    db.session.add(user)
    campaign = Campaign(title="Eco-Friendly Drive", description="Promoting eco-friendly products through influencer collaboration.", end_date=datetime(2024, 12, 31), budget=5000, sponsor=1, visibility=True, influencer=0, proof=0, flagged=False, progress="Pending")
    db.session.add(campaign)
    db.session.flush()
    db.session.commit()

admin_exist = User.query.filter_by(email="influ@gmail.com").first()
if admin_exist is None:
    user = User(email="influ@gmail.com",
                password=generate_password_hash("123"), role="influencer")
    db.session.add(user)
    db.session.flush()
    db.session.commit()

admin_exist = User.query.filter_by(email="spon@gmail.com").first()
if admin_exist is None:
    user = User(email="spon@gmail.com",
                password=generate_password_hash("123"), role="sponsor")
    db.session.add(user)
    db.session.flush()
    db.session.commit()
# ------- My flask-restful api resources will start from here --------#








# ------- The authentication and authorization part will start from here ----#
class login(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        email = data.get("email", None)
        password = data.get("password", None)
        print(email)
        user = User.query.filter_by(email=email).first()
        if user:
            print(user)
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user)
                role=user.role
                print(user.followers)
                fol=user.followers
                if role in ("influ", "influencer"):
                    print(user.followers)
                    response = jsonify(id=user.id, role=user.role,
                                   email=user.email, access_token=access_token,industry=0,platform=user.platform,followers=fol)
                else:
                    response = jsonify(id=user.id, role=user.role,
                                   email=user.email, access_token=access_token,industry=user.industry,platform=0,followers=0)
                print(user)
                return response
            
            return jsonify(error="Authentication failed"), 401
        return jsonify(error="wrong credentials"), 404
    def get(self):
        return "hello"

class AuthUser(Resource):
    @jwt_required()
    def get(self):
        
        if not current_user:
            # if the user doesn't exist or password is wrong, reload the page
            return jsonify({'error': 'wrong credentials'}), 404
        else:
            user_data = {
                'id': current_user.id,
                'role': current_user.role,
                'email': current_user.email,
                # Assuming image is stored as a base64-encoded string
                # 'image': base64.b64encode(current_user.image).decode('utf-8') if current_user.image else None
            }
            return jsonify({'message': 'User login successfully',
                            'resource': user_data}), 200






class Signup(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        user = User.query.filter_by(email=data["email"]).first()
        print(user)
        
        if user:
            return jsonify({'error': 'User already exists'}), 409
        print('nouserfound')
        
        role=data["role"]
        print(role)
        if role=="sponsor":
                print("spon")
                new_user = User(
                    email=data["email"],
                    role=data["role"],
                    password=generate_password_hash(data["password"], method='scrypt'),
                    industry=data["industry"]
                )
        else:
                    print('influencer')
                    new_user = User(
                    email=data["email"],
                    role=data["role"],
                    password=generate_password_hash(data["password"], method='scrypt'),
                    platform=data['platform'],
                    followers=data['followers']
                )
        print(new_user)
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        print(new_user.id)
        admin_exist = User.query.filter_by(email=data["email"]).first()

        
        # Generate a JWT for the newly registered user
        access_token = create_access_token(identity=id)
        print(access_token)
        
        verified_data = {
            "email": data["email"],
            "role": data["role"],
            # "auth-token": access_token
        }
        
        return jsonify({
            'message': 'User registered successfully',
            'data': verified_data
        }), 201



class Logout(Resource):
    def get(self):
        print("We will implement it later")
        return jsonify({'message': "logout successful"}), 200
# --------------- AUTH END HERE ------------------------###








class complete_campaign(Resource):
    def post(self, id):
        proof = request.json.get('proof')  # Assuming proof is sent in JSON body
        if not proof:
            return jsonify({'message': 'Proof is required.'}), 400

        # Fetch the campaign from the database
        print(id)
        print(proof)
        print('###################################################################')
        from models import Campaign
        campaign = Campaign.query.get(id)
        if not campaign:
            return jsonify({'message': 'Campaign not found.'}), 404

        # Update campaign with proof
        
        campaign.proof = proof
        campaign.accep = 3

        print('###################################################################')
        print("ok")
        campaign.progress = 'Completed waiting for confirmation'  # Update status
        db.session.flush()
        db.session.commit()
        print('###################################################################')
        print(campaign.proof)

from sqlalchemy.sql import text  # Import the text function






class CampaignList(Resource):
    def get(self):
        influencer_email = request.headers.get('X-User-Email')
        role=request.headers.get('X-User-role')
        # print(influencer_email)
        # campaign=db.session.execute(
        #     text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        print(role)
        print(influencer_email)
        if role in ["influ", "influencer"]:
            campaign1 = db.session.execute(
                text("""SELECT * FROM campaigns WHERE influencer = :email AND accep = :status"""),
                {'email': influencer_email, 'status': 2}
            ).fetchall()
        else:
                campaign1 = db.session.execute(
                text("""SELECT * FROM campaigns WHERE sponsor = :email"""),
                {'email': influencer_email}
            ).fetchall()
        print(campaign1)

        campaigns_list = []
        for campaign in campaign1:
            camp = {
                'id': campaign.id,
                'title': campaign.title,
                'budget': campaign.budget,
                'description': campaign.description,
                'sponsor': campaign.sponsor,
                'influencer': campaign.influencer,
                'enddate': campaign.end_date if campaign.end_date else None,
            }
            campaigns_list.append(camp)
        print(campaigns_list)
        
        # if role in ["influ", "influencer"]:
        #     print('hi')
        # else:
        #         campaign2 = db.session.execute(
        #         text("""SELECT * FROM campaigns WHERE sponsor = :email AND accep = :status"""),
        #         {'email': influencer_email, 'status': 1}
        #     ).fetchall()
        # campaigns_list1 = []
        # for campaign in campaign2:
        #     camp = {
        #         'id': campaign.id,
        #         'title': campaign.title,
        #         'budget': campaign.budget,
        #         'description': campaign.description,
        #         'sponsor': campaign.sponsor,
        #         'influencer': campaign.influencer,
        #         'enddate': campaign.end_date if campaign.end_date else None,
        #     }
        #     campaigns_list1.append(camp)
        


        # if role in ["influ", "influencer"]:
        #         campaign3 = db.session.execute(
        #         text("""SELECT * FROM campaigns WHERE influencer = :email AND progress = :status"""),
        #         {'email': influencer_email, 'status': "comp"}).fetchall()
        # else:
        #         campaign3 = db.session.execute(
        #         text("""SELECT * FROM campaigns WHERE sponsor = :email AND progress = :status"""),
        #         {'email': influencer_email, 'status': "comp"}
        #     ).fetchall()
        # campaigns_list2 = []
        # for campaign in campaign3:
        #     camp = {
        #         'id': campaign.id,
        #         'title': campaign.title,
        #         'budget': campaign.budget,
        #         'description': campaign.description,
        #         'sponsor': campaign.sponsor,
        #         'influencer': campaign.influencer,
        #         'enddate': campaign.end_date if campaign.end_date else None,
        #     }
        #     campaigns_list2.append(camp)
        

        # if role in ["influ", "influencer"]:
        #         campaign4 = db.session.execute(
        #         text("""SELECT * FROM campaigns WHERE influencer = :email AND progress = :status"""),
        #         {'email': influencer_email, 'status': "conf"}).fetchall()
        # else:
        #         campaign4 = db.session.execute(
        #         text("""SELECT * FROM campaigns WHERE sponsor = :email AND progress = :status"""),
        #         {'email': influencer_email, 'status': "conf"}
        #     ).fetchall()
        # campaigns_list3 = []
        # for campaign in campaign4:
        #     camp = {
        #         'id': campaign.id,
        #         'title': campaign.title,
        #         'budget': campaign.budget,
        #         'description': campaign.description,
        #         'sponsor': campaign.sponsor,
        #         'influencer': campaign.influencer,
        #         'enddate': campaign.end_date if campaign.end_date else None,
        #     }
        #     campaigns_list3.append(camp)
        

        return campaigns_list  #,campaigns_list1,campaigns_list2,campaigns_list3, 200






#campaign that belong ot other influencer
class OtherCampaigns(Resource):
    def post(self):
        # Retrieve influencer's email from the request
        data = request.get_json()
        influencer_email = data.get('email')
        print("23233232332")
        print(influencer_email)
        print("23322222222222")
        if not influencer_email:
            return {"message": "Email is required"}, 400

        # Query to get campaigns that do NOT belong to the influencer
        # campaign=db.session.execute(text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        from models import Campaign
        # new_campaign = Campaign(
        #     title="New Campaign Title",
        #     description="This is a description for the new campaign.",
        #     end_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),  # Example date
        #     budget=5000,
        #     sponsor=1,  # Replace with the correct sponsor id
        #     visibility=True,
        #     influencer=2,  # Replace with the id of the influencer named "iflu"
        #     proof=None,
        #     flagged=False,
        #     accep=False,
        #     progress="Pending"
        # )

        # # Add and commit the new campaign
        # db.session.add(new_campaign)
        # db.session.commit()
        from models import Campaign
        campaigns = Campaign.query.filter(Campaign.influencer != influencer_email).all()
        print("13213212")
        print(campaigns)
        print("312312231123")

            # Serialize campaign data
        campaigns_list = []
        for campaign in campaigns:
                camp = {
                    'id': campaign.id,
                    'title': campaign.title,
                    'budget': campaign.budget,
                    'description': campaign.description,
                    'sponsor': campaign.sponsor,
                    'influencer': campaign.influencer,
                    'end_date': campaign.end_date if campaign.end_date else None,
                }
                campaigns_list.append(camp)

        return jsonify({'campaigns': campaigns_list})

api.add_resource(OtherCampaigns, '/campaigns/others')

class RemoveFlag(Resource):
    def put(self,id):
        print(id)
        print('hi')
        # Assuming the user ID is passed in the request body or as a query parameter
        # data = request.get_json()
        # print(data)
        user = User.query.get(id)   # Adjust how the ID is passed
        print(user)
        if user:
            user.flagged = False  # Assuming 'flagged' is a boolean field
            print(user.flagged)
            db.session.commit()
            return {'message': f'Flag removed from user {user.email}.'}, 200
        else:
            return {'error': 'User not found'}, 404

api.add_resource(RemoveFlag, '/remove/flag/<int:id>')




class Flaguser(Resource):
    def put(self,id):
        print(id)
        print('hi')
        # Assuming the user ID is passed in the request body or as a query parameter
        # data = request.get_json()
        # print(data)
        user = User.query.get(id)   # Adjust how the ID is passed
        print(user)
        if user:
            user.flagged = True  # Assuming 'flagged' is a boolean field
            print(user.flagged)
            db.session.commit()
            return {'message': f'Flag removed from user {user.email}.'}, 200
        else:
            return {'error': 'User not found'}, 404

api.add_resource(Flaguser, '/flag/user/<int:id>')








class DeleteUser(Resource):
    # @jwt_required()
    def delete(self,id):
        print("ind del")
        print(id)
        user = User.query.get(id)  # You may want to adjust how the ID is passed
        print(user)
        if user:
            user.password=322
            print
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user.email} deleted successfully.'}, 200
        else:
            return {'error': 'User not found'}, 404

api.add_resource(DeleteUser, '/delete/user/<int:id>')














class DeleteCampaign(Resource):
    # @jwt_required()
    def delete(self,id):
        print("ind del")
        print(id)
        from models import Campaign
        user = Campaign.query.get(id)  # You may want to adjust how the ID is passed
        print(user)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'campaign deleted'}, 200
        else:
            return {'error': 'User not found'}, 404
api.add_resource(DeleteCampaign, '/delete/campaign/<int:id>')




class FlaggedInfluencers(Resource):
    @jwt_required()
    def get(self):
        try:
            # flagged_influencer = User(
            #     email="influencer@example.com",
            #     password="securepassword",
            #     role="influencer",
            #     flagged=True,
            #     platform="Instagram",
            #     followers=10000,
            #     niche="Fashion"
            # )

            # # Create a flagged Sponsor
            # flagged_sponsor = User(
            #     email="sponsor@example.com",
            #     password="securepassword",
            #     role="sponsor",
            #     flagged=True,
            #     industry="Tech"
            # )

            # # Add to the database session
            # db.session.add(flagged_influencer)
            # db.session.add(flagged_sponsor)

            # # Commit changes
            # db.session.commit()
            
            influencers = db.session.query(User).filter(User.role == 'influencer').all()
            # Filter flagged influencers by combining the two conditions
            flagged_influencers = [
                user for user in influencers if user.flagged
            ]

            if not flagged_influencers:
                return {"message": "No flagged influencers found", "resource": []}, 200

            # Serialize flagged influencer data
            influencers_list = [
                {
                    "id": influencer.id,
                    "email": influencer.email
                }
                for influencer in flagged_influencers
            ]

            return {"message": "Flagged influencers fetched successfully", "resource": influencers_list}, 200
        except Exception as e:
            print(f"Error fetching flagged influencers: {e}")
            return {"message": "An error occurred while fetching flagged influencers"}, 500

api.add_resource(FlaggedInfluencers, '/get/all/flagged/influencers')











class unFlaggedInfluencers(Resource):
    @jwt_required()
    def get(self):
        try:     
            influencers = db.session.query(User).filter(User.role == 'influencer').all()
            print("unflaginflu")
            print(influencers)
            flagged_influencers = [
                user for user in influencers if not user.flagged
            ]
            print(flagged_influencers)

            if not flagged_influencers:
                return {"message": "No flagged influencers found", "resource": []}, 200

            # Serialize flagged influencer data
            influencers_list = [
                {
                    "id": influencer.id,
                    "email": influencer.email,
                    "platform": influencer.platform,
                    "fllowers": influencer.followers
                }
                for influencer in flagged_influencers
            ]
            print(influencers_list)

            return { "resource": influencers_list}, 200
        except Exception as e:
            print(f"Error fetching unflagged influencers: {e}")
            return {"message": "An error occurred while fetching unflagged influencers"}, 500
api.add_resource(unFlaggedInfluencers, '/get/unflagged-influencer')



class FlaggedSponsors(Resource):
    @jwt_required()
    def get(self):
        try:
            # Query all sponsors with the role 'sponsor'
            sponsors = db.session.query(User).filter(User.role == 'sponsor').all()

            # Filter flagged sponsors by combining the conditions
            flagged_sponsors = [
                sponsor for sponsor in sponsors if sponsor.flagged
            ]

            if not flagged_sponsors:
                return {"message": "No flagged sponsors found", "resource": []}, 200

            # Serialize flagged sponsor data
            sponsors_list = [
                {
                    "id": sponsor.id,
                    "email": sponsor.email
                }
                for sponsor in flagged_sponsors
            ]

            return {"message": "Flagged sponsors fetched successfully", "resource": sponsors_list}, 200
        except Exception as e:
            return {"message": "An error occurred while fetching flagged sponsors"}, 500

api.add_resource(FlaggedSponsors, '/get/all/flagged/sponsors')





class unFlaggedSponsors(Resource):
    @jwt_required()
    def get(self):
        try:
            # Query all sponsors with the role 'sponsor'
            sponsors = db.session.query(User).filter(User.role == 'sponsor').all()
            print("unflagspon")
            print(sponsors)

            # Filter flagged sponsors by combining the conditions
            flagged_sponsors = [
                sponsor for sponsor in sponsors if not sponsor.flagged
            ]
            print(flagged_sponsors)

            if not flagged_sponsors:
                return {"message": "No flagged sponsors found", "resource": []}, 200

            # Serialize flagged sponsor data
            sponsors_list = [
                {
                    "id": sponsor.id,
                    "email": sponsor.email,
                    "industry":sponsor.industry
                }
                for sponsor in flagged_sponsors
            ]
            print(sponsors_list)

            return { "resource": sponsors_list}, 200
        except Exception as e:
            print(f"Error fetching unflagged sponsors: {e}")
            return {"message": "An error occurred while fetching unflagged sponsors"}, 500
api.add_resource(unFlaggedSponsors, '/get/unflagged-sponsor')





class AcceptCampaign(Resource):
    def put(self,id):
        print(id)
        data = request.get_json()
        email = data.get('email')
        campaign_id = id

        # Query the campaign and influencer
        from models import Campaign
        campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
         # Get the first matching campaign
        print('hi')
        print(campaign)
        print(email)
        print("12313")

        # Query the influencer using raw SQL
        influencer_result = db.session.execute(
            text("""SELECT * FROM users WHERE email = :email"""),
            {'email': email}
        )
        influencer = influencer_result.fetchone()
        print('bye')
        print(influencer)

        if not campaign or not influencer:
            return jsonify({'message': 'Campaign or Influencer not found'}), 404
        print('ók')

        # Accept the campaign (assign the influencer to the campaign)
        from models import Campaign
        campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
        print(campaign)
        if campaign:
            campaign.influencer = email
            campaign.accep=1
            print(campaign.influencer)
            db.session.commit()
        print(campaign)
        print(campaign.influencer)
        print('ok433')

        # Return the updated campaign
        # campaign_dict = dict(campaign)  # Convert the row to a dictionary

        # Return the updated campaign
        return jsonify(campaign.to_dict())
    
# Register the resource
api.add_resource(AcceptCampaign, '/campaigns/accept/<int:id>')










class AcceptNotification1(Resource):

    def put(self, id):
        # Get the notification ID from the request
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(f"Accepting campaign with ID: {id}")
        
        # Query the notification by ID (assuming it relates to a campaign in the database)
        from models import Campaign
        notification = db.session.query(Campaign).filter_by(id=id).first()

        # Check if the notification exists
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404

        # Accept the campaign (update its status to 2)
        notification.accep = 4  # Setting accep to 2, as per your requirement
        print("#################################################################")
        print(notification)
        db.session.commit()

        # Return the updated notification
        return jsonify({'message': 'Campaign accepted successfully', 'id': notification.id})

# Register the resource
api.add_resource(AcceptNotification1, '/accept/influencerproof/<int:id>')



















class AcceptNotification(Resource):
    def put(self, id):
        # Get the notification ID from the request
        print(f"Accepting campaign with ID: {id}")
        
        # Query the notification by ID (assuming it relates to a campaign in the database)
        from models import Campaign
        notification = db.session.query(Campaign).filter_by(id=id).first()

        # Check if the notification exists
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404

        # Accept the campaign (update its status to 2)
        notification.accep = 2  # Setting accep to 2, as per your requirement
        print("#################################################################")
        print(notification)
        db.session.commit()

        # Return the updated notification
        return jsonify({'message': 'Campaign accepted successfully', 'id': notification.id})

# Register the resource
api.add_resource(AcceptNotification, '/accept/influencer/<int:id>')





class RejectNotification(Resource):
    def delete(self, id):
        # Get the notification ID from the request
        print(f"Rejecting notification with ID: {id}")
        
        # Query the notification by ID
        from models import Campaign
        notification = db.session.query(Campaign).filter_by(id=id).first()

        # Check if the notification exists
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404

        # Reject the notification (could update its status or delete it)
        notification.accep = '0'
        print("#################################################################")
        print(notification)
        db.session.commit()

        # Return the updated notification
        return jsonify({'message': 'Notification rejected successfully', 'id': notification.id})

# Register the resource
api.add_resource(RejectNotification, '/delete/notification/<int:id>')


class RejectNotification1(Resource):
    def delete(self, id):
        # Get the notification ID from the request
        print(f"Rejecting notification with ID: {id}")
        
        # Query the notification by ID
        from models import Campaign
        notification = db.session.query(Campaign).filter_by(id=id).first()

        # Check if the notification exists
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404

        # Reject the notification (could update its status or delete it)
        notification.accep = '2'
        print("#################################################################")
        print(notification)
        db.session.commit()

        # Return the updated notification
        return jsonify({'message': 'Notification rejected successfully', 'id': notification.id})

# Register the resource
api.add_resource(RejectNotification1, '/delete/notification1/<int:id>')
























# class CampaignList(Resource):
#     # @cache.cached(timeout=50, key_prefix="get_campaigns")
#     def get(self):
#         print("hi")
#         campaigns = db.session.execute(text('SELECT * FROM campaigns')).fetchall()
#         print(campaigns)
#         campaigns_list = []
#         for campaign in campaigns:
#             camp = {
#                 'id': campaign.id,
#                 'title': campaign.title,
#                 'budget': campaign.budget,
#                 'description': campaign.description,
#                 'sponsor': campaign.sponsor ,  # Assuming a relationship exists
#                 'influencer': campaign.influencer if campaign.influencer else None,  # Assuming a relationship exists
#                 'enddate': campaign.end_date if campaign.end_date else None  # Format date
#             }
#             campaigns_list.append(camp)
#             print(campaigns_list)
#         return campaigns_list, 200



















    



class Campaign(Resource):
    # getting the detailes of a single campaign
    @jwt_required()
    def get(self, id):
        from models import Campaign
        campaign = Campaign.query.get(id)
        if campaign:
            return {
                'id': campaign.id,
                'title': campaign.title,
                'description': campaign.description,
                'budget': campaign.budget,
                'sponsor': campaign.sponsor.name if campaign.sponsor else None,
                'influencer': campaign.influencer.name if campaign.influencer else None,
                'enddate': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None
            }
        else:
            return {'error': 'Campaign not found'}, 404

    # editing the campaign details
    @jwt_required()
    def put(self, id):
        print("hi12313122")
        data = request.get_json()
        from models import Campaign
        campaign = Campaign.query.get(id)
        x=campaign.sponsor
        y=campaign.influencer
        print("spondetailes")
        print(x)
        if campaign:
            campaign.title = data.get('title', campaign.title)
            campaign.description = data.get('description', campaign.description)
            campaign.budget = data.get('budget', campaign.budget)
            campaign.end_date = data.get('enddate', campaign.end_date)
            
            sponsor_id = data.get('sponsor')
            campaign.sponsor = x

            influencer_id = data.get('influencer')
            campaign.influencer_id = y
            
            db.session.flush()
            db.session.commit()
            return {
                'message': f"Campaign {campaign.title} updated successfully",
                'resource': {
                    'id': campaign.id,
                    'title': campaign.title,
                    'description': campaign.description,
                    'budget': campaign.budget,
                    'enddate': campaign.end_date if campaign.end_date else None,
                    'sponsor': campaign.sponsor if campaign.sponsor else None,
                    'influencer': campaign.influencer if campaign.influencer else None,
                }
            }, 200
        else:
            return {'error': 'Campaign not found'}, 404

    # deleting the Campaign
    @jwt_required()
    def delete(self, id):
        campaign = Campaign.query.get(id)
        if campaign:
            db.session.delete(campaign)
            db.session.flush()
            db.session.commit()
            return {
                'message': f"Campaign {campaign.title} deleted successfully",
                'resource': {
                    'id': campaign.id,
                    'title': campaign.title,
                    'description': campaign.description
                }
            }, 200
        else:
            return {'error': 'Campaign not found'}, 404

# creating a campaign
    @jwt_required()
    def post(self):
        data = request.get_json()
        print(data)
        email = request.headers.get('X-User-Email')
        print(email)
        print(data)
        if data:
            sponsor = email
            print(sponsor)
            end_date1 = datetime.strptime(data['enddate'], '%Y-%m-%d').date()

            title1=data['name']
            from models import Campaign
            campaign2 = db.session.query(Campaign).filter_by(title=title1).first()

            if not campaign2:
                # Execute the raw SQL query to insert the new campaign
                from models import Campaign
                new_campaign = Campaign(
                    title=data['name'],
                    description=data['description'],
                    budget=data['budget'],
                    end_date=end_date1,
                    influencer=0,
                    sponsor=sponsor,
                    flagged=False,
                    accep=0,
                    progress="pending"
                )
                print("hi")

                # Commit the transaction
                print("hi")
                db.session.add(new_campaign)
                db.session.commit()
                return {
                'message': f"Campaign {new_campaign.title} has been sent to db",
                'resource': {
                    'id': new_campaign.id,
                    'title': new_campaign.title,
                    'description': new_campaign.description,
                    'budget': new_campaign.budget,
                    'enddate': new_campaign.end_date,
                    'sponsor': new_campaign.sponsor,
                    'influencer': new_campaign.influencer,
                }
            }, 201
            else:
                print("name already taken")
            return {
                'message': f"Campaign has been sent to db",},400
        else:
            return {'error': 'Invalid data'}, 400




class SearchCampaignResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        # Search for campaigns based on the query
        campaigns = Campaign.query.filter(or_(
            Campaign.title.ilike(f'%{query}%'),
            Campaign.description.ilike(f'%{query}%'),
            Campaign.budget.ilike(f'%{query}%'),
            Campaign.end_date.ilike(f'%{query}%'),
            Campaign.sponsor.has(Sponsor.name.ilike(f'%{query}%')),
            Campaign.influencer.has(Influencer.name.ilike(f'%{query}%'))
        )).all()
        campaign_list = []
        for campaign in campaigns:
            campaign_data = {
                'id': campaign.id,
                'title': campaign.title,
                'description': campaign.description,
                'budget': campaign.budget,
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'sponsor': campaign.sponsor if campaign.sponsor else None,
                'influencer': campaign.influencer if campaign.influencer else None,
            }
            campaign_list.append(campaign_data)

        return jsonify({"campaigns": campaign_list}), 200



class SearchResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')

        # Search for campaigns based on the query
        from models import Campaign
        from sqlalchemy import or_

        campaigns = Campaign.query.filter(or_(
            Campaign.title.ilike(f'%{query}%'), # Searching sponsor email (or any other relevant field) # Searching influencer name (or any other relevant field)
        )).all()

        campaign_list = []

        for campaign in campaigns:
            campaign_data = {
                'id': campaign.id,
                'title': campaign.title,
                'description': campaign.description,
                'budget': campaign.budget,
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'sponsor': campaign.sponsor if campaign.sponsor else None,
                'influencer': campaign.influencer if campaign.influencer else None,
            }
            campaign_list.append(campaign_data)
        print(campaign_list)

        return jsonify({'campaigns': campaign_list})































api.add_resource(login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(complete_campaign, '/influ/camp/comp/<int:id>')
api.add_resource(Campaign, '/update/campaign/<int:id>',
                 '/delete/campaign/<int:id>', '/get/campaign/<int:id>',
                 '/spon/camp/add')



api.add_resource(CampaignList,'/get/campaigns')

class NotifiList(Resource):
    @cache.cached(timeout=50, key_prefix="get_Campaign1")
    def get(self):
        email = request.headers.get('X-User-Email')
        role=request.headers.get('X-User-role')
        # print(influencer_email)
        # campaign=db.session.execute(
        #     text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        print(role)
        print(email)
        print('##########################################################################')
        from models import Campaign
        campaign1 = db.session.query(Campaign).filter(
            Campaign.sponsor == email,  
            Campaign.accep == 1
        ).all()

        campaigns_list = []
        for campaign in campaign1:
            camp = {
                'id': campaign.id,
                'title': campaign.title,
                'budget': campaign.budget,
                'description': campaign.description,
                'accep':campaign.accep,
                'sponsor': campaign.sponsor,
                'influencer': campaign.influencer,
                'enddate': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            }
            campaigns_list.append(camp)
        print(campaigns_list)
        return jsonify({'campaigns': campaigns_list})
api.add_resource(NotifiList,'/get/notifications')





class NotifiList1(Resource):
    def get(self):
        email = request.headers.get('X-User-Email')
        role=request.headers.get('X-User-role')
        # print(influencer_email)
        # campaign=db.session.execute(
        #     text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        print(role)
        print(email)
        print('##########################################################################')
        from models import Campaign
        campaign1 = db.session.query(Campaign).filter(
            Campaign.sponsor == email,  
            Campaign.accep == 3
        ).all()

        campaigns_list = []
        for campaign in campaign1:
            camp = {
                'id': campaign.id,
                'title': campaign.title,
                'budget': campaign.budget,
                'description': campaign.description,
                'accep':campaign.accep,
                'sponsor': campaign.sponsor,
                'influencer': campaign.influencer,
                'proof':campaign.proof,
                'enddate': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            }
            campaigns_list.append(camp)
        print(campaigns_list)
        return jsonify({'campaigns': campaigns_list})
api.add_resource(NotifiList1,'/get/notifications1')



class NotifiList2(Resource):
    def get(self):
        email = request.headers.get('X-User-Email')
        role=request.headers.get('X-User-role')
        # print(influencer_email)
        # campaign=db.session.execute(
        #     text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        print(role)
        print(email)
        print('*******************************************************************')
        from models import Campaign
        campaign1 = db.session.query(Campaign).filter(
            Campaign.sponsor == email,  
            Campaign.accep == 4
        ).all()

        campaigns_list = []
        for campaign in campaign1:
            camp = {
                'id': campaign.id,
                'title': campaign.title,
                'budget': campaign.budget,
                'description': campaign.description,
                'accep':campaign.accep,
                'sponsor': campaign.sponsor,
                'influencer': campaign.influencer,
                'proof':campaign.proof,
                'enddate': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            }
            campaigns_list.append(camp)
        print(campaigns_list)
        return jsonify({'campaigns': campaigns_list})
api.add_resource(NotifiList2,'/get/notifications2')






class NotifiList3(Resource):
    def get(self):
        email = request.headers.get('X-User-Email')
        role=request.headers.get('X-User-role')
        # print(influencer_email)
        # campaign=db.session.execute(
        #     text('SELECT * FROM campaigns')).fetchall()
        # print(campaign)
        print(role)
        print(email)
        print('*******************************************************************')
        from models import Campaign
        campaign1 = db.session.query(Campaign).filter(
            Campaign.influencer == email,  
            Campaign.accep == 4
        ).all()
        print(campaign1)

        campaigns_list = []
        for campaign in campaign1:
            camp = {
                'id': campaign.id,
                'title': campaign.title,
                'budget': campaign.budget,
                'description': campaign.description,
                'accep':campaign.accep,
                'sponsor': campaign.sponsor,
                'influencer': campaign.influencer,
                'proof':campaign.proof,
                'enddate': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
            }
            campaigns_list.append(camp)
        print(campaigns_list)
        return jsonify({'campaigns': campaigns_list})
api.add_resource(NotifiList3,'/get/notifications3')
































api.add_resource(SearchResource, '/search/for')



# @cache.cached(timeout=50, key_prefix="get_Campaign")
class CampaignListall(Resource):
    from models import Campaign
    def get(self):
        print('hi123312')
        from models import Campaign
        categories = Campaign.query.all()
        print("123")
        campaigns_list = []
        for category in categories:
            cat = {
                'id': category.id,
                'name': category.title,
                'budget': category.budget,
                'end_date': category.end_date.strftime('%Y-%m-%d'),
                'sponsor': category.sponsor,
                'influencer': category.influencer,
            }
            campaigns_list.append(cat)
            print(campaigns_list)
        return campaigns_list
api.add_resource(CampaignListall,'/get/current-campaigns')

# ----------- All the micro services or celery tasks will be added here ------------###
@celery.task()
def daily_reminder():
    from models import Campaign
    users=Campaign.query.all()
    for user in users:
        flag=True
        if user.end_date.strftime("%m/%d")==datetime.now().strftime("%m/%d"):
            flag=False
            break
        if flag:
            with mail.connect() as conn:
                subject= "campaign Reminder"
                message = """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color: #28a745;">Reminder: campaign</h1>
                            <p>This is a friendly reminder to complete the campaign as soon as possible</p>
                            <a href="http://127.0.0.1:5000/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #fff; text-decoration: none; border-radius: 5px;">Visit Eat Fresh App</a>
                            <p>please complete the camapign as soon as possible.</p>
                        </div>
                        """
                msg = Message(recipients=[user.sponsor],html=message, subject=subject)
                conn.send(msg)
    return {"status": "success"}


@celery.task()
def monthly_report():
    from models import Campaign
    users=Campaign.query.all()
    for user in users:
        flag=True
        print(user.end_date)
        print(datetime.now())
        if user.end_date.strftime("%m/%d")==datetime.now().strftime("%m/%d"):
            flag=False
            break
        if flag:
            with mail.connect() as conn:
                subject= "campaign Reminder"
                message = """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color: #28a745;">Reminder: Visit Eat Fresh App</h1>
                            <p>This is a friendly reminder to complete the campaign as soon as possible</p>
                            <a href="http://127.0.0.1:5000/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #fff; text-decoration: none; border-radius: 5px;">Visit Eat Fresh App</a>
                            <p>please complete the camapign as soon as possible.</p>
                        </div>
                        """
                msg = Message(recipients=[user.influencer],html=message, subject=subject)
                conn.send(msg)
    return {"status": "success"}



@celery.task
def user_triggered_async_job():
    header = ["Campaign Title", "Description", "Budget", "End Date", "Sponsor", "Influencer"]
    
    with open('campaign_report.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        content = []
        from models import Campaign
        for campaign in Campaign.query.all():
            csvwriter.writerow([
                campaign.title,
                campaign.description,
                campaign.budget,
                campaign.end_date.strftime('%Y-%m-%d'),
                campaign.sponsor if campaign.sponsor else "N/A",
                campaign.influencer if campaign.influencer else "N/A"
            ])
            item = {
                'title': campaign.title,
                'description': campaign.description,
                'budget': campaign.budget,
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'sponsor': campaign.sponsor if campaign.sponsor else "N/A",
                'influencer': campaign.influencer if campaign.influencer else "N/A",
            }
            content.append(item)
    return {'header': header, 'content': content}


@app.route('/get/report/data', methods=['GET'])
def get_report():
    job = user_triggered_async_job.delay()
    result = job.get()
    return result, 200

@app.route('/get/report/download', methods=['GET'])
def download_report():
    with open('campaign_report.csv', 'r') as file:
        csv_reader = csv.reader(file)
        csv_data = list(csv_reader)
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerows(csv_data)
        print(csv_buffer.getvalue())
    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


# ------- To schedule the tasks --------#
celery.conf.beat_schedule = {
    'my_monthly_task': {
        'task': "main.daily_reminder",
        'schedule': crontab(hour=13, minute=50, day_of_month=1,
                            month_of_year='*/1'),
    },
    'my_daily_task': {
        'task': "main.monthly_report",
        'schedule': crontab(hour=21, minute=0),
    },
    'my_quick_check_task': {
        'task': "main.daily_reminder",
        'schedule': crontab(minute='*/1'), 
    },
}

if __name__ == "__main__":
    app.run()
