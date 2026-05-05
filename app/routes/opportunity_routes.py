from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.opportunity import Opportunity
from app.extensions import db

opp_bp = Blueprint('opportunity', __name__)

@opp_bp.route('/', methods=['POST'])
@jwt_required()
def create_opportunity():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required_fields = [
        "name", "category", "duration", "start_date",
        "description", "skills", "future_opportunities"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    opportunity = Opportunity(
        admin_id=user_id,
        name=data['name'],
        category=data['category'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=data['skills'],
        future_opportunities=data['future_opportunities'],
        max_applicants=data.get('max_applicants')
    )

    db.session.add(opportunity)
    db.session.commit()

    return jsonify({"message": "Opportunity created"}), 201

@opp_bp.route('/', methods=['GET'])
@jwt_required()
def get_opportunities():
    user_id = int(get_jwt_identity())

    opportunities = Opportunity.query.filter_by(admin_id=user_id).all()

    result = []
    for opp in opportunities:
        result.append({
            "id": opp.id,
            "name": opp.name,
            "category": opp.category,
            "duration": opp.duration,
            "start_date": opp.start_date,
            "description": opp.description,
            "skills": opp.skills,
            "future_opportunities": opp.future_opportunities,
            "max_applicants": opp.max_applicants
        })

    return jsonify(result), 200

@opp_bp.route('/<int:opp_id>', methods=['GET'])
@jwt_required()
def get_single_opportunity(opp_id):
    user_id = int(get_jwt_identity())

    opportunity = Opportunity.query.get(opp_id)

    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    if opportunity.admin_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "id": opportunity.id,
        "name": opportunity.name,
        "category": opportunity.category,
        "duration": opportunity.duration,
        "start_date": opportunity.start_date,
        "description": opportunity.description,
        "skills": opportunity.skills,
        "future_opportunities": opportunity.future_opportunities,
        "max_applicants": opportunity.max_applicants
    })


@opp_bp.route('/<int:opp_id>', methods=['PUT'])
@jwt_required()
def update_opportunity(opp_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    opportunity = Opportunity.query.get(opp_id)

    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    if opportunity.admin_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

   
    opportunity.name = data.get('name', opportunity.name)
    opportunity.category = data.get('category', opportunity.category)
    opportunity.duration = data.get('duration', opportunity.duration)
    opportunity.start_date = data.get('start_date', opportunity.start_date)
    opportunity.description = data.get('description', opportunity.description)
    opportunity.skills = data.get('skills', opportunity.skills)
    opportunity.future_opportunities = data.get('future_opportunities', opportunity.future_opportunities)
    opportunity.max_applicants = data.get('max_applicants', opportunity.max_applicants)

    db.session.commit()

    return jsonify({"message": "Opportunity updated successfully"}), 200

@opp_bp.route('/<int:opp_id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(opp_id):
    user_id = int(get_jwt_identity())

    opportunity = Opportunity.query.get(opp_id)

    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    if opportunity.admin_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({"message": "Opportunity deleted successfully"}), 200