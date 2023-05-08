import demjson
from flask import Flask,render_template,request,redirect,session
import datetime

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

from DBConnection import Db

app = Flask(__name__)
app.secret_key="career"
static_path=r"D:\project\Career_Recommendation_System\static\\"


@app.route('/')
def loginn():
    db=Db()
    qry=db.select("select * from career_expert,login where career_expert.expert_id=login.login_id and login.usertype='career_expert'")
    qry1=db.select("select * from feedback,user where feedback.user_id=user.user_id")
    return render_template("login_index.html",data=qry,data1=qry1)

@app.route('/login',methods=['post'])
def login1():
    na = request.form['un']
    pw = request.form['ps']
    db = Db()
    res = db.selectOne("select * from login where username='" + na + "'and password='" + pw + "'")
    if res is not None:
        if res['usertype'] == "admin":
            session['lin'] = 'lin'
            return redirect('/admin_home')
        elif res['usertype'] == "career_expert":
            session['lid'] = res['login_id']

            session['lin'] = 'lin'
            return redirect('/career_home')
        elif res['usertype'] == "user":
            session['lid'] = res['login_id']

            session['lin'] = 'lin'
            return redirect('/user_home')
        else:
            return '<script>alert("Invalid details!!");window.location="/"</script>'
    else:
        return '<script>alert("User not found");window.location="/"</script>'

@app.route('/reg')
def reg():
    return render_template('reg_index.html')

# =================================================================================================================================
#                                                 ADMIN MODULE
# =================================================================================================================================


@app.route('/admin_home')
def admin_home():
    if session['lin']=='lin':
        return render_template('admin/admin_index.html')
    else:
        return redirect('/')

@app.route('/view_career_expert')
def view_career_expert():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from career_expert,login WHERE career_expert.expert_id=login.login_id and login.usertype='pending'  ")
        return render_template("admin/view_career_expert.html", a=qry)
    else:
        return redirect('/')


@app.route('/approve_career_expert/<cid>')
def approve_career_expert(cid):
    if session['lin']=='lin':
        db=Db()
        db.update("update login set usertype='career_expert' where login_id='"+cid+"'")
        return redirect('/view_career_expert#cta')

    else:
        return redirect('/')

@app.route('/reject_career_expert/<cid>')
def reject_career_expert(cid):
    if session['lin']=='lin':
        db=Db()
        db.delete("delete from login where login_id='"+cid+"'")
        db.delete("delete from career_expert where expert_id='"+cid+"'")
        return redirect('/view_career_expert#cta')

    else:
        return redirect('/')


@app.route('/view_approved_career_expert')
def view_approved_career_expert():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from career_expert,login WHERE career_expert.expert_id=login.login_id and login.usertype='career_expert' ")
        return render_template("admin/view_approved_career_expert.html", a=qry)
    else:
        return redirect('/')


@app.route('/view_user')
def view_user():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from user  ")
        print(qry)
        return render_template("admin/view_users.html", a=qry)
    else:
        return redirect('/')


@app.route('/view_feedback')
def view_feedback():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from feedback,user where feedback.user_id=user.user_id")
        return render_template('admin/view_feedback.html',a=qry)
    else:
        return redirect('/')


@app.route('/view_complaint')
def view_complaint():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from complaint,user where complaint.user_id=user.user_id ")
        return render_template("admin/view_Complaint.html", a=qry)
    else:
        return redirect('/')

@app.route('/reply/<cid>')
def reply(cid):
    if session['lin']=='lin':
        return render_template('admin/send_reply.html',c=cid)
    else:
        return redirect('/')


@app.route('/reply1/<a>', methods=['post'])
def reply1(a):
    if session['lin'] == "lin":

            db = Db()
            rply = request.form['textarea']
            qry = db.update(
                "update complaint set reply='" + rply + "',r_date=curdate() where complaint_id='" + a + "'")
            return '<script>alert("Success");window.location="/view_complaint#aa"</script>'

    else:
        return redirect('/')

# ==============================================================================================================================
#                                         CAREER EXPERT MODULE
# ==============================================================================================================================

@app.route('/career_expert_reg',methods=['post'])
def career_expert_reg():
    n=request.form['n']
    e=request.form['e']
    ph=request.form['ph']
    q=request.form['q']
    h=request.form['h']
    po=request.form['p']
    pi=request.form['pi']
    im=request.files['im']
    date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    im.save(static_path + "career_expert_img\\"+date+'.jpg')
    path="/static/career_expert_img/"+date+'.jpg'
    ps=request.form['ps']
    cp=request.form['rp']
    db=Db()
    qry=db.selectOne("select * from login where username='"+e+"'")
    if qry is not None:
        return '''<script>alert('Email already exist!');window.location="/reg"</script>'''
    else:
        if ps==cp:
            qry1=db.insert("insert into login VALUES ('','"+e+"','"+cp+"','pending')")
            db.insert("insert into career_expert VALUES ('"+str(qry1)+"','"+n+"','"+e+"','"+ph+"','"+q+"','"+h+"','"+po+"','"+pi+"','"+str(path)+"')")
            return '''<script>alert('Registeration success!!');window.location="/"</script>'''
        else:
            return '''<script>alert('Password incorrect!!');window.location="/reg"</script>'''


@app.route('/career_home')
def career_home():
    if session['lin'] == 'lin':
        return render_template('career_expert/career_index.html')
    else:
        return redirect('/')

@app.route('/view_profile')
def view_profile():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.selectOne("select * from career_expert where expert_id='" + str(session['lid']) + "'")
        return render_template('career_expert/view_profile.html', data=qry)
    else:
        return redirect('/')

@app.route('/view_followers')
def view_followers():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select(
            "select * from follower,user where follower.user_id=user.user_id and follower.expert_id='" + str(
                session['lid']) + "' and follower.status='follow'")
        return render_template('career_expert/view_followers.html', data=qry)
    else:
        return redirect('/')

@app.route('/ph_user_chat1/<uid>')
def ph_user_chat1(uid):
    if session['lin'] == "lin":

        return render_template("career_expert/ecpert_user_Chat.html", u=uid)
    else:
        return redirect('/')

@app.route('/chatsnd1/<u>', methods=['post'])
def chatsnd1(u):
    if session['lin'] == "lin":

        db = Db()
        c = session['lid']
        b = request.form['n']
        print(b)
        m = request.form['m']

        q2 = "insert into chat values(null,'" + m + "','" + str(c) + "','" + str(u) + "',now())"
        res = db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return redirect('/')

@app.route('/chatrply1', methods=['post'])
def chatrply1():
    if session['lin'] == "lin":

        print("...........................")
        c = session['lid']
        t = Db()
        qry2 = "select * from chat ORDER BY chat_id ASC ";
        res = t.select(qry2)
        print(res, )

        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
            v['id'] = c
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        return rw
    else:
        return redirect('/')

@app.route('/add_tips')
def add_tips():
    if session['lin'] == 'lin':
        return render_template('career_expert/add_tips.html')
    else:
        return redirect('/')

@app.route('/add_tips1', methods=['post'])
def add_tips1():
    if session['lin'] == 'lin':
        t = request.form['t']
        c = request.form['c']
        db = Db()
        db.insert(
            "insert into tips VALUES ('',curdate(),'" + str(session['lid']) + "','" + t + "','" + c + "')")
        return '<script>alert("Successfully added");window.location="/career_home"</script>'
    else:
        return redirect('/')

@app.route('/view_tips')
def view_tips():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from tips where expert_id='" + str(session['lid']) + "'")
        return render_template('career_expert/view_tips.html', a=qry)
    else:
        return redirect('/')

@app.route('/update_tips/<tid>')
def update_tips(tid):
    if session['lin'] == 'lin':
        db = Db()
        qry = db.selectOne("select * from tips where tips_id='" + tid + "'")
        return render_template('career_expert/edit_tips.html', data=qry, t=tid)
    else:
        return redirect('/')

@app.route('/update_tips1/<tid>', methods=['post'])
def update_tips1(tid):
    if session['lin'] == 'lin':
        t = request.form['t']
        c = request.form['c']
        db = Db()
        db.update(
            "update tips set date=curdate(),title='" + t + "',content='" + c + "' where tips_id='" + tid + "'")
        return '<script>alert("Successfully updated");window.location="/view_tips#cta"</script>'
    else:
        return redirect('/')

@app.route('/delete_tips/<tid>')
def delete_tips(tid):
    if session['lin'] == 'lin':
        db = Db()
        db.delete("delete from tips where tips_id='" + tid + "'")
        return redirect('/view_tips#cta')
    else:
        return redirect('/')

@app.route('/add_vaccancy')
def add_vaccancy():
    if session['lin'] == 'lin':
        return render_template('career_expert/add_vaccancy.html')
    else:
        return redirect('/')

@app.route('/add_vaccancy1', methods=['post'])
def add_vaccancy1():
    if session['lin'] == 'lin':
        cn = request.form['cn']
        p = request.form['ps']
        q = request.form['q']
        v = request.form['v']
        l = request.form['ld']
        db = Db()
        db.insert("insert into vaccancy VALUES ('','" + str(
            session['lid']) + "',curdate(),'" + cn + "','" + p + "','" + v + "','" + l + "','" + q + "')")
        return '<script>alert("Successfully added");window.location="/career_home"</script>'
    else:
        return redirect('/')

@app.route('/view_vaccancy')
def view_vaccancy():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from vaccancy where expert_id='" + str(session['lid']) + "'")
        return render_template('career_expert/view_vaccancy.html', a=qry)
    else:
        return redirect('/')

@app.route('/update_vaccancy/<tid>')
def update_vaccancy(tid):
    if session['lin'] == 'lin':
        db = Db()
        qry = db.selectOne("select * from vaccancy where vaccancy_id='" + tid + "'")
        return render_template('career_expert/edit_vaccancy.html', data=qry, t=tid)
    else:
        return redirect('/')

@app.route('/update_vaccancy1/<tid>', methods=['post'])
def update_vaccancy1(tid):
    if session['lin'] == 'lin':
        cn = request.form['cn']
        p = request.form['ps']
        q = request.form['q']
        v = request.form['v']
        l = request.form['ld']
        db = Db()
        db.update(
            "update vaccancy set date=curdate(),company_name='" + cn + "',post='" + p + "',no_of_vaccancy='" + v + "',last_date='" + l + "',qualifications='" + q + "' where vaccancy_id='" + tid + "'")
        return '<script>alert("Successfully updated");window.location="/view_vaccancy#cta"</script>'
    else:
        return redirect('/')

@app.route('/delete_vaccancy/<tid>')
def delete_vaccancy(tid):
    if session['lin'] == 'lin':
        db = Db()
        db.delete("delete from vaccancy where vaccancy_id='" + tid + "'")
        return redirect('/view_vaccancy')
    else:
        return redirect('/')

@app.route('/apprating')
def ar():
    # qry="select rating.*,customer.* from rating,customer where customer.lid=rating.user_id"
    db = Db()
    qry = "select rating.rating,rating.date,user.uname,user.uimage,rating.rating_id from user,rating where user.user_id=rating.user_id and rating.expert_id='" + str(
        session['lid']) + "' order by rating_id desc"
    res = db.select(qry)

    ar_rt = []

    for im in range(0, len(res)):
        val = str(res[im]['rating'])
        ar_rt.append(val)
    fs = "/static/star/full.jpeg"
    hs = "/static/star/half.jpeg"
    es = "/static/star/empty.jpeg"
    arr = []

    for rt in ar_rt:
        print(rt)
        a = float(rt)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            arr.append(ar)

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            arr.append(ar)

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            arr.append(ar)

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            arr.append(ar)

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            arr.append(ar)

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            arr.append(ar)

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            arr.append(ar)

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            arr.append(ar)

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            arr.append(ar)

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            arr.append(ar)

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            arr.append(ar)
        print(arr)
    # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
    return render_template('career_expert/vew_ raiting.html', resu=res, r1=arr, ln=len(arr))


# ==============================================================================================================================
#                                         USER MODULE
# ==============================================================================================================================


@app.route('/user_reg', methods=['post'])
def user_reg():
    n = request.form['n']
    e = request.form['e']
    ph = request.form['ph']
    h = request.form['h']
    po = request.form['p']
    pi = request.form['d']
    im = request.files['im']
    g = request.form['RadioGroup1']
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    im.save(static_path + "userimg\\" + date + '.jpg')
    path = "/static/userimg/" + date + '.jpg'
    ps = request.form['ps']
    cp = request.form['rp']
    db = Db()
    qry = db.selectOne("select * from login where username='" + e + "'")
    if qry is not None:
        return '''<script>alert('Email already exist!');window.location="/reg"</script>'''
    else:
        if ps == cp:
            qry1 = db.insert("insert into login VALUES ('','" + e + "','" + cp + "','user')")
            db.insert("insert into user VALUES ('" + str(
                qry1) + "','" + n + "','" + e + "','" + ph + "','" + h + "','" + po + "','" + pi + "','" + str(
                path) + "','" + g + "')")
            return '''<script>alert('Registeration success!!');window.location="/"</script>'''
        else:
            return '''<script>alert('Password incorrect!!');window.location="/reg"</script>'''

@app.route('/user_home')
def user_home():
    if session['lin'] == 'lin':
        return render_template('user/user_index.html')
    else:
        return redirect('/')

@app.route('/view_user_profile')
def view_user_profile():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.selectOne("select * from user where user_id='" + str(session['lid']) + "'")
        return render_template('user/view_user_profile.html', data=qry)
    else:
        return redirect('/')

@app.route('/view_user_career_expert')
def view_user_career_expert():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select(
            "select * from career_expert left join login on career_expert.expert_id=login.login_id left join follower on career_expert.expert_id=follower.expert_id where login.usertype='career_expert' ")
        return render_template("user/view_career_expert.html", a=qry)
    else:
        return redirect('/')

@app.route('/send_follow/<eid>')
def send_follow(eid):
    if session['lin'] == "lin":
        db = Db()
        qry1 = db.selectOne("select * from follower where expert_id='" + eid + "' and user_id='" + str(
            session['lid']) + "' and status='unfollow' ")
        if qry1 is not None:
            f = qry1['follower_id']
            db.update("update  follower set status='follow' where follower_id='" + str(f) + "'")
            return redirect('/view_user_career_expert#cta')

        else:
            qry = db.insert(
                "insert into follower VALUES ('','" + eid + "','" + str(session['lid']) + "','follow')")
            return redirect('/view_user_career_expert#cta')
    else:
        return redirect('/')

@app.route('/send_unfollow/<eid>')
def send_unfollow(eid):
    if session['lin'] == "lin":
        db = Db()
        # qry1=db.selectOne("select * from follower where expert_id='"+eid+"' and user_id='"+str(session['lid'])+"' and status='follow' ")
        qry = db.update("update follower set status='unfollow' where expert_id='" + eid + "'")
        return redirect('/view_user_career_expert#cta')
    else:
        return redirect('/')

@app.route('/view_following_expert')
def view_following_expert():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from career_expert,follower where career_expert.expert_id=follower.expert_id and follower.status='follow' ")
        return render_template('user/view_following_career_expert.html', a=qry)
    else:
        return redirect('/')

@app.route('/view_user_tips/<eid>')
def view_user_tips(eid):
    if session['lin'] != 'lin':
        return redirect('/')
    db = Db()
    qry = db.select("select * from tips where expert_id='" + eid + "'")
    return render_template('user/view_tips.html', data=qry)

@app.route('/view_user_vaccancy/<eid>')
def view_user_vaccancy(eid):
    if session['lin'] != 'lin':
        return redirect('/')
    db = Db()
    qry = db.select("select * from vaccancy where expert_id='" + eid + "'")
    return render_template('user/view_vaccancy.html', data=qry)

@app.route('/send_complaint')
def send_complaint():
    if session['lin'] != 'lin':
        return redirect('/')
    return render_template('user/send_complaint.html')

@app.route('/send_complaint1', methods=['post'])
def send_complaint1():
    if session['lin'] != 'lin':
        return redirect('/')
    c = request.form['textarea']
    db = Db()
    db.insert("insert into complaint VALUES ('','" + str(
        session['lid']) + "','" + c + "',curdate(),'pending','pending')")
    return '<script>alert("Successfully Sended");window.location="/user_home"</script>'

@app.route('/send_rating/<cid>')
def send_rating(cid):
    if session['lin'] != 'lin':
        return redirect('/')
    return render_template('user/rate.html', c=cid)

@app.route('/send_rating1', methods=['post'])
def send_rating1():
    if session['lin'] != 'lin':
        return redirect('/')
    r = request.form['star']
    cid = request.form['cid']
    db = Db()
    qry = db.selectOne(
        "select * from rating where user_id='" + str(session['lid']) + "' and expert_id='" + cid + "' ")
    if qry is not None:
        rid = qry['rating_id']
        db.update("update rating set rating='" + r + "' where rating_id='" + str(rid) + "' ")
        return '<script>alert("Successfully Sended");window.location="/user_home"</script>'

    else:
        db.insert(
            "insert into rating VALUES ('',curdate(),'" + str(session['lid']) + "','" + cid + "','" + r + "')")
        return '<script>alert("Successfully Sended");window.location="/user_home"</script>'

@app.route('/view_reply')
def view_reply():
    if session['lin'] != 'lin':
        return redirect('/')
    db = Db()
    qry = db.select("select * from complaint where user_id='" + str(session['lid']) + "'")
    return render_template('user/view_replyt.html', data=qry)

@app.route('/send_feedback')
def send_feedback():
    return render_template('user/send_feedback.html')

@app.route('/send_feedback1', methods=['post'])
def send_feedback1():
    f = request.form['textarea']
    db = Db()
    db.insert("insert into feedback VALUES ('','" + str(session['lid']) + "',curdate(),'" + f + "')")
    return '<script>alert("Successfully Sended");window.location="/user_home"</script>'

@app.route('/view_user_feedback')
def view_user_feedback():
    db = Db()
    qry = db.select("select * from feedback,user where feedback.user_id=user.user_id")
    return render_template('user/view_feedback.html', data=qry)

@app.route('/user_apprating/<eid>')
def user_apprating(eid):
    # qry="select rating.*,customer.* from rating,customer where customer.lid=rating.user_id"
    db = Db()
    qry = "select rating.rating,rating.date,user.uname,user.uimage,rating.rating_id from user,rating where user.user_id=rating.user_id and rating.expert_id='" + eid + "' order by rating_id desc"
    res = db.select(qry)

    ar_rt = []

    for im in range(0, len(res)):
        val = str(res[im]['rating'])
        ar_rt.append(val)
    fs = "/static/star/full.jpeg"
    hs = "/static/star/half.jpeg"
    es = "/static/star/empty.jpeg"
    arr = []

    for rt in ar_rt:
        print(rt)
        a = float(rt)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            arr.append(ar)

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            arr.append(ar)

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            arr.append(ar)

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            arr.append(ar)

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            arr.append(ar)

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            arr.append(ar)

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            arr.append(ar)

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            arr.append(ar)

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            arr.append(ar)

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            arr.append(ar)

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            arr.append(ar)
        print(arr)
    # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
    return render_template('user/view_rating.html', resu=res, r1=arr, ln=len(arr))

        # -----------------chat-------------------------------------


@app.route('/ph_user_chat/<uid>')
def ph_user_chat(uid):
    if session['lin'] == "lin":

        return render_template("user/user_career_chat.html", u=uid)
    else:
        return redirect('/')

@app.route('/chatsnd/<u>', methods=['post'])
def chatsnd(u):
    if session['lin'] == "lin":

        db = Db()
        c = session['lid']
        b = request.form['n']
        print(b)
        m = request.form['m']

        q2 = "insert into chat values(null,'" + str(c) + "','" + str(u) + "',curdate(),curtime(),'" + m + "')"
        res = db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return redirect('/')

@app.route('/chatrply', methods=['post'])
def chatrply():
    if session['lin'] == "lin":

        print("...........................")
        c = session['lid']
        t = Db()
        qry2 = "select * from chat ORDER BY chat_id ASC ";
        res = t.select(qry2)
        print(res, )

        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
            v['id'] = c
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        return rw
    else:
        return redirect('/')


# ==============================================MAIN SECTION====================================================================
#
# @app.route('/load_dataset')
# def load_dataset():
#     import pandas as pd
#     data = pd.read_csv(static_path + "dataset\\career_choices.csv")
#     print(data)
#     # print(data.shape)
#     # print(data.head)
#     attributes = data.values[:1000, 0:28]
#     labels = data.values[:1000, 28]
#
#     attributes1 = data.values[:900, 0:28]
#     labels1 = data.values[:900, 28]
#     # print("ATTRIBUTES",attributes)
#     # print("LABELS",labels)
#     X_train, X_test, y_train, y_test = train_test_split(attributes, labels, test_size=0.2)
#     #
#     #
#     rf = RandomForestClassifier(n_estimators=100)
#     rf.fit(attributes1, labels1)
#     y_pred_rf = rf.predict(X_test)
#     print(y_pred_rf)
#     acc = accuracy_score(y_test, y_pred_rf)
#     acc_rf = round(acc * 100, 2)
#     print("R", acc_rf)
#
#     #
#     svm = LinearSVC()
#     # svm.fit(X_train,y_train)
#     svm.fit(attributes1, labels1)
#     y_pred_svm = svm.predict(X_test)
#     acc = accuracy_score(y_test, y_pred_svm)
#     acc_sv = round(acc * 100, 2)
#     print("S", acc_sv)
#
#     #
#     nb = GaussianNB()
#     # nb.fit(X_train, y_train)
#     nb.fit(attributes1, labels1)
#     y_pred_nb = nb.predict(X_test)
#     acc = accuracy_score(y_test, y_pred_nb)
#     acc_nb = round(acc * 100, 2)
#     print("N", acc_nb)
#
#     import os
#     import numpy as np
#     import matplotlib.pyplot as plt
#
#     x = ["Random Forest", "SVM", "Naive Bayes"]
#     y = [acc_rf, acc_sv, acc_nb]
#     # plt.bar(x, y)
#     fig, ax=plt.subplots()
#     bar1=ax.bar(x, y)
#     ax.set_xticks(x)
#     ax.bar_label(bar1)
#     ax.legend()
#
#     plt.show()
#     # fig, ax = plt.subplots()
#     # width = 0.75
#     # ind = np.arange(len(y))
#     #
#     # ax.barh(ind, y, width, color="green")
#     #
#     # for i, v in enumerate(y):
#     #     ax.text(v + 3, i + .25, str(v),
#     #             color='blue', fontweight='bold')
#     # plt.show()
#     # plt.savefig()
#
#     return "ok"


# ---------------



@app.route('/load_dataset')
def load_dataset():
    import pandas as pd
    data = pd.read_csv(static_path + "dataset\\career_choices.csv")
    print(data)
    # print(data.shape)
    # print(data.head)
    attributes = data.values[:1000, 0:28]
    labels = data.values[:1000, 28]

    attributes1 = data.values[:900, 0:28]
    labels1 = data.values[:900, 28]
    # print("ATTRIBUTES",attributes)
    # print("LABELS",labels)
    X_train, X_test, y_train, y_test = train_test_split(attributes, labels, test_size=0.2)
    #
    #
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(attributes1, labels1)
    y_pred_rf = rf.predict(X_test)
    print(y_pred_rf)
    acc = accuracy_score(y_test, y_pred_rf)
    acc_rf = round(acc * 100, 2)
    print("R", acc_rf)

    #
    svm = LinearSVC()
    # svm.fit(X_train,y_train)
    svm.fit(attributes1, labels1)
    y_pred_svm = svm.predict(X_test)
    acc = accuracy_score(y_test, y_pred_svm)
    acc_sv = round(acc * 100, 2)
    print("S", acc_sv)

    #
    nb = GaussianNB()
    # nb.fit(X_train, y_train)
    nb.fit(attributes1, labels1)
    y_pred_nb = nb.predict(X_test)
    acc = accuracy_score(y_test, y_pred_nb)
    acc_nb = round(acc * 100, 2)
    print("N", acc_nb)


    #

    dummy = DummyClassifier()
    # svm.fit(X_train,y_train)
    dummy.fit(attributes1, labels1)
    y_pred_dummy = dummy.predict(X_test)
    acc = accuracy_score(y_test, y_pred_dummy)
    acc_dy = round(acc * 100, 2)
    print("d", acc_dy)

    #

    ridg = RidgeClassifier()
    # svm.fit(X_train,y_train)
    ridg.fit(attributes1, labels1)
    y_pred_ridg = ridg.predict(X_test)
    acc = accuracy_score(y_test, y_pred_ridg)
    acc_rg = round(acc * 100, 2)
    print("R", acc_rg)



    import os
    import numpy as np
    import matplotlib.pyplot as plt

    x = ["Random Forest", "SVM", "DummyClassifier", "RidgeClassifier"]
    y = [acc_rf, acc_sv ,acc_dy, acc_rg]
    # plt.bar(x, y)
    fig, ax=plt.subplots()
    bar1=ax.bar(x, y)
    ax.set_xticks(x)
    ax.bar_label(bar1)
    ax.legend()

    plt.show()
    # fig, ax = plt.subplots()
    # width = 0.75
    # ind = np.arange(len(y))
    #
    # ax.barh(ind, y, width, color="green")
    #
    # for i, v in enumerate(y):
    #     ax.text(v + 3, i + .25, str(v),
    #             color='blue', fontweight='bold')
    # plt.show()
    # plt.savefig()

    return "ok"


















# ---------------------------------------
# prediction section######

@app.route('/prediction')
def prediction():
    return render_template('user/prediction.html')

@app.route('/prediction1', methods=['post'])
def prediction1():
    os = request.form['textfield']
    alg = request.form['textfield2']
    pc = request.form['textfield3']
    se = request.form['textfield4']
    cn = request.form['textfield5']
    es = request.form['textfield6']
    ca = request.form['textfield7']
    maths = request.form['textfield8']
    cskill = request.form['textfield9']
    hw = request.form['textfield13']
    hk = request.form['textfield12']
    csk = request.form['textfield11']
    psp = request.form['textfield10']
    cts = request.form['RadioGroup14']
    sc = request.form['RadioGroup13']
    tt = request.form['RadioGroup12']
    ods = request.form['RadioGroup11']
    rws = request.form['RadioGroup10']
    mcs = request.form['RadioGroup9']
    ica = request.form['RadioGroup15']
    jh = request.form['RadioGroup8']
    tcs = request.form['RadioGroup7']
    sre = request.form['RadioGroup6']
    mt = request.form['RadioGroup5']
    sw = request.form['RadioGroup4']
    hs = request.form['RadioGroup3']
    wte = request.form['RadioGroup2']
    intro = request.form['RadioGroup1']

    import numpy as np

    ar = []

    ar.append(int(os))
    ar.append(int(alg))
    ar.append(int(pc))
    ar.append(int(se))
    ar.append(int(cn))
    ar.append(int(es))
    ar.append(int(ca))
    ar.append(int(maths))
    ar.append(int(cskill))
    ar.append(int(hw))
    ar.append(int(hk))
    ar.append(int(csk))
    ar.append(int(psp))
    ar.append(int(cts))
    ar.append(int(sc))
    ar.append(int(tt))
    ar.append(int(ods))
    ar.append(int(rws))
    ar.append(int(mcs))
    ar.append(int(ica))
    ar.append(int(jh))
    ar.append(int(tcs))
    ar.append(int(sre))
    ar.append(int(mt))
    ar.append(int(sw))
    ar.append(int(hs))
    ar.append(int(wte))
    ar.append(int(intro))

    aatest = np.array([ar])
    import pandas as pd
    a = pd.read_csv(static_path + "dataset\\career_choices.csv")
    attributes = a.values[:, 0:28]
    labels = a.values[:, 28]

    rf = RandomForestClassifier()
    rf.fit(attributes, labels)
    res = rf.predict(aatest)
    print(res)
    job_roles=['Database Developer', 'Portal Administrator', 'System security Administrator', 'Business System Analyst', 'Software System Engineer',
               'Business intelligence analyst', 'CRM technical developer', 'Mobile Applcation developer', 'UX Designer', 'Quality Assurance associate',
               'Web developer', 'Information Security Analyst', 'Technical support', 'CRM business analyst', 'Project Manager', 'Information technology manager',
               'Programmer analyst', 'Design and UX', 'Sollutions Architect', 'System analyst', 'Network Security administrator', 'Data Architect',
               'Software Developer', 'E-commerce analystTechnical Service', 'Technical Service', 'Information Technology auditor', 'Network security Engineer',
               'Database Manager', 'Application Developer', 'Network engineer', 'Technical Engineer', 'Software quality assurance(QA)/Testing',
               'Database Administrator']
    idx=res[0]
    data=job_roles[idx]
    print(idx, data)
    return render_template('user/prediction.html', data=data)
    # return render_template('user/prediction.html', data=res[0])


# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    session['lin']=""
    return redirect('/')




if __name__ == '__main__':
    app.run()
