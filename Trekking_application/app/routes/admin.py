from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import current_user,login_required
from ..models import User,Trek,Booking
from ..extensions import db
from ..forms.trek_forms import TrekForm

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_treks = Trek.query.count() 
    total_bookings = Booking.query.count()

    available_slots = (db.session.query(db.func.sum(Trek.available_slots)).scalar() or 0)

    recent_bookings = (Booking.query.order_by(Booking.booking_date.desc()).limit(5).all() )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        available_slots=available_slots,
        recent_bookings=recent_bookings
    )
    
    
@admin_bp.route("/add-trek", methods=["GET", "POST"])
@login_required
def add_trek():
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    form = TrekForm()
    staff_members = User.query.filter_by(role="staff",is_approved=True,is_blacklisted=False).all()
    form.assigned_staff.choices = [(0, "Not Assigned")]
    form.assigned_staff.choices.extend([(staff.id,f"{staff.first_name} {staff.last_name}")
    for staff in staff_members])
    
    if form.validate_on_submit():
        assigned_staff_id = (None if form.assigned_staff.data == 0 else form.assigned_staff.data)

        trek = Trek(
               trek_name=form.trek_name.data,
               location=form.location.data,
               difficulty=form.difficulty.data,
               duration=form.duration.data,
               available_slots=form.available_slots.data,
               status=form.status.data,
               start_date=form.start_date.data,
               end_date=form.end_date.data,
               assigned_staff_id=assigned_staff_id)
        db.session.add(trek)
        db.session.commit()
        flash("Trek created successfully!", "success")
        return redirect(url_for("admin.manage_treks"))
    
    return render_template(
          "admin/trek_form.html",
           form=form,
           page_title="Add New Trek",
           page_description="Create a new trekking experience.",
           button_text="Create Trek")


@admin_bp.route("/manage-treks")
@login_required
def manage_treks():

    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    search = request.args.get("search", "")
    treks = Trek.query.filter(Trek.trek_name.ilike(f"%{search}%")).order_by(Trek.start_date.asc()).all()

    return render_template("admin/manage_treks.html",treks=treks)




@admin_bp.route("/edit-trek/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    trek = Trek.query.get_or_404(trek_id)
    form = TrekForm(obj=trek)
    staff_members = User.query.filter_by(
        role="staff",
        is_approved=True,
        is_blacklisted=False
    ).all()
    form.assigned_staff.choices = [(0, "Not Assigned")]
    form.assigned_staff.choices.extend([
        (staff.id, f"{staff.first_name} {staff.last_name}")
        for staff in staff_members])

    if not form.is_submitted():
        form.assigned_staff.data = trek.assigned_staff_id or 0

    if form.validate_on_submit():

        trek.trek_name = form.trek_name.data
        trek.location = form.location.data
        trek.difficulty = form.difficulty.data
        trek.duration = form.duration.data
        trek.available_slots = form.available_slots.data
        trek.start_date = form.start_date.data
        trek.end_date = form.end_date.data
        trek.status = form.status.data
        trek.assigned_staff_id = (
            None if form.assigned_staff.data == 0
            else form.assigned_staff.data )
        db.session.commit()
        flash("Trek updated successfully!", "success")

        return redirect(url_for("admin.manage_treks"))
    return render_template(
        "admin/trek_form.html",
        form=form,
        page_title="Edit Trek",
        page_description="Update trek information.",
        button_text="Update Trek"
    )
    
    
@admin_bp.route("/delete-trek/<int:trek_id>")
@login_required
def delete_trek(trek_id):

    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully!", "success")

    return redirect(url_for("admin.manage_treks"))


@admin_bp.route("/pending-staff")
@login_required
def pending_staff():
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))
    staff = User.query.filter_by(role="staff", is_approved=False ).all()
    return render_template("admin/pending_staff.html",staff=staff )


@admin_bp.route("/approve-staff/<int:user_id>")
@login_required
def approve_staff(user_id):
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash("Staff approved successfully.", "success")

    return redirect(url_for("admin.pending_staff"))


@admin_bp.route("/reject-staff/<int:user_id>")
@login_required
def reject_staff(user_id):
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Registration rejected.", "warning")

    return redirect(url_for("admin.pending_staff"))



@admin_bp.route("/manage-users")
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    search = request.args.get("search", "")
    users = User.query.filter(
        User.role == "user",
        User.first_name.ilike(f"%{search}%")
    ).all()
    return render_template(
        "admin/manage_users.html",
        users=users,
        search=search
    )
    
@admin_bp.route("/blacklist-user/<int:user_id>")
@login_required
def blacklist_user(user_id):
    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = True
    db.session.commit()
    flash("User blacklisted successfully!", "success")

    return redirect(url_for("admin.manage_users"))
    
@admin_bp.route("/unblacklist-user/<int:user_id>")
@login_required
def unblacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = False
    db.session.commit()
    flash("User restored successfully.", "success")

    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/manage-bookings")
@login_required
def manage_bookings():

    if current_user.role != "admin":
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home.index"))

    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()

    return render_template(
        "admin/manage_bookings.html",
        bookings=bookings
    )
    
@admin_bp.route("/delete-booking/<int:booking_id>")
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.trek.available_slots += 1
    db.session.delete(booking)
    db.session.commit()

    flash("Booking deleted successfully.", "success")

    return redirect(url_for("admin.manage_bookings"))