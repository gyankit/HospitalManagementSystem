from flask import Blueprint

pharmacist = Blueprint('pharmacist', __name__)

from HMS.pharmacist import routes