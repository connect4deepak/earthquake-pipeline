import os
import sys
import csv
import json
import logging
import requests
import psycopg2
import pandas as pd

from datetime import datetime, timezone, timedelta
from pathlib import Path
# from dotenv import load_dotenv