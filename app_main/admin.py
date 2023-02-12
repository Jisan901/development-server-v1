from app_main import app, courses, db,course_req, users, web_data
from flask import render_template, session, request, redirect
from app_main.db import parse_json
from app_main.routes import updateDailyInfo


@app.route('/courses/manage',methods=['GET','POST'])
def manageCourse():
    if 'admin' in session:
        return render_template('courseAdmin.html',title='Management course',courses=parse_json(courses.find()))
    return '<h1>404 not found</h1>'
    

@app.route('/courses/manage/add',methods=['GET','POST'])
def addCourse():
    if 'admin' in session:
        if request.method=='POST':
            data = parse_json(dict(
            title = request.form['title'],
            fee = request.form['fee'],
            duration = request.form['duration'],
            internduration = request.form['internduration'],
            # splitting str <---> list
            jobfields = request.form['jobfields'].split('|'),
            courseContent = request.form['courseContent'].split('|'),
            softwares = request.form['softwares'].split('|'),
            tags = request.form['tags'].split("|"),
            # splitting end
            courseDesc = request.form['courseDesc'],
            tag = request.form['tag'],
            author = request.form['author'],
            banner = request.form['banner'],
            useravater = request.form['useravater'],
            videos=[]
            ))
            
            db.add(data,courses)
            return redirect('/courses/manage')
            
            
        return render_template('add_course.html',title='Management course',act="/add")
    return '<h1>404 not found</h1>'
    
@app.route('/courses/manage/update/<string:nameC>',methods=['GET','POST'])
def updateCourse(nameC):
    if 'admin' in session:
        if request.method=='POST':
            data = parse_json(dict(
            title = request.form['title'],
            fee = request.form['fee'],
            duration = request.form['duration'],
            internduration = request.form['internduration'],
            # splitting str <---> list
            jobfields = request.form['jobfields'].split('|'),
            courseContent = request.form['courseContent'].split('|'),
            softwares = request.form['softwares'].split('|'),
            tags = request.form['tags'].split("|"),
            # splitting end
            courseDesc = request.form['courseDesc'],
            tag = request.form['tag'],
            author = request.form['author'],
            banner = request.form['banner'],
            useravater = request.form['useravater']
            ))
            if courses.find_one({"_UID_":nameC})!=None:
                db.update({"_UID_":nameC},{"$set":data},courses)
                return redirect('/courses/manage')
            
            
            return render_template('add_course.html',alertMessage="course index not found "+nameC,act="/update/"+str(nameC),title="Management course",data=parse_json(courses.find_one({"_UID_":nameC})))
        return render_template('add_course.html',title='Management course',act="/update/"+str(nameC),data=parse_json(courses.find_one({"_UID_":nameC})))
    return '<h1>404 not found</h1>'
    
@app.route('/courses/manage/add_video/<string:nameC>',methods=['GET','POST'])
def addVideo(nameC):
    if 'admin' in session:
        old_c = parse_json(courses.find_one({"_UID_":nameC}))

        if old_c!=None:
            videos = old_c['videos']
            if request.method=='POST':
                data = parse_json(dict(
                title = request.form['title'],
                link = request.form['link'],
                duration = request.form['duration'],
                bannerLink = request.form['bannerLink']))
                

                videos.append(data)
                db.update({"_UID_":nameC},{"$set":{
                    'videos':videos
                }},courses)
                return redirect('/courses/manage/add_video/'+str(nameC))
                
            #return render_template('Add_video.html',alertMessage="course index not found "+str(nameC),act=nameC,title="Management course",videos=videos)
        return render_template('Add_video.html',title='Management course',act=nameC,videos=videos)
    return '<h1>404 not found</h1>'
    
@app.route('/courses/manage/delete/<string:name>')
def deleteCourse(name):
    if 'admin' in session:
        if courses.find_one({"_UID_":name})!=None:
            db.delete({"_UID_":name},courses)
            return redirect('/courses/manage')
    return '<h1>404 not found</h1>'
    


@app.route('/request/courses/<string:order>')
def requestC(order):
    if order == 'pending' or order=='completed' or order=='canceled':
        if 'admin' in session:
            allData=parse_json(course_req.find({"state":order}))
            
            return render_template('Request.courses.bootstrap.html',allData=allData,order=order)
        return redirect('/login')
    elif order == 'my':
        if 'user' in session:
            allData=parse_json(course_req.find({"urserId":session['user']['username']}))
        
            return render_template('Request.courses.bootstrap.html',allData=allData,order=order)

        return redirect('/login')
    return 'invalid url'
        
        
@app.route('/request/course/<string:opt>/<string:key>')
def handleReq(opt,key):
    info = updateDailyInfo()
    if opt == 'view' and 'admin' in session or opt=='complete' or opt=='cancel':
        if 'admin' in session:
            

            allData=parse_json(course_req.find_one({"_UID_":key}))
            course = parse_json(courses.find_one({'_UID_':allData['courseId']}))
            print('out complete')
            if opt=='complete' and course_req.find_one({'_UID_':key,'state':'complete'})==None:
                print('in complete')
                user = parse_json(users.find_one({"username":allData['urserId']}))
                
                db.update({'_UID_':key,'state':'pending'},{'$set':{'state':'completed'}},course_req)
                db.update({'_UID_':key,'state':'canceled'},{'$set':{'state':'completed'}},course_req)
                db.update({'username':allData['urserId']},{
                    '$set':{
                        'paid_courses':user['paid_courses']+[allData['courseId']],
                        'spend_for_courses':user['spend_for_courses']+int(course['fee'])
                    }
                },users)
                if info!=None:
                    db.update({"date":info['date']},{'$set':{"sellout_amount":info["sellout_amount"]+int(course['fee']),"sell_courses":info['sell_courses']+[key]}},web_data)

                return redirect('/request/course/view/'+str(key))
            elif opt == 'cancel':
                db.update({'_UID_':key},{'$set':{'state':'canceled'}},course_req)
                return redirect('/request/course/view/'+str(key))
            
            return render_template('request.details.html',allData=allData,order=opt,user=False,course=course)
        return redirect('/login')
        
        
    elif opt == 'view':
        if 'user' in session:
            
            
            allData=parse_json(course_req.find_one({"urserId":session['user']['username'],"_UID_":key}))
            course = parse_json(courses.find_one({'_UID_':allData['courseId']}))
            return render_template('request.details.html',allData=allData,order=opt,user=True,course=course)

        return redirect('/login')
    return 'invalid url'
    
    
    
    
@app.route('/users')
def userAll ():
    if 'admin' in session:
        usera = parse_json(users.find())
        return render_template('users.html',users=usera)
    return '404'