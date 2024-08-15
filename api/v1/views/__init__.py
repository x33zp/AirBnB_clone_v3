#!/usr/bin/python3
"""Blue print for API"""
from flask import Blueprint
from api.v1.views.index import *

app_views = BLueprint('app_views', __name__, url_prefix='/api/v1')
