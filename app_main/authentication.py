from app_main import app ,params, db, users, web_data, admin_info, course_req,courses
from flask import render_template, session, request, redirect,jsonify
from app_main.db import parse_json
from app_main.routes import updateDailyInfo






@app.route('/dashboard')
def dashboard():
    
    
    if 'admin' in session or 'user' in session: 
        if 'admin' in session and session['admin']['isLogdin']==True:
            return render_template('dashboard.html',title="adMain panel")
        elif 'user' in session and session['user']['isLogdin']==True:
            if users.find_one({"email":session['user']['email'],"password":session["user"]["password"],"isFreeze":False})!=None:
                
                course_re = parse_json(course_req.find({'urserId':session['user']['username']}))
                courseAll = []
                for re in course_re:
                    courseAll.append({"course":parse_json(courses.find_one({'_UID_':re['courseId']})),"request":re})
                
                return render_template('userDashbord.html',title='dashboard',course_req=courseAll,user=session['user'])
            session.pop('user')
            return render_template('error.html',errorMassage='account freezed')
    return redirect('/login')

# ------------------------------
# form utility 
# forms for authentication and create account
#------------------------------

@app.route('/signup',methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        device=request.form['device']
        user = {
            "name":name,
            "username":username,
            "email":email,
            "password":password,
            "isFreeze":False,
            "devices":[device],
            "paid_courses":[],
            "spend_for_courses":0,
            "request":[]
        }
        if users.find_one(parse_json({"username":username,"email":email}))==None and username != 'admin':
            db.add(user,users)
            
            info = updateDailyInfo()
            if info!=None:
                acc = info['account_created']
                acc.append(username)
                db.update({"date":info['date']},{'$set':{"account_created":acc}},web_data)
            if 'admin' in session:
                    session.pop('admin')
            session['user']=user
            session['user']['isLogdin']=True
            return redirect('/dashboard')
        return render_template('signup.html',alertMessage="Server error: username or email already exist.",title="signup")
    return render_template('signup.html',title="signup")

#------------------------------
# loging page 
#------------------------------

@app.route('/login',methods=['GET','POST'])
def login():
    if 'loginAttempt' in session and session['loginAttempt']==8:
        
        return render_template('login.html',title="login",alertMessage="too many attempt please try again after few hours")
        
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        device = request.form['device']
        
        db_query=parse_json(users.find_one(parse_json({"email":email,"password":password})))
        
        
        if params['admin']['email']==email and params['admin']['password']==password:
            db.add({'device':device},admin_info)
            session['admin']=params['admin']
            session['admin']['isLogdin']=True
            if 'user' in session:
                session.pop('user')
            return redirect('/dashboard')
            
        elif db_query!=None:
            devices = db_query['devices']
            
            if len(devices)<=2:
                if devices.count(device)>0:
                    devices=[device]
                    db.update({"email":email,"password":password},{'$set':{"devices":devices}},users)
                else:
                    devices.append(device)
                    db.update({"email":email,"password":password},{'$set':{"devices":devices}},users)
                    
                session['user']=db_query
                session['user']['isLogdin']=True
                if 'admin' in session:
                    session.pop('admin')
                return redirect('/dashboard')
                
            db.update({"email":email,"password":password},{'$set':{"isFreeze":True}},users)
            
            return render_template('error.html',errorMassage="we freeze your account")   
        else:
            if 'loginAttempt' in session:
                session['loginAttempt']+=1
            else:
                session['loginAttempt']=1;
            return render_template('login.html',title="login",alertMessage=f"incorrect email password attempt {session['loginAttempt'] if 'loginAttempt' in session else 0} of 8")

    return render_template('login.html',title="login")

#------------------------------
#logout function remove all user and admin session
#------------------------------

@app.route('/clear')
def clear():
    session.clear()
    return 'clear development session'


@app.route('/logout')
def logout():
    if 'admin' in session:
        session.pop('admin')
    elif 'user' in session:
        session.pop('user')
    return redirect('/login')