from flask_bcrypt import check_password_hash
from flask_httpauth import HTTPBasicAuth

from API.models_api import FamilyMembers

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login, password):
    member = FamilyMembers.query.filter_by(login=login).first()
    if member is not None and check_password_hash(member.password, password):
        return login