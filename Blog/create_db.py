from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from main import db

db.create_all()