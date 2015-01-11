#################
#### imports ####
#################

from flask import Blueprint
from project import db
from project.models import Scrap

################
#### config ####
################

api_blueprint = Blueprint(
    'api', __name__,
    template_folder='templates'
)


################
#### routes ####
################

# use decorators to link the function to a url
@api_blueprint.route('/list')
def index():

    # result = db.Query(Scrap).all()
    return 'hello'

@api_blueprint.route('/welcome')
def welcome():
    return 'welcome aa'  # render a template
