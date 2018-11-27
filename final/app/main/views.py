from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
# from .forms import
from ..models import Populations, Counties, Metros, Metros_Counties
from .. import db
from sqlalchemy import or_, func
import re


@main.route('/')
def index():
    metros = db.session.query(Metros)\
        .order_by(Metros.metro)\
        .all()
    return render_template('main/index.html', metros=metros)


@main.route('/metro')
def metro():
    metros = map(int, re.findall('\d+', request.args.get('metros')))

    query = db.session.query(Metros.id, Metros.metro, Populations.year, func.sum(Populations.population).label('population'))\
        .join(Metros_Counties)\
        .join(Counties)\
        .join(Populations)\
        .filter(Metros.id.in_(metros))\
        .group_by(Metros.id, Populations.year)\
        .order_by(Populations.year)\
        .all()

    to_ret = [{'sort_by': i[1], 'population': int(i[3]), 'year': i[2].strftime('%Y')} for i in query]
    return jsonify(to_ret)
