from flask import Blueprint

bp = Blueprint('texas', __name__)

from app.states.texas import routes