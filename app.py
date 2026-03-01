from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)









# =========================
# MODELS
# =========================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False)  # admin / student / company
    is_approved = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship("StudentProfile", back_populates="user", uselist=False)
    company_profile = db.relationship("CompanyProfile", back_populates="user", uselist=False)
    notifications = db.relationship("Notification", back_populates="user")
    # one to one relationship one User has one StudentProfile




class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    resume = db.Column(db.String(200))

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student")
    placements = db.relationship("Placement", back_populates="student")




class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    website = db.Column(db.String(150))

    user = db.relationship("User", back_populates="company_profile")
    jobs = db.relationship("Job", back_populates="company")
    placements = db.relationship("Placement", back_populates="company")


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"), nullable=False)

    title = db.Column(db.String(150))
    skills = db.Column(db.String(200))
    salary = db.Column(db.String(50))
    description = db.Column(db.Text)

    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    company = db.relationship("CompanyProfile", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job")
    placements = db.relationship("Placement", back_populates="job")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)

    status = db.Column(db.String(50), default="Applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship("Job", back_populates="applications")
    student = db.relationship("StudentProfile", back_populates="applications")
    status_logs = db.relationship("ApplicationStatusLog", back_populates="application")


class ApplicationStatusLog(db.Model):
    __tablename__ = "application_status_logs"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)

    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship("Application", back_populates="status_logs")

    
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 👤 Relationship back to User
    user = db.relationship(
        "User",
        back_populates="notifications"
    )


class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id"),
        nullable=False
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    offer_date = db.Column(db.DateTime, default=datetime.utcnow)
    salary_offered = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Placed")

    student = db.relationship("StudentProfile", back_populates="placements")
    company = db.relationship("CompanyProfile", back_populates="placements")
    job = db.relationship("Job", back_populates="placements")








@app.route("/regester", methods=["GET", "POST"])
def regester():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered"

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
            is_approved=False if role == "company" else True
        )

        db.session.add(user)
        db.session.commit()

        # 🔥 CREATE PROFILE BASED ON ROLE
        if role == "company":
            company_profile = CompanyProfile(
                user_id=user.id,
                company_name=name
            )
            db.session.add(company_profile)

        elif role == "student":
            student_profile = StudentProfile(
                user_id=user.id
            )
            db.session.add(student_profile)

        db.session.commit()
        return "Registered Successfully"

    return render_template("regester.html")






"""
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return "No user found"

        if user.password != password:
            return "Wrong password"

        if user.role == "company" and not user.is_approved:
            return "You are not approved"

        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))

        elif user.role == "company":
            return redirect(url_for("company_dashboard"))

        elif user.role == "student":
            return redirect(url_for("student_dashboard"))

    return render_template("login.html")"""



# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="Invalid email or password")

        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid email or password")

        if user.role == "company" and not user.is_approved:
            return render_template("login.html", error="Company not approved yet")

        # Create session
        session["user_id"] = user.id
        session["role"] = user.role

        # Redirect based on role
        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif user.role == "company":
            return redirect(url_for("company_dashboard"))
        elif user.role == "student":
            return redirect(url_for("student_dashboard"))

    return render_template("login.html")







@app.route("/student_dashboard")
def student_dashboard():
    return "This is Student Dashboard"














#MY WORKS

# ADMIN DASHBOARD
@app.route("/admin_dashboard")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    total_students = User.query.filter_by(role="student").count()

    total_companies = User.query.filter_by(
        role="company",
        is_approved=True
    ).count()

    total_jobs = Job.query.count()
    total_applications = Application.query.count()

    # Pending company approvals
    pending_companies = User.query.filter_by(
        role="company",
        is_approved=False
    ).all()

    # 🔥 Pending job approvals (NEW)
    pending_jobs = Job.query.filter_by(
        is_approved=False
    ).all()

    recent_applications = Application.query.order_by(
        Application.applied_at.desc()
    ).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_jobs=total_jobs,
        total_applications=total_applications,
        pending_companies=pending_companies,
        pending_jobs=pending_jobs,   # 🔥 pass this
        recent_applications=recent_applications
    )





#COMAPNY DASHBOARD
@app.route("/company_dashboard")
def company_dashboard():
    if "role" not in session or session["role"] != "company":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user.company_profile:
        return "Company profile not created"

    company = user.company_profile

    active_jobs = Job.query.filter_by(
        company_id=company.id,
        is_active=True
    ).all()

    closed_jobs = Job.query.filter_by(
        company_id=company.id,
        is_active=False
    ).all()

    total_applications = Application.query.join(Job).filter(
        Job.company_id == company.id,
        Job.is_approved == True
    ).count()

    return render_template(
        "company_dashboard.html",
        company=company,
        active_jobs=active_jobs,
        closed_jobs=closed_jobs,
        total_applications=total_applications
    )





@app.route("/create_job", methods=["GET", "POST"])
def create_job():
    if "role" not in session or session["role"] != "company":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    company = user.company_profile

    if request.method == "POST":
        title = request.form["title"]
        skills = request.form["skills"]
        salary = request.form["salary"]
        description = request.form["description"]

        job = Job(
            company_id=company.id,
            title=title,
            skills=skills,
            salary=salary,
            description=description,
            is_active=True,
            is_approved=False
        )

        db.session.add(job)
        db.session.commit()

        return redirect(url_for("company_dashboard"))

    return render_template("create_job.html")






#JOB CLOSE
@app.route("/close_job/<int:job_id>")
def close_job(job_id):
    if "role" not in session or session["role"] != "company":
        return redirect(url_for("login"))

    job = Job.query.get_or_404(job_id)

    if job.is_approved:
        job.is_active = False
        db.session.commit()

    return redirect(url_for("company_dashboard"))











# APPROVECOMPANY by ADMIN

@app.route("/approve_company/<int:user_id>")
def approve_company(user_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    company = User.query.get_or_404(user_id)
    company.is_approved = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

# REJECTED COMPANY BY ADMIN
@app.route("/reject_company/<int:user_id>")
def reject_company(user_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    company = User.query.get_or_404(user_id)
    db.session.delete(company)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))






#APROVED JOBES by ADMIN
@app.route("/approve_job/<int:job_id>")
def approve_job(job_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    job = Job.query.get_or_404(job_id)
    job.is_approved = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))


# REJECTED JOB by ADMIN
@app.route("/reject_job/<int:job_id>")
def reject_job(job_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    job = Job.query.get_or_404(job_id)


    db.session.delete(job)


    db.session.commit()

    return redirect(url_for("admin_dashboard"))




#Admin Job Detail Route
@app.route("/admin/job/<int:job_id>")
def admin_view_job(job_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    job = Job.query.get_or_404(job_id)
    return render_template("admin_job_detail.html", job=job)






@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================
# APP START
# =========================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(email="admin@gmail.com").first()

        if not admin:
            admin_user = User(
                name="admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin"),
                role="admin",
                is_approved=True
            )

            db.session.add(admin_user)
            db.session.commit()

    app.run(debug=True)

