from flask import Flask
# from flask import request, Blueprint
# from flask_bcrypt import Bcrypt
# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()
from API.family_member import family_members
from API.family import family
from API.costs import costs
from API.profits import profits

app = Flask(__name__)
app.register_blueprint(family_members)
app.register_blueprint(family)
app.register_blueprint(costs)
app.register_blueprint(profits)
