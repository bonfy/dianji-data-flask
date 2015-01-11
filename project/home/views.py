#################
#### imports ####
#################

from flask import render_template, Blueprint
from project import db

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


################
#### routes ####
################

# use decorators to link the function to a url
@home_blueprint.route('/')
def index():
    return 'hello world'

@home_blueprint.route('/welcome')
def welcome():
    return 'welcome'  # render a template
