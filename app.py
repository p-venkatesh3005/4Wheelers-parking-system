from flask import Flask, redirect, request, render_template, url_for
from controllers.user import user_bp
from flask_sqlalchemy import SQLAlchemy
from controllers.admin import admin_bp
from models.user import Users
from controllers.adashboard import adashboard_bp
from controllers.udashboard import udashboard_bp
from models import db
app = Flask(__name__)
app.secret_key='venkatesh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'


db.init_app(app)

with app.app_context():
    db.create_all()
    a=Users.query.filter_by(email="pudivenkatesh914@gmail.com").first()
    if not a:
        ad= Users(email="pudivenkatesh914@gmail.com",password="11",name="venkatesh")
        db.session.add(ad)
        db.session.commit()


app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(adashboard_bp,url_prefix='/adashboard')
app.register_blueprint(udashboard_bp,url_prefix='/udashboard')
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/role',methods=['post'])
def role():
    role = request.form.get('role')
    if role=='admin':
        return redirect('/admin/login')
    elif role == 'user':
        return redirect('/user/login')
    else:
        return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
