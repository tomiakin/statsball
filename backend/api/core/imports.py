from api.core.base import BaseStatsBombView
from rest_framework.response import Response
from statsbombpy import sb
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Common HTTP status codes
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500
