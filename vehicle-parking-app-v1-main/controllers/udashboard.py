from flask import Blueprint, render_template, request, redirect,session
from models import db
from models.lots import Lots1
from models.user import Users
from datetime import datetime
from sqlalchemy import func
from models.delspot import Dels
from models.reserveparkspot import ReserveParkSpot
udashboard_bp = Blueprint('udashboard_bp', __name__)
@udashboard_bp.route('/<int:user_id>/profile', methods=['GET','POST'])
def profile(user_id):
    print("User ID from session:", user_id)
    x=ReserveParkSpot.query.filter_by(user_id=user_id).all()
    if user_id:
        user = Users.query.get(user_id)
        return render_template("user_dash.html", user=user, spot=x)
    else:
        print("No userid")
    return render_template("user_dash.html")
@udashboard_bp.route('/<int:user_id>/search', methods=['POST', 'GET'])
def search(user_id):
    if request.method=='POST':
        loc=request.form.get('search')
        x= Users.query.get(user_id)
        c=ReserveParkSpot.query.filter_by(user_id=user_id).all()
        results = Lots1.query.filter(Lots1.prime_location== loc).all()
        if results:
            return render_template("user_dash.html", results=results, user=x,spot=c)
    return render_template("user_dash.html", n=True, user=x,spot=c)
@udashboard_bp.route('/<int:user_id>/<int:lot_id>/book', methods=['GET', 'POST'])
def book(user_id, lot_id):
    x= Lots1.query.get(lot_id)
    y= Users.query.get(user_id)
    spot_id=0
    z=ReserveParkSpot.query.filter_by(lot_id=lot_id).all()
    all_spots = [f"{x.id}{i}" for i in range(1, x.max_slots + 1)]
    l=Dels.query.all()
    k=[str(f.spot_id) for f in l]
    booked = [str(s.spot_id) for s in z if s.Action != 'released out']+k
    for i in all_spots:
        if i in booked:
            continue
        else:
            spot_id = i
            break
    if x.status <= 0:
        r= ReserveParkSpot.query.filter_by(user_id=user_id).all()
        return render_template('user_dash.html', lot=x, user=y, o=True, spot=r, results=[])
    return render_template('book_spot.html', lot=x, user=y, spot_id=spot_id)
@udashboard_bp.route('/<int:user_id>/<int:lot_id>/bookspot', methods=['GET','POST'])
def book_spot(user_id, lot_id):
    if request.method == 'POST':
        spot_id = request.form.get('spot_id')
        vehicle_number = request.form.get('vehicle_number')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        x = Lots1.query.get(lot_id)
        y = Users.query.get(user_id)
        if x.status>=1:
            if spot_id:
                new_spot = ReserveParkSpot(
                    user_id=user_id,
                    lot_id=lot_id,
                    spot_id=spot_id,
                    vehicle_number=vehicle_number,
                    start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M'),
                    end_time=datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
                )
                x.status-= 1
                duration = abs((new_spot.end_time - new_spot.start_time).total_seconds() / 3600)
                price = round(abs(x.price * duration),2)
                z=ReserveParkSpot.query.get(spot_id)
                db.session.add(new_spot)
                db.session.commit()
                return render_template('booked.html', lot=x, user=y, spot_id=spot_id, vehicle_number=vehicle_number, start_time=start_time, end_time=end_time, price=price,duration=duration)
            else:
                print("No spot selected.")
    return redirect(f'/udashboard/{user_id}/profile')
@udashboard_bp.route('/<int:user_id>/<int:spot_id>/release', methods=['GET', 'POST'])
def release(user_id, spot_id):
    x = ReserveParkSpot.query.filter_by(spot_id=spot_id).all()
    z= Users.query.get(user_id)
    if request.method =='POST' :
        for i in x:
            if i.Action=='Release':
                l= Lots1.query.filter_by(id=i.lot_id).first()
                price=abs(i.start_time- i.end_time).total_seconds() / 3600 * l.price
                return render_template('release_spot.html', spot_id=spot_id, user_id=user_id,spot=i,price=price,user=z)
    print(request.method,i.Action)
    return redirect(f'/udashboard/{user_id}/profile')
@udashboard_bp.route('/<int:user_id>/<int:spot_id>/released', methods=['GET', 'POST'])
def released(user_id, spot_id):
    if request.method == 'POST':
        l=Users.query.get(user_id)
        c=ReserveParkSpot.query.filter_by(user_id=user_id).all()
        x = ReserveParkSpot.query.filter_by(spot_id=spot_id).all()
        for i in x:
            if i.Action=="Release":
                i.Action = 'released out'
                db.session.commit()
                y = Lots1.query.get(i.lot_id)
                if y.max_slots!=y.status:
                    y.status = y.status + 1
                    db.session.commit()
                    return render_template('user_dash.html', spot=c, user_id=user_id,user=l)
    return render_template('user_dash.html', spot=c, user_id=user_id,user=l)
@udashboard_bp.route('/<int:user_id>/summary', methods=['GET'])
def summary(user_id):
    l1=[]
    l2=[]
    p1=[]
    p2=[]
    o=db.session.query(ReserveParkSpot.vehicle_number,func.count(ReserveParkSpot.vehicle_number).label('count')).filter(ReserveParkSpot.user_id==user_id).group_by(ReserveParkSpot.vehicle_number).order_by(func.count(ReserveParkSpot.id).desc()).all()
    for i in o:
        p1.append(i[0])
        p2.append(i[1])
    l=db.session.query(Lots1.prime_location,func.count(ReserveParkSpot.id).label('count')).join(ReserveParkSpot,Lots1.id==ReserveParkSpot.lot_id).filter(ReserveParkSpot.user_id==user_id).order_by(func.count(ReserveParkSpot.id).desc()).group_by(Lots1.prime_location).limit(5).all()
    for i in l:
        l1.append(i[0])
        l2.append(i[1])
    return render_template("sum.html",l1=l1,l2=l2,p1=p1,p2=p2,user_id=user_id)
