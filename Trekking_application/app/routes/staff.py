from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Trek
from ..forms.staff_forms import StaffTrekForm
from ..extensions import db

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if current_user.role != "staff":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))
    trek = Trek.query.filter_by(assigned_staff_id=current_user.id ).first()

    if not trek:
        return render_template( "staff/dashboard.html",trek=None)

    form = StaffTrekForm(obj=trek)

    if form.validate_on_submit():
        trek.available_slots = form.available_slots.data
        trek.status = form.status.data
        db.session.commit()
        flash("Trek updated successfully!", "success")
        return redirect(url_for("staff.dashboard"))

    return render_template("staff/dashboard.html",trek=trek,form=form)