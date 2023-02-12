from app_main import app, db, blogs
from app_main.db import parse_json
from flask import session, abort, render_template, request, redirect



@app.route('/blogs/page/<int:page>')
def blog(page):
    authorized = parse_json(blogs.find({'isAuthorized':'authorized'}))
    total = len(authorized)
    perPage = -9
    end = perPage*page
    start = end+9
    if page == 1:
        start = total
    
    
    mapped = authorized[end:start]
    
    return render_template('blogs.html',title='Blogs',blogs=mapped,page=page,stext='')


@app.route('/blog/<string:key>')
def blogf(key):
    blogd=parse_json(blogs.find_one({'_UID_':key}))
    
    return render_template('blog.html',title='blog',data=blogd)

@app.route('/blogs/add',methods=['GET','POST'])
def addBlogs():
    if 'user' in session or 'admin' in session:
        
        if request.method == 'POST':
            if 'admin' in session:
                userName = 'admin'
            elif 'user' in session:
                userName = session['user']['username']
            data = dict(
                title = request.form['title'],
                tag = request.form['tag'], 
                tags = request.form['tags'].split('|'),
                date = request.form['date'],
                author = request.form['author'],
                banner = request.form['banner'],
                useravater = request.form['useravater'],
                blog = request.form['blog-body'] if request.form['blog-body'].find('<style') == -1 and request.form['blog-body'].find('<script')==-1 else "This blog content has script or style tag",
                userName = userName,
                isAuthorized = 'unauthorized'
                )
            if blogs.find_one(data) == None:
                db.add(data,blogs)
                return render_template('addBlog.html', title="addBlog",alertMessage="blog added wait for authorized")
            return render_template('addBlog.html', title="addBlog",alertMessage="blog already added wait for authorized")

            
        return render_template('addBlog.html',title="add blog")
    abort(404)
    

    
@app.route('/blogs/authorize/<string:state>')
def authorizeBlogs(state):
    if 'admin' in session:
        
        blogsF = parse_json(blogs.find({'isAuthorized':state}))
        
        return render_template('blog_request.html',title="add blog",state=state, blogs = blogsF)
    abort(404)

@app.route('/blog/authorize/<string:key>')
def authorizeBlog(key):
    if 'admin' in session:
        allData = parse_json(blogs.find_one({'_UID_':key}))
        return render_template('blogr.html',title="add blog",allData = allData)
    abort(404)
    
@app.route('/blog/confirm/authorize/<string:key>')
def CmauthorizeBlog(key):
    if 'admin' in session:
        blog = parse_json(blogs.find_one({'_UID_':key}))
        if blog != None:
            db.update({'_UID_':key},{'$set':{'isAuthorized':'authorized'}},blogs)
            
        return redirect('/blog/authorize/'+key)
    abort(404)
    
@app.route('/blog/cancel/authorize/<string:key>')
def CnauthorizeBlog(key):
    if 'admin' in session:
        blog = parse_json(blogs.find_one({'_UID_':key}))
        if blog != None:
            db.update({'_UID_':key},{'$set':{'isAuthorized':'canceled'}},blogs)
            
        return redirect('/blog/authorize/'+key)
    abort(404)

