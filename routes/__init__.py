from flask import Blueprint

bp = Blueprint("routes", __name__)

from .upload_resume import *
from .get_resume_data import *
from .recommended_courses import *

# import more routes like this

