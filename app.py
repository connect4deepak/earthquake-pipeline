import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request
import psycopg2
import psycopg2.extras

