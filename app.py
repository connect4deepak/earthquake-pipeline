import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request
import psycopg2
import psycopg2.extras

PIPELINE_DIR = "/home/ubuntu/earthquake-pipelibe"
sys.path.insert(0, PIPELINE_DIR)
from config import DB_CONFIG, PROCESSED_TABLE, RAW_TABLE
app = Flask(__name__)