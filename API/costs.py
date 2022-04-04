from flask_httpauth import HTTPBasicAuth

from API.models_api import Costs, FamilyMembers, Session
from API.schemas import CostsSchema
from flask import request, Blueprint

from API.utils import (
    create_entry,
    get_entry_by_id,
    update_entry_by_id,
    delete_entry_by_id,
    get_entries_by_member_id,
    get_entries_by_family_id,
    InvalidUsage,
)

from API.verify_password import verify_password, auth
session = Session()

# auth = HTTPBasicAuth()
costs = Blueprint("costs", __name__)


@costs.route("/costs", methods=["POST"])
@auth.login_required
def create_cost():
    cost_data = CostsSchema().load(request.get_json())
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    cost_data['familyMemId'] = member.id
    cost_data['familyId'] = member.familyId
    return create_entry(Costs, CostsSchema, **cost_data)


@costs.route("/costs/family", methods=["GET"])
@auth.login_required
def get_costs():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    return get_entries_by_family_id(Costs, CostsSchema, member.familyId)


@costs.route("/costs/member", methods=["GET"])
@auth.login_required
def get_costs_by_member_id():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    return get_entries_by_member_id(Costs, CostsSchema, member.id)


@costs.route("/costs/<int:id>", methods=["GET"])
@auth.login_required
def get_costs_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Costs).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    # if member.familyId != entry.familyId:
    #     raise InvalidUsage("Unauthorized access", status_code=403)
    return get_entry_by_id(Costs, CostsSchema, id)


@costs.route("/costs/<int:id>", methods=["PUT"])
@auth.login_required
def update_cost_by_id(id):
    cost_data = CostsSchema().load(request.get_json())
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Costs).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    if member.id != entry.familyMemId:
        raise InvalidUsage("Unauthorized access", status_code=403)
    cost_data['familyMemId'] = member.id
    cost_data['familyId'] = member.familyId
    return update_entry_by_id(Costs, CostsSchema, id, **cost_data)


@costs.route("/costs/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_costs_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Costs).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    # if member.id != entry.familyMemId:
    #     raise InvalidUsage("Unauthorized access", status_code=403)
    return delete_entry_by_id(Costs, CostsSchema, id)
