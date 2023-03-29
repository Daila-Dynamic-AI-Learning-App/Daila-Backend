from flask import Blueprint

daila = Blueprint('daila', __name__, url_prefix='/api/v1')

from v1.views.authRoute import *
from v1.views.actionRoute import *
