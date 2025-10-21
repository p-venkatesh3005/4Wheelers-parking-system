from flask import Blueprint, render_template,request,redirect
from models import db
from models.user import Users
admin_bp = Blueprint('admin_bp', __name__,)
@admin_bp.route('/login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=Users.query.filter_by(email=email,password=password).first()
        if email=='pudivenkatesh914@gmail.com':
            user=Users.query.filter_by(email=email,password=password).first()
            if user:
                print("Login successful")
                print("Welcome Admin")
                return redirect('/adashboard/profile')
        else:
            print("Login failed, please check your credentials")
            return redirect('/admin/login')    
    return render_template("adminlogin.html")