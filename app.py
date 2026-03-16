from flask import Flask
from db.db_helper import init_db
from routes.account_routes import (account)
from routes.auth_routes import(auth)

app=Flask(__name__)

init_db()

app.register_blueprint(account)
app.register_blueprint(auth)

if __name__=="__main__":
    app.run()

