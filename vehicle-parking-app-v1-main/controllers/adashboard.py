from flask import Blueprint, render_template, request, redirect
from models import db
from models.lots import Lots1
from models.user import Users
from models.reserveparkspot import ReserveParkSpot
from models.delspot import Dels
from sqlalchemy import func
adashboard_bp = Blueprint('adashboard_bp', __name__)
def delsp(a,b):
    k=str(a)+str(b)
    d=Dels.query.filter(Dels.spot_id==k).first()
    if d:
        return True
    return False
def booked(r):
    p=ReserveParkSpot.query.filter(ReserveParkSpot.spot_id==r).order_by(ReserveParkSpot.id.desc()).first()
    if p==None or p.Action=="released out":
        return True
    return False
@adashboard_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    x=ReserveParkSpot.query.all()
    lots=Lots1.query.all()
    r=ReserveParkSpot.query.all()
    return render_template("admin_dash.html", lots=lots, spots=x,slot=r,delsp=delsp,booked=booked)
@adashboard_bp.route('/addparkinglot',methods=['GET', 'POST'])
def add_lot():
    if request.method=='POST':
        prime_location = request.form.get('prime_location')
        price = request.form.get('price')
        status =request.form.get('status')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        max_slots = int(request.form.get('max_slots'))
        name = request.form.get('name')
        new_lot = Lots1(prime_location=prime_location, price=price, status=status, address=address, pin_code=pin_code, max_slots=max_slots, name=name)
        db.session.add(new_lot)
        db.session.commit()
        lot=Lots1.query.all()
        spot=ReserveParkSpot.query.all()
        return render_template("admin_dash.html",lots=lot,slot=spot,spot=spot,delsp=delsp,booked=booked)
    return render_template("add_lot.html")
@adashboard_bp.route('/<int:lot_id>/remove', methods=['GET'])
def remove_lot(lot_id):
    lot=Lots1.query.all()
    f=Dels.query.all()
    r=ReserveParkSpot.query.filter(ReserveParkSpot.lot_id==lot_id).all()
    for j in r:
        if j.Action=="Release":
            return render_template("admin_dash.html",lots=lot,slot=r,spot=r,delsp=delsp,m=True,booked=booked)
    l=Lots1.query.get(lot_id)
    for i in f:
        if str(i.spot_id)[0]==str(lot_id):
            db.session.delete(i)
            db.session.commit()
            
    for i in r:
        if i.Action=="Release":
            return render_template("admin_dash.html",lots=lot,slot=r,spot=r,delsp=delsp,booked=booked)
    if l:
        db.session.delete(l)
        db.session.commit()
    lot=Lots1.query.all()
    return render_template("admin_dash.html",lots=lot,slot=r,spot=r,delsp=delsp,booked=booked)
@adashboard_bp.route('/<int:lot_id>/editlot', methods=['GET', 'POST'])
def edit_lot(lot_id):
    x=Lots1.query.get(lot_id)
    if request.method=='POST':
        prime_location = request.form.get('prime_location')
        price=request.form.get('price')
        status = (request.form.get('status') == '1')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        max_slots = int(request.form.get('max_slots'))
        name = request.form.get('name')
        y=Lots1(id=lot_id, prime_location=prime_location, price=price, status=status, address=address, pin_code=pin_code, max_slots=max_slots, name=name)
        db.session.add(y)
        db.session.delete(x)
        db.session.commit()
        return redirect('/adashboard/profile')
    return render_template("edit_lot.html", lot=x)
@adashboard_bp.route('/editprofile', methods=['GET', 'POST'])
def edit_profile():
    x= Users.query.get(1)
    if request.method == 'POST':
        x.password = request.form.get('password')
        email = request.form.get('email')
        x.email = email
        name = request.form.get('name')
        x.name = name
        db.session.commit()
        return render_template("view_profile.html", user=x)
    return render_template("view_profile.html",user=x)
@adashboard_bp.route('/update', methods=['GET', 'POST'])
def update_profile():
        return render_template("edit_profile.html")
@adashboard_bp.route('/users', methods=['GET'])
def view_users():
    users = Users.query.filter(Users.email!="pudivenkatesh914@gmail.com")
    return render_template("users.html", users=users)
@adashboard_bp.route('/Search', methods=['GET', 'POST'])
def search_users():
    if request.method == 'POST':
        search_type= request.form.get('search_type')
        q=request.form.get('search')
        if search_type == 'user_id':
            user = Users.query.filter(Users.id==q).first()
            x=ReserveParkSpot.query.filter(ReserveParkSpot.user_id==user.id).all() if user else None
            if user:
                return render_template("search_user.html",user=user,users=x,search_type=search_type)
            else:
                return render_template("err.html",user=user)
        elif search_type == 'ploc':
            loc=Lots1.query.filter(Lots1.prime_location==q).all()
            return render_template("search_user.html", lots=loc, search_type=search_type)

    return render_template("search_user.html")
@adashboard_bp.route('/<int:spot_id>/viewsp',methods=["POST","GET"])
def viewsp(spot_id):
    d="U"
    f=ReserveParkSpot.query.filter(ReserveParkSpot.spot_id==spot_id).all()
    for i in f:
        if i.Action=="released out":
            continue
        else:
            d="O"
            break
    return render_template("viewsp.html",spot_id=spot_id,status=d)
    
@adashboard_bp.route('/<int:spot_id>/spd',methods=["POST","GET"])
def detailspot(spot_id):
    print(spot_id)
    s=request.form.get("status")
    if request.method=="POST":
        if s=="O":
            d=ReserveParkSpot.query.filter(ReserveParkSpot.spot_id==spot_id).first()
            return render_template("spotdet.html",spot=d)

    return render_template("viewsp.html",spot_id=spot_id,status=s)
@adashboard_bp.route('/<int:spot_id>/<status>/delspot',methods=["POST","GET"])
def delspot(spot_id,status):
    f=Dels.query.filter(Dels.spot_id==spot_id).first()
    lots=Lots1.query.all()
    spots=ReserveParkSpot.query.all()
    if status=='U':
        if not f:
            x=Dels(spot_id=spot_id)
            db.session.add(x)
            l=Lots1.query.filter_by(id=str(spot_id)[0]).first()
            l.status=l.status-1
            db.session.commit()
        return render_template("admin_dash.html",lots=lots,delsp=delsp,spot=spots,booked=booked)
    return render_template("viewsp.html",lots=lots,delsp=delsp,spot_id=spot_id,m=True,status=status)
@adashboard_bp.route("/summary",methods=['POST','GET'])
def summary():
    x=(db.session.query(Users.name,func.count(ReserveParkSpot.id).label('count')).join(ReserveParkSpot, Users.id == ReserveParkSpot.user_id).group_by(Users.name).order_by(func.count(ReserveParkSpot.id).desc()).limit(5).all())
    ul=[i[0] for i in x]
    uc=[i[1] for i in x]
    y=(db.session.query(Lots1.prime_location,func.count(ReserveParkSpot.id).label('count')).outerjoin(ReserveParkSpot,ReserveParkSpot.lot_id==Lots1.id).group_by(Lots1.prime_location).order_by(func.count(ReserveParkSpot.id)).all())
    ta=[i[0] for i in y]
    tc=[i[1] for i in y]
    return render_template("summ.html",ul=ul,uc=uc,ta=ta,tc=tc)





