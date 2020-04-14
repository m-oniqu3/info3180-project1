"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.form import ProfileForm
from app.models import UserProfile
import os, datetime,random
from app import app, db


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/profile", methods=["GET", "POST"])
def profile():
    form=ProfileForm()
    if (request.method =="POST" and form.validate_on_submit()):
        first= form.firstname.data
        last= form.lastname.data
        gen= form.gender.data
        mail = form.email.data
        locate= form.location.data
        biog= form.biography.data
        pic = request.files['picture']
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
        now = datetime.date.today()
        join= now.strftime("%B %d %Y") 
        user= UserProfile(first,last,gen,mail,locate,biog,filename,join)
        db.session.add(user)
        db.session.commit()
       
        flash("User Profile has been added", "success")
        return redirect(url_for('profiles'))
        
    return render_template('profile.html', form=form)
   
@app.route('/profiles', methods=["GET", "POST"])
def profiles():
    users = UserProfile.query.all()
    if request.method == "GET":
        return render_template('profiles.html', users=users)
        
@app.route('/profile/<userid>')
def getUserProfile(userid):
    user = UserProfile.query.filter_by(userid=userid).first()
    return render_template('userprofile.html', user=user)

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
