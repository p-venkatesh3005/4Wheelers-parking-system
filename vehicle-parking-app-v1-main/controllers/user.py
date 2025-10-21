from flask import Blueprint, render_template, request,redirect, session, url_for,flash
from models import db
from models.user import Users
user_bp = Blueprint('user_bp', __name__,)
@user_bp.route('/register', methods=['GET','POST'])
def user_register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        name=request.form.get('name')
        new=Users(email=email,password=password,name=name)
        er = Users.query.filter_by(email=email).first()
        if er:
            print("User already exists, please login")
            return redirect('/user/login')
        db.session.add(new)
        db.session.commit()
        print("User registered successfully,now login")
        return render_template("login.html")
    return render_template("register.html")
@user_bp.route('/login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=Users.query.filter_by(email=email,password=password).first()
        if user:
            return redirect(url_for('udashboard_bp.profile', user_id=user.id))
        else:
            return render_template("login.html",l=True)
    return render_template("login.html")