from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User


@app.route("/")
def index():
    return redirect('/users/new')

@app.route("/success")
def email_show():
    email_to_show = User.get_one()
    all_emails= User.get_all()
    return render_template("success.html",email=email_to_show,emails=all_emails)

@app.route('/users/new')
def create_user():
    return render_template("index.html")

@app.route("/users/create",methods=['POST'])
def new_email():
    print(request.form)
    if not User.validate_user(request.form):
        # redirect to the route where the dojo form is rendered.
        return redirect('/')
    User.save(request.form)
    return redirect('/success')

@app.route("/delete_user/<int:user_id>")
def delete_email(user_id):
    User.del_email({'id':user_id})
    
    return redirect('/success')
