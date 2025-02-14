from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from flask_session import Session
import os
from scraper.collect import collect_data

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Required for session management
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.permanent_session_lifetime = timedelta(minutes=10)  # Set session timeout
Session(app)  # Initialize session storage

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        session.clear()  # Clears old session data before new search
        session.permanent = True  # Ensures session persists
        job_role = request.form['job_role']
        job_location = request.form['job_location']

        # Run the scraper and parser
        job_results = collect_data(job_role, job_location)

        # Store job results in session
        session['job_results'] = job_results
        session['job_role'] = job_role
        session['job_location'] = job_location

        session.modified = True

        # Redirect to results page
        return redirect(url_for('results'))

    return render_template('search.html')

@app.route('/results', methods=["GET"])
def results():

    job_results = session.get('job_results', [])
    job_role = session.get('job_role', '')
    job_location = session.get('job_location', '')

    if not job_results:  # Redirect back if no search was done
        return redirect(url_for('search'))

    return render_template('results.html', job_role=job_role, job_location=job_location, job_results=job_results)

if __name__ == '__main__':
    app.run(debug=True)
