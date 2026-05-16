from database import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False) #email
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    accep=db.Column(db.Boolean,default=False)
    platform = db.Column(db.String(50))
    followers = db.Column(db.Integer)
    flagged = db.Column(db.Boolean,default=False)
    niche =  db.Column(db.String(50))
    industry = db.Column(db.String(100))

    
    #campaigns = db.relationship('Campaign', back_populates='user')

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    email = db.Column(db.String(100))  # A separate string column, not a foreign key to 'username' # email
    platform = db.Column(db.String(50), nullable=False)
    followers = db.Column(db.Integer)
    flagged = db.Column(db.Boolean,default=False)
    niche =  db.Column(db.String(50), nullable=False)
    image = db.Column(db.BLOB)


class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100)) #email
    flagged = db.Column(db.Boolean,default=False)
    image = db.Column(db.BLOB)
    #campaigns = db.relationship('Campaign', backref='spon_id')

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False,unique=True)
    description = db.Column(db.String(300), nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    sponsor = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    visibility = db.Column(db.Boolean)
    influencer = db.Column(db.Integer)
    proof=db.Column(db.String)
    flagged = db.Column(db.Boolean, nullable=False, default=False)
    accep = db.Column(db.Integer, nullable=False, default=False)
    progress = db.Column(db.String(20), nullable=False, default='Pending')



class CampaignRequest(db.Model):
    __tablename__ = 'campaign_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influ_id = db.Column(db.Integer, db.ForeignKey('influencers.id'))
    spon_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=False)
    req_status_influ = db.Column(db.Boolean)
    req_status_spon = db.Column(db.Boolean)
    budget = db.Column(db.Integer, nullable=True)
    end_date = db.Column(db.String, nullable=True)
    influ_name = db.Column(db.String)
    influ_followers = db.Column(db.Integer)
    note = db.Column(db.String)
    
    completed = db.Column(db.Boolean, nullable=False, default=False)
    completion_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    title=db.Column(db.String)
    description=db.Column(db.String)
    chart=db.Column(db.String)
