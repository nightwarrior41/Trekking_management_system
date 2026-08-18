from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Trek
from ..models import Booking
from ..extensions import db
user_bp = Blueprint("user", __name__)


@user_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "user":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")

    query = Trek.query.filter(Trek.status == "Open")

    if search:
        query = query.filter( Trek.trek_name.ilike(f"%{search}%"))

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty )

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))
    treks = query.all()

    return render_template(
        "user/dashboard.html",treks=treks,
        search=search,
        difficulty=difficulty,
        location=location
    )


@user_bp.route("/book/<int:trek_id>")
@login_required
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    booking = Booking.query.filter_by( user_id=current_user.id,trek_id=trek.id).first()

    if booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.dashboard"))

    if trek.available_slots <= 0:
        flash("No slots available.", "danger")
        return redirect(url_for("user.dashboard"))

    booking = Booking(user_id=current_user.id,trek_id=trek.id )

    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    flash("Trek booked successfully!", "success")

    return redirect(url_for("user.my_bookings"))


@user_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()

    return render_template("user/my_bookings.html",bookings=bookings )