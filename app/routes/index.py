from flask import Blueprint, render_template

projects_router = Blueprint("projects_router", __name__)

@projects_router.route("/")
def index():
    return "<h1>Hola</h1>"