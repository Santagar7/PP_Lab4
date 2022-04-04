from flask_httpauth import HTTPBasicAuth

from API.models_api import Family, FamilyMembers
from API.schemas import FamilySchema
from flask import request, Blueprint
import bcrypt
from API.verify_password import verify_password, auth

from API.utils import (
    create_entry,
    get_entries,
    get_entry_by_id,
    update_entry_by_id,
    delete_entry_by_id,
    InvalidUsage
)

# auth = HTTPBasicAuth()
family = Blueprint("family", __name__)


@family.route("/family", methods=["POST"])
def create_family():
    family_data = FamilySchema().load(request.get_json())
    return create_entry(Family, FamilySchema, **family_data)


@family.route("/family", methods=["GET"])
def get_family():
    return get_entries(Family, FamilySchema)


@family.route("/family/<int:id>", methods=["GET"])
def get_family_by_id(id):
    return get_entry_by_id(Family, FamilySchema, id)


@family.route("/family/<int:id>", methods=["PUT"])
@auth.login_required
def update_family_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    # if id != member.familyId:
    #     raise InvalidUsage("Unauthorized access", status_code=403)
    family_data = FamilySchema().load(request.get_json())
    return update_entry_by_id(Family, FamilySchema, id, **family_data)


@family.route("/family/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_family_by_id(id):
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    if id != member.familyId:
        raise InvalidUsage("Unauthorized access", status_code=403)
    return delete_entry_by_id(Family, FamilySchema, id)