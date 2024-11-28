import ast
import requests
import tools.database.database as db
from flask import Flask, json, request, render_template, redirect, url_for, flash, session, g #pip install Flask
#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user #pip install flask-login
from werkzeug.security import generate_password_hash, check_password_hash
from tools.checktarget import check_target
from tools.nslookup import run_nslookup
from tools.nmap import run_nmap
from tools.virustotal import run_virustotal
from tools.iplocation import run_iplocation
from tools.robotstxt import run_robots
from tools.waybackmachine import run_wayback
from tools.nuclei import run_nuclei
from dotenv import load_dotenv  #pip install python-dotenv --break-system-packages
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, name, password, profile_picture):
        self.id = id
        self.name = name
        self.password = password
        self.profile_picture = profile_picture

@app.before_request
def before_request():
    if not current_user.is_authenticated:
        g.user = User(-1, "Admin", "", "/static/image/foto_perfil.png")
    else:
        g.user = current_user

"""OBLIGATORIO DE FLASK-LOGIN"""
@login_manager.user_loader
def load_user(user_id):
    user_row = db.get_user_flask(user_id)
    if user_row:
        return User(user_row['id'], user_row['name'], user_row['password'], user_row['profile_picture'])
    return None

@app.route('/')
def index():
    return render_template('index.html', user=g.user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        
        user_row = db.get_user(name)

        if user_row and check_password_hash(user_row['password'], password):
            print("user: ", user_row['name'])
            user = User(user_row['id'], user_row['name'], user_row['password'], user_row['profile_picture'])
            login_user(user)
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            flash ('User or password incorrect')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = generate_password_hash(request.form['password'])
        profile_picture = request.form['profile_picture']

        if db.get_user(name):
            flash('The username already exists. Please choose another one.')
            return redirect(url_for('register'))
        try:
            requests.get(profile_picture)
        except requests.exceptions.RequestException:
            profile_picture = "/static/image/foto_perfil.png"
        db.create_user(name, password, profile_picture)
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_password':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            db.change_password(g.user.id, current_password, new_password, confirm_password)
            return redirect(url_for('account'))
        elif action == 'delete_account':
            db.delete_user(g.user.id)
            return redirect(url_for('index'))        
    return render_template('account.html', user=g.user)

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    results = request.form.get('results')
    created_at = request.form.get('created_at')
    if results and created_at:
        results = ast.literal_eval(results) #Convierte el string en un diccionario
        return render_template('scan.html', target=target, results=results, created_at=created_at, user=g.user)

    web_exists, web_error = check_target(target)
    if not web_exists:
        flash(web_error)
        return redirect(url_for('index'))

    # NSLOOKUP
    ip = run_nslookup(target)
    print("NSLOOKUP:", ip)

    # NMAP
    use_nmap = request.form.get('use_nmap')
    nmap_results = run_nmap(ip) if use_nmap else {} 
    print("nmap_results: ", nmap_results)

    # VirusTotal
    use_virus = request.form.get('use_virus')
    vt_data, vt_count = run_virustotal(target) if use_virus else ({}, {})
    print("vt_data: ", vt_data)
    print("vt_count: ", vt_count)

    # IP Location
    use_ip = request.form.get('use_ip')
    ip_location = run_iplocation(ip) if use_ip else {}
    print("ip_location: ", ip_location)

    # Robots.txt
    use_robots = request.form.get('use_robots')
    robots_txt = run_robots(target) if request.form.get('use_robots') else {}
    print("robots_txt: ", robots_txt)

    #Wayback Machine
    use_wayback = request.form.get('use_wayback')
    waym_results = run_wayback(target) if use_wayback else []
    print("waym_results: ", waym_results)

    # Nuclei
    use_nuclei = request.form.get('use_nuclei')
    nuclei_results = run_nuclei(target) if use_nuclei else []
    print("nuclei_results: ", nuclei_results)

    if not any([use_nmap, use_virus, use_ip, use_robots, use_wayback, use_nuclei]):
        flash("You didn't press any of the buttons.<br/>For its execution it is necessary to")
        return redirect(url_for('index'))

    if not any([nmap_results, vt_data, vt_count, ip_location, robots_txt, waym_results, nuclei_results]) or ip_location.get('status') == "fail":
        flash("No results found for the given target.<br/>Please try again.")
        return redirect(url_for('index'))
    
    results = {
        "nmap_results": nmap_results,
        "vt_data": vt_data,
        "vt_count": vt_count,
        "ip_location": ip_location,
        "robots_txt": robots_txt,
        "waym_results": waym_results,
        "nuclei_results": nuclei_results
    }
    return render_template( 'scan.html', 
                            target=target,
                            results=results,
                            user=g.user)

@app.route('/save_scan_results', methods=['POST'])
@login_required
def save_scan_results():
    target = request.form.get('target')
    name = request.form.get('scan_name')
    results = request.form.get('results')
    direc_results = db.get_results(g.user.id)
    if direc_results:
        all_results = [dict(row) for row in direc_results]
        for result in all_results:
            if result['name'] is None:
                continue
            elif isinstance(result, dict) and result.get('name') == name:
                flash('The name already exists. Please choose another one.')
                return redirect(url_for('index'))
            else:
                continue
    db.add_results(g.user.id, name, target, results)
    return redirect(url_for('index'))

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    if request.method == 'POST':
        result_id = request.form.get('result_id')
        db.delete_result(result_id, g.user.id)
        return redirect(url_for('results'))
    
    user_data = db.get_results(g.user.id)
    if not user_data:
        return render_template('results.html', user=g.user)
    results = [dict(row) for row in user_data]

    return render_template('results.html', user_data=results, user=g.user)

if __name__ == '__main__':
    db.init()
    app.run(host="0.0.0.0", port=5000)
