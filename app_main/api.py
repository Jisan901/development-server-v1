from app_main import app,web_data
from flask import jsonify, session
from app_main.db import parse_json
from app_main.routes import updateDailyInfo



@app.route('/dashboard/daily_info')
def dashboardApi():
    if 'admin' in session and session['admin']['isLogdin']==True:
        info = updateDailyInfo()
        if info!=None:
            datas = parse_json(web_data.find())
            data=datas[-7:len(datas)]
        else:
            data=[]
        return jsonify(data)
    return jsonify(["bad request found"])

