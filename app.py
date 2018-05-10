from flask import Flask, render_template,jsonify, make_response, redirect, request, url_for , send_file,session,g,flash
import csv
import ConfigParser
from pymongo import MongoClient
import json
#import xlsxwriter
from datetime import datetime, timedelta
import re
import flask_login
from datetime import datetime, timedelta
import pymongo
from bson.son import SON
import time
import json
from functools import wraps
from bson.objectid import ObjectId
# from cec_authentication import LDAPAuth
from faqdatabase import FaqDatabase
import os
global user_details

user_details = {}
# https://wiki.python.org/moin/TimeComplexity

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)
    session.modified = True
    g.user = flask_login.current_user


def is_logged_in(f) :
   @wraps(f)
   def wrap(*args,**kwargs):
       if 'user' in session:
           return f(*args, **kwargs)
       else:
           return redirect (url_for ('login'))
   return wrap

@app.route('/home')
def login():
    return render_template('index.html',action=url_for('authentication'))


@app.route('/login', methods=["GET","POST"])
def authentication():
    if request.method == 'POST':
        session.pop('user',None)
        username = request.form["Username"]
        # user_cec = LDAPAuth()
        managers = ['argangul', 'dpatwa', 'mnamasev', 'rajestiw', 'vabs', 'gbkumar', 'jlouis', 'sgohil', 'shekar',
                    'yblanche', 'yviswesw']
        """if request.form["Username"] and request.form["Password"] :
            authentic = user_cec.auth(request.form["Username"],request.form["Password"])
            if authentic :
                session['user'] = request.form['Username']
                if request.form['Username'] in managers :
                    return redirect(url_for('manager'))
                else :
                    return redirect(url_for('user'))
            else :
                return render_template('login_new_style.html')"""

        if request.form["Username"] and request.form["Password"]:
            # if request.form['Username'] in managers:
            #     if request.form["Password"] == "Password" :
            #         return redirect(url_for('manager'))
            if request.form["Password"] == "Password":
                session['user'] = request.form['Username']
                user_fullname = os.popen("/usr/cisco/bin/fullname.pl " + request.form['Username']).read().split('\n')[0]
                if user_fullname is None:
                    user_fullname = request.form['Username']
                session ['user_fullname'] = user_fullname
                user_details ['user_fullname'] = user_fullname
                return redirect(url_for('home'))
            else :
                return render_template('index.html')
    return render_template ('index.html')
    # return render_template('login_new_style.html')


@app.route('/', methods=["GET", "POST"])
@is_logged_in
def home():
    print("am in home")
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    print(session ['user_fullname'])
    return render_template("home.html",user=user)


@app.route('/submitfaq')
@is_logged_in
def submitfaq():
    print("am in home")
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    return render_template("submit_faq.html",user=user)


@app.route("/faqsubmitted", methods=["GET", "POST"])
@is_logged_in
def faqsubmitted():

    """ Here we collect the data submitted and will insert it to Database"""
    try :
        if not session ['user']:
            return redirect (url_for ('login'))
        else:
            user = session ['user']
        if request.method == "POST":
            title = request.form["title"]
            device = request.form["device"]
            answer = request.form["answer"]
            user = user
            l2_l3_infra = request.form["l2_l3_infra"]
            if str(l2_l3_infra) == "L2":
                feature = request.form["l2_feature"]
            elif l2_l3_infra == "L3":
                feature = request.form["l3_feature"]
            elif l2_l3_infra == "INFRA":
                feature = request.form ["infra_feature"]
            else:
                feature = ""
                l2_l3_infra = ""
            # Full name
            # user_fullname = os.popen("/usr/cisco/bin/fullname.pl " + user).read().split('\n')[0]
            # if user_fullname is None:
            #     user_fullname = user
            org = os.popen("/usr/cisco/bin/rchain -P " + user).read()
            org_str = re.findall(r'\n(\w+)', org)
            dir_info = ""
            for st in org_str:
                dir_info += st + "::"
            submitter_manager_org = dir_info.strip("::")
            "username, title, device, feature, answer, submitter_manager_org"
            faq_obj = FaqDatabase()
            inser_faq = faq_obj.insert(user, title, device, feature, answer, submitter_manager_org)
            if inser_faq is True :
                flash("Successfully submitted the FAQ, Thanks")
            else :
                flash("OOPs something went wrong can't submit the FAQ, Please try again later.")
            return render_template("home.html", user=user)
        else:
            return render_template("home.html", user=user)
    except Exception as e:
        if not session ['user']:
            return redirect (url_for ('login'))
        else:
            user = session ['user']
        print(e)
        return render_template("home.html", user=user)


@app.route("/viewfaq")
@is_logged_in
def viewfaq():
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    return render_template("viewfaq.html" ,user=user)


@app.route("/faq", methods=["GET", "POST"])
@is_logged_in
def faq():
    if request.method == "POST":
        if not session ['user']:
            return redirect (url_for ('login'))
        else:
            user = session ['user']
        faq_obj = FaqDatabase ()
        device = request.form["device"]
        l2_l3_infra = request.form ["l2_l3_infra"]
        if str (l2_l3_infra) == "L2":
            feature = request.form ["l2_feature"]
        elif l2_l3_infra == "L3":
            feature = request.form ["l3_feature"]
        elif l2_l3_infra == "INFRA":
            feature = request.form ["infra_feature"]
        else:
            print ("Not a valid input")
            feature = ""
            l2_l3_infra = ""
        # feature = request.form["feature"]
        faq_rec = faq_obj.findfaq(device, feature)
        if faq_rec is not False:
            faq_data = []
            for record in faq_rec:
                rec_id = str(record['_id'])
                title = record['title']
                submitter = record["submitter-id"]
                view = record["views"]
                print("in /faq"+ str(view))
                faq_data.append((title, submitter, rec_id,view))
            return render_template("faq.html", user=user, device=device, faq_data=faq_data)
        return render_template("viewfaq.html", user=user)


# # device = "Fretta"
        # # title = "QPPB Support on Fretta in 651 release"
        # # username = "ikyalnoo"
        # # title2 = "QPPB Support on Fretta in 651 release"
        # # username2 = "ikyalnoo"
        # # answer2 = "Yes Supported"
        # # answer = """
        # # Yes Supported
        # # """
        # # num = "5ac791258614d9424a8b942f"
        # # num1 = "5ac791258614d9424a8b1111"
        # # num2 = "5ac791258614d9424a8b2222"
        # # answer = json.dumps(irf)
        #
        # # answer = JSON()
        # faq_data = [(title, username, answer,num),(title2, username2, answer2,num1), (title2, username2, answer2,num2), (title2, username2, answer2,num)]


@app.route("/<route>/<faqid>")
@is_logged_in
def faqid(route,faqid):
    # faqid = str(faqid)
    faq_obj = FaqDatabase ()
    view = faq_obj.updateview (faqid)
    print(view)
    faq_rec = faq_obj.findrecord(faqid)
    route = route
    answer = dict()
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    if faq_rec is not False:
        for rec in faq_rec:
            device = rec["device"]
            title = rec["title"]
            answer = rec["answer"]
            submitter = rec["submitter-id"]
            likes = rec["likes"]
            created = rec["created_on"]
            rec_id = str (rec ['_id'])
            views = rec["views"]
            return render_template("faqdetails.html", device=device,views=views, route=route, rec_id=rec_id, user=user, title=title, answer=answer, submitter=submitter, created=created)
    # d = db.find ({'_id': ObjectId ('5ac791258614d9424a8b942f')})
    return render_template ("home.html" , user=user)


@app.route("/edit/<recid>")
@is_logged_in
def editfaq(recid):
    # faqid = str(recid)
    faq_obj = FaqDatabase ()
    faq_rec = faq_obj.findrecord(recid)
    answer = dict()
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    if faq_rec is not False:
        for rec in faq_rec:
            title = rec["title"]
            answer = rec["answer"]
            rec_id = str (rec ['_id'])
            return render_template("editfaqtiny.html", rec_id=rec_id, user=user, title=title, answer=answer)
    # d = db.find ({'_id': ObjectId ('5ac791258614d9424a8b942f')})
    return render_template ("home.html" , user=user)


@app.route("/update/<recid>", methods=["GET", "POST"])
@is_logged_in
def updatefaq(recid):
    # faqid = str(faqid)
    answer = dict()
    if not session ['user']:
        return redirect (url_for ('login'))
    else:
        user = session ['user']
    try:
        if request.method == "POST":
            title = request.form ["title"]
            device = request.form ["device"]
            answer = request.form ["answer"]
            user = user
            l2_l3_infra = request.form ["l2_l3_infra"]
            if str (l2_l3_infra) == "L2":
                feature = request.form ["l2_feature"]
            elif l2_l3_infra == "L3":
                feature = request.form ["l3_feature"]
            elif l2_l3_infra == "INFRA":
                feature = request.form ["infra_feature"]
            else:
                print ("Not a valid input")
                feature = ""
                l2_l3_infra = ""
            faq_obj = FaqDatabase ()
            faq_obj_res = faq_obj.updatefaq(recid,title,device,feature,answer)
            print(faq_obj_res)
            if faq_obj_res is not False:
                return redirect (url_for ('faqid', route="updated", faqid=recid))
                # faq_rec = faq_obj.findrecord (recid)
                # if faq_rec is not False:
                #     for rec in faq_rec:
                #         device = rec ["device"]
                #         title = rec ["title"]
                #         answer = rec ["answer"]
                #         submitter = rec ["submitter-id"]
                #         likes = rec ["likes"]
                #         created = rec ["created_on"]
                #         rec_id = str (rec ['_id'])
                #         return render_template ("faqdetails.html", device=device, rec_id=rec_id, user=user, title=title,
                #             answer=answer, submitter=submitter, created=created)
                #         # d = db.find ({'_id': ObjectId ('5ac791258614d9424a8b942f')})
            return render_template ("home.html", user=user)
        else:
            return render_template ("home.html", user=user)
    except Exception as e:
        print (e)
        return render_template ("home.html", user=user)


@app.route("/logout")
def logout():
        session.pop('user', None)
        session.pop('user_fullname', None)
        g.user = None
        return render_template('index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50405, debug=True, threaded=True, )
