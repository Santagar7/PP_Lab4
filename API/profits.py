from flask_httpauth import HTTPBasicAuth

from API.models_api import Profits, FamilyMembers, Session
from API.schemas import ProfitsSchema
from flask import request, Blueprint
from API.verify_password import verify_password, auth


from API.utils import (
    create_entry,
    get_entry_by_id,
    update_entry_by_id,
    delete_entry_by_id,
    get_entries_by_member_id,
    get_entries_by_family_id,
    InvalidUsage
)

session = Session()

# auth = HTTPBasicAuth()
profits = Blueprint("profits", __name__)


@profits.route("/profits", methods=["POST"])
@auth.login_required
def create_profit():
    profit_data = ProfitsSchema().load(request.get_json())
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    profit_data['familyMemId'] = member.id
    profit_data['familyId'] = member.familyId
    return create_entry(Profits, ProfitsSchema, **profit_data)


@profits.route("/profits/family", methods=["GET"])
@auth.login_required
def get_profits():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    return get_entries_by_family_id(Profits, ProfitsSchema, member.familyId)


@profits.route("/profits/member", methods=["GET"])
@auth.login_required
def get_profits_by_member_id():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    return get_entries_by_member_id(Profits, ProfitsSchema, member.id)


@profits.route("/profits/<int:id>", methods=["GET"])
@auth.login_required
def get_profits_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Profits).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    if member.familyId != entry.familyId:
        raise InvalidUsage("Unauthorized access", status_code=403)
    return get_entry_by_id(Profits, ProfitsSchema, id)


@profits.route("/profits/<int:id>", methods=["PUT"])
@auth.login_required
def update_profits_by_id(id):
    profit_data = ProfitsSchema().load(request.get_json())
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Profits).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    # if member.id != entry.familyMemId:
    #     raise InvalidUsage("Unauthorized access", status_code=403)
    profit_data['familyMemId'] = member.id
    profit_data['familyId'] = member.familyId
    return update_entry_by_id(Profits, ProfitsSchema, id, **profit_data)


@profits.route("/profits/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_profits_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    entry = session.query(Profits).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    if member.id != entry.familyMemId:
        raise InvalidUsage("Unauthorized access", status_code=403)
    return delete_entry_by_id(Profits, ProfitsSchema, id)