from app import create_app, db
from app.models import States, Counties, Metros, Metros_Counties, Populations
import os
import csv
from datetime import datetime


print('Entering...')
app = create_app(os.environ.get('CONFIG') or 'development')
with app.app_context():
    db.drop_all()
    db.create_all()

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'states.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:
        next(file)
        for row in csv.reader(file):
            try:
                s = States(id=int(row[0]), state=row[1], abbreviation=row[2])
                db.session.add(s)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('States finished...')

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'counties.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:
        next(file)
        for row in csv.reader(file):
            try:
                c = Counties(id=int(row[0]), county=row[1], state_id=int(row[2]))
                db.session.add(c)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Counties finished...')

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'metros.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:
        next(file)
        for row in csv.reader(file):
            try:
                m = Metros(id=int(row[0]), metro=row[1])
                db.session.add(m)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Metros finished...')

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'metros_counties.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:
        next(file)
        for row in csv.reader(file):
            try:
                mc = Metros_Counties(id=int(row[0]), metro_id=int(row[1]), county_id=int(row[2]))
                db.session.add(mc)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Metros_Counties finished...')

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'populations.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:
        next(file)
        for row in csv.reader(file):
            try:
                p = Populations(id=int(row[0]), county_id=int(row[1]), year=datetime.strptime(row[2], '%Y'),
                                population=int(row[3]))
                db.session.add(p)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Populations finished...')

    print('Finished...')
