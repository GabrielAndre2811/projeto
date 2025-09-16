from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import secrets
import logging
import os
from werkzeug.utils import secure_filename


logging.basicConfig(level=logging.INFO)
banco_bp = Blueprint('banco', __name__)