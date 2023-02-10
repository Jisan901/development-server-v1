from app_main import app
from flask import render_template




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
