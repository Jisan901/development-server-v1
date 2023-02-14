from app_main import app
from flask import render_template,make_response




# ------------------------------- #
#             /about              #
# ------------------------------- #

@app.route('/about')
def about():
    return render_template('About.html')
    

# ------------------------------- #
#             /contact            #
# ------------------------------- #    
    
@app.route('/contact')
def contact():
    return render_template('contact.html')
    
# ------------------------------- #
#             routes              #
# ------------------------------- #



# seo 
@app.route('/sitemap.xml')
 
def sitemap ():
     
    res = make_response(render_template('sitemap.xml'))
    res.headers["Content-Type"] = "application/xml"
    return res