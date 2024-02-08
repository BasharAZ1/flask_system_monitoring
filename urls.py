# urls.py
from flask import Flask
from views import homepage

def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    

