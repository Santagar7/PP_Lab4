from API.models_api import FamilyMembers
from API.schemas import FamilyMembersSchema
from flask import request, Blueprint
import bcrypt
from API.verify_password import verify_password, auth

from flask_httpauth import HTTPBasicAuth

from API.utils import (
    create_entry,
    get_entries,
    get_entry_by_id,
    get_entry_by_login,
    update_entry_by_id,
    delete_entry_by_id
)

# auth = HTTPBasicAuth()
family_members = Blueprint("family_members", __name__)


@family_members.route("/family_members", methods=["POST"])
def create_member():
    family_member_data = FamilyMembersSchema().load(request.get_json())

    pwd = request.json.get('password', None)
    hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    family_member_data.update({"password": hashed_pwd})

    return create_entry(FamilyMembers, FamilyMembersSchema, **family_member_data)


@family_members.route("/family_members", methods=["GET"])  # get all members
def get_members():
    return get_entries(FamilyMembers, FamilyMembersSchema)


@family_members.route("/family_members/<int:id>", methods=["GET"])  # get member by id
def get_member_by_id(id):
    return get_entry_by_id(FamilyMembers, FamilyMembersSchema, id)


@family_members.route("/family_members/<string:login>", methods=["GET"])  # get user by username
def get_member_by_username(login):
    return get_entry_by_login(FamilyMembers, FamilyMembersSchema, login)


@family_members.route("/family_members", methods=["PUT"])
@auth.login_required
def update_member_by_id():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    user_data = FamilyMembersSchema().load(request.get_json())
    return update_entry_by_id(FamilyMembers, FamilyMembersSchema, member.id, **user_data)


@family_members.route("/family_members", methods=["DELETE"])
@auth.login_required
def delete_member_by_id():
    member = FamilyMembers.query.filter_by(login=auth.current_user()).first()
    return delete_entry_by_id(FamilyMembers, FamilyMembersSchema, member.id)
