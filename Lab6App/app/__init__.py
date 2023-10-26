import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask import Flask, request, jsonify

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views, models


# List ALL users
@app.route("/list", methods=["GET"])
def list_all_users():
    result_set = db.session.query(models.User).all()
    return jsonify(result_set)


# Add NEW user
@app.route("/insert", methods=["POST"])
def insert_user():
    name = request.form.get("user_name")
    email = request.form.get("user_email")

    u1 = models.User(email=email, name=name)

    db.session.add(u1)

    # flush before commit
    db.session.flush()
    db.session.commit()

    status_message = "Row with a primary 🔑 of " + email + " has been inserted"

    return jsonify({"📋:": status_message})


#  UPDATE User
@app.route("/update", methods=["POST"])
def update_user():
    name = request.form.get("user_name")
    email = request.form.get("user_email")

    query = db.session.query(models.User)
    query = query.filter(models.User.email == email)
    rows_changed = query.update({models.User.name: name})

    print("🥞 Rows changed: ", rows_changed)
    print("🔎 query", query)

    # flush before commit
    db.session.flush()
    db.session.commit()

    status_message = (
        "✅ "
        + str(rows_changed)
        + " rows have been updated. User 📧 "
        + email
        + " has been updated"
    )

    return jsonify({"📋:": status_message})


@app.route("/delete", methods=["POST"])
def delete_user():
    email = request.form.get("user_email")

    query = db.session.query(models.User)
    query = query.filter(models.User.email == email)
    rows_changed = query.delete(synchronize_session=False)

    print("🥞 Rows changed: ", rows_changed)
    print("🔎 query", query)

    # flush before commit
    db.session.flush()
    db.session.commit()

    status_message = (
        "🚮 "
        + str(rows_changed)
        + " rows have been updated. User 📧 "
        + email
        + " has been deleted"
    )

    return jsonify({"📋:": status_message})
