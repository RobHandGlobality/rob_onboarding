"""
Entrypoint module for WSGI containers.

"""
from rob_onboarding.app import create_app


app = create_app().app
