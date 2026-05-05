from app.extensions import db
from datetime import datetime

class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    future_opportunities = db.Column(db.Text, nullable=False)
    max_applicants = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)