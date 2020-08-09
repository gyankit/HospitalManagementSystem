from flask import Blueprint

diagnostic = Blueprint('diagnostic', __name__)

from HMS.diagnostic import routes