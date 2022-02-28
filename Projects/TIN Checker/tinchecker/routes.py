from asyncio import tasks
from tinchecker import app, db
from flask import render_template, redirect, request, url_for, flash
from tinchecker.resources import *
from tinchecker.models import Users, Admins
from tinchecker.forms import LoginForm
from flask_login import login_user, logout_user, login_required


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home_page():
    if request.method == 'POST':
        my_list = []

        tin = request.form['tinnumber']
        userIP = request.remote_addr
        deviceInfo = request.user_agent.platform
        browserInfo = request.user_agent.browser + " " +request.user_agent.version
        dateTime = date.today().strftime("%B %d, %Y") + " " + datetime.now().strftime("%H:%M:%S")
        meta_data = Users(tin, userIP,deviceInfo, browserInfo, dateTime)
        
        if not tin:
            return render_template('error.html', tasks={"ID":True, "Info":"Empty Entery!", "Detail":status_dict[1]})
        elif not tin.isdigit():
            return render_template('error.html', tasks={"ID":True, "Info":"Wrong Entery!", "Detail":status_dict[2]})
        else:
            try:
                body = BeautifulSoup(requests.get(url + tin).text, 'lxml').body.text.strip()
                try:
                    mytree = list(ET.fromstring(body))
                    
                    for y in mytree:
                        my_list.append(y.tag)       
                    my_list = replaceIt(my_list)
                    
                    z = 0
                    dict.clear()
                    for y in mytree:
                        dict.update({my_list[z]: y.text})
                        z+=1
                    dict.pop("TPNAME_F")
                except:
                    return render_template('error.html', tasks={"ID":True, "Info":"User Cannot Be Found!", "Detail":status_dict[3]})
                try:
                    db.session.add(meta_data)
                    db.session.commit()
                except:
                    pass
            except:
                return render_template('error.html', tasks={"ID":True, "Info":"No Internet Connection!", "Detail":status_dict[4]})
            return redirect('/')
            
    else:
        return render_template("index.html", tasks=dict)

@app.route('/admin')
@login_required
def admin_page():
    total_number = Users.query.count()
    mobile_user = Users.query.filter((Users.deviceInfo == 'android')).count()
    computer_user = Users.query.filter((Users.deviceInfo == 'linux') and (Users.deviceInfo == 'windows')).count()
    mobile_user_per = (mobile_user / total_number) * 100
    computer_user_per = (computer_user / total_number) * 100
    dict = {
        'cond': True,
        'total_number': total_number,
        'mobile_user': mobile_user,
        'mobile_user_per': mobile_user_per,
        'computer_user': computer_user,
        'computer_user_per': computer_user_per
    }
    return render_template('admin.html', tasks=dict)

@app.route('/analytics')
@login_required
def analytics_page():
    return render_template('analytics.html')

@app.route('/tables')
@login_required
def tables_page():
    items = Users.query.all()
    return render_template('tables.html', tasks=items)

@app.route('/tincheck', methods=['POST', 'GET'])
@login_required
def tinchecker_page():
    if request.method == 'POST':
        my_list = []

        tin = request.form['tinnumber']
        userIP = request.remote_addr
        deviceInfo = request.user_agent.platform
        browserInfo = request.user_agent.browser + " " +request.user_agent.version
        dateTime = date.today().strftime("%B %d, %Y") + " " + datetime.now().strftime("%H:%M:%S")
        meta_data = Users(tin, userIP,deviceInfo, browserInfo, dateTime)
        
        if not tin:
            return render_template('error_tin.html', tasks={"ID":True, "Info":"Empty Entery!", "Detail":status_dict[1]})
        elif not tin.isdigit():
            return render_template('error_tin.html', tasks={"ID":True, "Info":"Wrong Entery!", "Detail":status_dict[2]})
        else:
            try:
                body = BeautifulSoup(requests.get(url + tin).text, 'lxml').body.text.strip()
                try:
                    mytree = list(ET.fromstring(body))
                    
                    for y in mytree:
                        my_list.append(y.tag)       
                    my_list = replaceIt(my_list)
                    
                    z = 0
                    dict.clear()
                    for y in mytree:
                        dict.update({my_list[z]: y.text})
                        z+=1
                    dict.pop("TPNAME_F")
                except:
                    return render_template('error_tin.html', tasks={"ID":True, "Info":"User Cannot Be Found!", "Detail":status_dict[3]})
                try:
                    db.session.add(meta_data)
                    db.session.commit()
                except:
                    pass
            except:
                return render_template('error_tin.html', tasks={"ID":True, "Info":"No Internet Connection!", "Detail":status_dict[4]})
            return redirect('/tincheck')
            
    else:
        return render_template("tincheck.html", tasks=dict)

@app.route('/users')
@login_required
def users_page():
    users = Admins.query.all()
    return render_template('users.html', tasks=users)

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/settings')
@login_required
def settings_page():
    return render_template('settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Admins.query.filter_by(email_add=form.email_add.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            app.jinja_env.globals['profile_img'] = attempted_user.profile_img
            # flash(f'Success! You are logged in as : {attempted_user.fullname}')
            return redirect(url_for('admin_page'))
        else:
            return "Failed"

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))
