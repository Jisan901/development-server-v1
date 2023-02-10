from app_main import app,db,users,web_data,params,courses,course_req
from flask import render_template, session, request, redirect
from app_main.db import parse_json
import datetime

def getLogInfo():
    if 'admin' in session or 'user' in session:
        return True
    return False


def updateDailyInfo():
    date=datetime.datetime.utcnow().strftime("%d-%B-%Y")
    data=parse_json(web_data.find_one({
        "date":date
    }))
    if data==None:
        db.add({
            "date":date,
            "visited":1,
            "sellout_amount":0,
            "sell_courses":[],
            "account_created":[]
        },web_data)
    return data

# ------------------------------- #
#             route    '/'        #
# ------------------------------- #

@app.route('/')
def index():
    info = updateDailyInfo()
    if info!=None:
        db.update({"date":info['date']},{'$set':{"visited":info["visited"]+1}},web_data)
    return render_template('home.html', title = 'Home')

    
# ------------------------------- #
#             /courses            #
# ------------------------------- #
    
@app.route('/courses')
def Courses():
    allCourses = parse_json(courses.find())[0:9]
    return render_template('courses.html',allCourses=allCourses,title='Courses')
    
# ------------------------------- #
#             /course             #
# ------------------------------- #
    
@app.route('/course/<string:key>')
def course(key):
    cdt=parse_json(courses.find_one({'_UID_':key}))
    if cdt!= None:
        return render_template('course.html',data=cdt,title=cdt['title'])
    return '<h1>404 course not found</h1>'
    
    
    
    
# ------------------------------- #
#              request            #
# ------------------------------- #
    
@app.route('/course/apply/<string:key>',methods=['GET','POST'])
def courseReq(key):
    cdt=parse_json(courses.find_one({'_UID_':key}))
    if cdt!= None:
        if 'user' in session:
            user = session['user']
            if request.method=='POST':
                data=dict(
                name=request.form['name'],
                email=request.form['email'],
                phone = request.form['phone'],
                tm=request.form['transection-methode'],
                paynum=request.form['paynum'],
                txid=request.form['trxid'],
                courseId=key,
                state='pending',
                urserId=user['username']
                )
                if course_req.find_one({"urserId":user['username'],"courseId":key})==None:
                    
                    key=db.add(data,course_req)['common']
                    old_req=parse_json(users.find_one({
                        "email":user['email'],
                        "password":user['password']
                    }))['request']
                    old_req.append(key)
                    db.update({
                        "email":user['email'],
                        "password":user['password']
                    },{
                        "$set":{
                            'request':old_req
                        }
                    },users)
                    
                    
                return render_template('courseApply.html',data=cdt,act=key,title=cdt['title'],alertMessage='requested')
            return render_template('courseApply.html',data=cdt,act=key,title=cdt['title'])
        return redirect('/login')
    return '<h1>404 course not found</h1>'
    
    
    
# ------------------------------- #
#              watch              #
# ------------------------------- #
    
@app.route('/class/watch/<string:key>')
def courseWatch(key):
    if 'user' in session:
        user = parse_json(users.find_one({'username':session['user']['username']}))
        if user['paid_courses'].count(key)>0:
            course = parse_json(courses.find_one({'_UID_':key}))
            videos = course['videos']
            
            return render_template('courseVideos.html',title = 'videos',videos = videos)
    if 'admin' in session:
        course = parse_json(courses.find_one({'_UID_':key}))
        videos = course['videos']
            
        return render_template('courseVideos.html',title = 'videos',videos = videos)
    
    
    return redirect('/login')
    
    
    
    
# ------------------------------- #
#             routes              #
# ------------------------------- #
