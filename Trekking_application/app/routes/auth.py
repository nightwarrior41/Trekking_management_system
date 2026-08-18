from flask import Blueprint,render_template,redirect,url_for,flash
from ..models import User
from ..extensions import db
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from ..forms.auth_forms import RegistrationForm,LoginForm


auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["GET","POST"])

def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        if form.role.data == "staff":
            approved = False
        else:
            approved = True
        hashed_password = generate_password_hash(form.password.data)
        
        user = User(
            first_name=form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            password = hashed_password,
            phone = form.phone.data,
            role = form.role.data,
            is_approved = approved
            )
        db.session.add(user)
        db.session.commit()
        
        if approved:
           flash("Registration Successful, Please login.","success")
        else:
            flash("Registration Successful. Please Wait for admin approval.","info")
        
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html",form=form)
        



@auth_bp.route("/login",methods=["GET","POST"])

def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Password or Email Not Correct","warning")
            return redirect(url_for("auth.login"))
        
        if not check_password_hash(user.password,form.password.data):
            flash("Password or Email Not Correct",'warning')
            return redirect(url_for("auth.login"))
        
        if user.is_blacklisted:
            flash("Your account has been suspended. Please contact the administrator.","warning")
            return redirect(url_for("auth.login"))
        
        if user.role == "staff":
            if not user.is_approved:
                flash("Wait For Admin Approval !","info")
                return redirect(url_for("auth.login"))
            
        login_user(user)
        
        if user.role == "staff":
            return redirect(url_for("staff.dashboard"))
        elif user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        else :
            return redirect(url_for("user.dashboard"))
        
    return render_template("auth/login.html",form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home.index"))