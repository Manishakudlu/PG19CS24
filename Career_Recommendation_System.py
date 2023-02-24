from flask import Flask,render_template,request,redirect,session
import datetime
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


# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    session['lin']=""
    return redirect('/')




if __name__ == '__main__':
    app.run()
