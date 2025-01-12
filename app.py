import base64
import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask,render_template,request,session,send_file,jsonify
from database import connection

app = Flask(__name__)
app.secret_key="xx"

static_path="D:\\project_final\\complete_my_project\\static\\"


@app.route('/')
def hello_world():
    return render_template('public/login.html')

@app.route("/login",methods=['POST'])
def log():
    uname=request.form['textfield']
    password=request.form['textfield2']
    qry="SELECT * FROM login WHERE username='"+uname+"' AND PASSWORD='"+password+"'"
    db=connection()
    data=db.selectOne(qry)
    if data[3]=="admin" :
        session['lg'] = "yes"
        return render_template('admin/admin_home.html')
    elif data[3]=="internal":
        qry = "SELECT * FROM `internal_guide` WHERE `loginid`='" + str(data[0]) + "'"
        print(qry)
        db = connection()
        data1 = db.selectOne(qry)
        if data1 is not None:
            session['lg']="yes"
            session['lg_img']=data1[7]
            session["internallid"]=data[0]
            return render_template('internal_guide/int_guide_home.html')
        else:
            return "<script>alert('User does not exist');window.location='/'</script>"
    elif data[3]=="external_org":
        qry = "SELECT * FROM `ext_org` WHERE `loginid`='" + str(data[0]) + "'"
        print(qry)
        db = connection()
        data1 = db.selectOne(qry)
        if data1 is not None:
            session['lg'] = "yes"
            session["externallid"]=data[0]
            return render_template('external_organisation/external_org_home.html')
        else:
            return "<script>alert('User does not exist');window.location='/'</script>"
    else:
        return "<script>alert('Unauthorised user');window.location='/'</script>"


@app.route("/forgot")
def forgot():
    return render_template("public/forgot_password.html")

@app.route("/forgot_post", methods=['post'])
def forgot_post():
    email=request.form['textfield']
    db=Db()
    qry="SELECT * FROM login WHERE username='"+email+"'"
    res=db.selectOne(qry)
    if res is None:
        return "<script>alert('Email not registered');window.location='/'</script>"
    else:
        psw=res['password']
        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("projectscheduler10@gmail.com", "Project@123")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from Project Scheduler"
        msg['From'] = "projectscheduler10@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Project Scheduler"
        body = "Password  :  " + psw
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return "<script>alert('Password sent to your mail..');window.location='/'</script>"


@app.route("/logout")
def logout():
    session['lg']="no"
    return render_template("public/login.html")
@app.route("/adhome",methods=['POST'])
def adhome():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('admin/admin_home.html')

@app.route('/admin_attandance_view')
def admin_attandance_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT DISTINCT batch FROM `group_table`"
    db = connection()
    data = db.select(qry)
    return render_template('admin/attandance_view.html',d=data)

@app.route("/ajax_grp_by_batch", methods=['post'])
def ajax_grp_by_batch():
    batch=request.form['batch']
    print(batch)
    db=Db()
    res=db.select("select * from group_table where batch='"+batch+"'")
    print(res)
    return jsonify(res)

@app.route("/ajax_att_by_grp", methods=['post'])
def ajax_att_by_grp():
    grpid=request.form['grpid']
    db=Db()
    res=db.select("select attandance.*,ext_org.orgname,ext_org.orgplace from ext_org inner join attandance on attandance.exassignid=ext_org.loginid where attandance.grouplid='"+grpid+"'")
    return jsonify(res)

@app.route("/admin_attandance_post",methods=['post'])
def admin_attandance_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    batch=request.form['batch']
    grpid=request.form['grp']
    qry="SELECT `group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`language`,`group_table`.`batch`,`attandance`.`file`,`attandance`.`date`,`ext_org`.`orgname` FROM `group_table` INNER JOIN attandance ON `group_table`.`loginid`=`attandance`.`grouplid` INNER JOIN ext_org ON attandance.`attandenceid`=ext_org.`eoid` WHERE attandance.`grouplid`='"+grpid+"' AND `group_table`.`batch`='"+str(batch)+"'"
    db=connection()
    qry2 = "SELECT `loginid`,`projectname` FROM `group_table`"
    value=db.select(qry)
    data = db.select(qry2)
    return render_template('admin/attandance_view.html',v=value,d=data)

@app.route('/admin_external_org_edit/<externalllid>')
def admin_external_org_edit(externalllid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT * FROM ext_org WHERE `loginid`='" + externalllid + "'"
    db = connection()
    data=db.selectOne(qry)
    return render_template('admin/external_org_edit.html',name=data[1],place=data[2],pin=data[3],phone=data[4],web=data[5],lat=data[6],long=data[7],loginid=data[9])

@app.route("/admin_ext_org_update_post",methods=['POST'])
def admin_ext_org_update():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    id = request.form['lid']
    name=request.form['textfield']
    place=request.form['textfield2']
    pin=request.form['textfield3']
    phone=request.form['textfield9']
    web=request.form['textfield4']
    latt=request.form['textfield5']
    longi=request.form['textfield6']
    db=connection()
    qry="UPDATE ext_org SET `orgname`='"+name+"',`orgplace`='"+place+"',`orgpin`='"+pin+"',`orgphone`='"+phone+"',`orgwebsite`='"+web+"',`orglat`='"+latt+"',`orglongi`='"+longi+"' WHERE `loginid`='"+id+"'"
    db.update(qry)
    return admin_external_org_view()

@app.route('/admin_external_org_registration')
def admin_external_org_registration():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('admin/external_org_registration.html')

@app.route("/admin_external_org_reg_post",methods=['post'])
def admin_external_org_reg_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    name=request.form['textfield']
    place=request.form['textfield2']
    phone=request.form['textfield9']
    pin=request.form['textfield3']
    web=request.form['textfield4']
    Latt=request.form['textfield5']
    longi=request.form['textfield6']
    email=request.form['textfield7']
    # password=request.form['textfield8']
    password=str(random.randint(10000000,99999999))
    db=connection()
    in1 = "INSERT INTO login (`username`,`password`,`type`)VALUES('" + email + "','" + password + "','external_org')"
    loginid=db.insert(in1)
    qry="INSERT INTO ext_org(`orgname`,`orgplace`,`orgpin`,`orgphone`,`orgwebsite`,`orglat`,`orglongi`,`email`,`loginid`)VALUES('"+name+"','"+place+"','"+pin+"','"+phone+"','"+web+"','"+Latt+"','"+longi+"','"+email+"','"+str(loginid)+"')"
    db.insert(qry)

    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("projectscheduler10@gmail.com", "Project@123")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from Project Scheduler"
    msg['From'] = "projectscheduler10@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Your Password for Project Scheduler"
    body = "Username  :  " + str(email) + "\nPassword  :  " + password
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return admin_external_org_registration()

@app.route('/admin_ext_org_delete/<extlid>')
def admin_ext_org_delete(extlid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete = "DELETE FROM ext_org WHERE `loginid`='" + extlid + "'"
    db=connection()
    db.delete(delete)
    return admin_external_org_view()

@app.route('/admin_external_org_view')
def admin_external_org_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM ext_org"
    db=connection()
    data=db.select(qry)
    return render_template('admin/external_org_view.html',d=data)

@app.route('/admin_group_add')
def admin_group_add():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('admin/group_add.html')

@app.route("/admin_group_add_post",methods=['POST'])
def admin_group_add_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    name=request.form['textfield']
    count=request.form['textfield2']
    email=request.form['textfield7']
    # password=request.form['textfield8']
    language=request.form['textfield3']
    batch=request.form['textfield4']
    status=request.form['textfield5']
    date=request.form['textfield6']
    password = str(random.randint(10000000, 99999999))
    db = connection()
    in1 = "INSERT INTO login (`username`,`password`,`type`)VALUES('" + email + "','" + password + "','group')"
    loginid = db.insert(in1)
    qry="INSERT INTO group_table(`projectname`,`membercount`,`email`,`language`,`batch`,`status`,`date`,`loginid`)VALUES('"+name+"','"+count+"','"+email+"','"+language+"','"+batch+"','"+status+"','"+date+"','"+str(loginid)+"')"
    db.insert(qry)
    return admin_group_add()

@app.route('/admin_group_edit/<grplid>')
def admin_group_edit(grplid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM group_table WHERE `loginid`='"+grplid+"'"
    db=connection()
    data=db.selectOne(qry)
    return render_template('admin/group_edit.html',name=data[1],count=data[2],email=data[3],laguage=data[4],batch=data[5],status=data[6],date=data[7],loginid=data[8])

@app.route("/admin_group_update_post",methods=['POST'])
def admin_group_update_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    id=request.form['lid']
    name=request.form['textfield']
    count=request.form['textfield2']
    language=request.form['textfield3']
    batch=request.form['textfield4']
    status=request.form['textfield5']
    date=request.form['textfield6']
    db=connection()
    qry="UPDATE group_table SET `projectname`='"+name+"',`membercount`='"+count+"',`language`='"+language+"',`batch`='"+batch+"',`status`='"+status+"',`date`='"+date+"' WHERE `loginid`='"+id+"'"
    db.update(qry)
    return admin_group_view()
@app.route('/admin_group_view')
def admin_group_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT * FROM group_table"
    db = connection()
    data = db.select(qry)
    return render_template('admin/group_view.html',g=data)

@app.route('/admin_group_delete/<grouplid>')
def admin_group_delete(grouplid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM group_table WHERE `loginid`='"+grouplid+"'"
    db=connection()
    db.delete(delete)
    return admin_group_view()

@app.route('/add_member_page_load/<grouplid>')
def add_member_page_load(grouplid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    session["grouplid"]=grouplid
    qry="SELECT `name`,`loginid` FROM student WHERE loginid NOT IN (SELECT studentid FROM group_members)"
    db=connection()
    data=db.select(qry)
    qry2 = "SELECT group_members.grpmemid,student.`name`,`student`.`email`,`student`.`pic` FROM `group_members` INNER JOIN `student` ON `group_members`.`studentid`=`student`.`loginid` WHERE `group_members`.`groupid`='" + grouplid + "'"
    db = connection()
    value=db.select(qry2)
    return render_template('admin/add_member.html',d=data,name=value)

@app.route("/member_add",methods=['POST'])
def member_add():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    studentlid=request.form['select2']
    grpid=session["grouplid"]
    qry="INSERT INTO group_members(`groupid`,`studentid`)VALUES('"+grpid+"','"+studentlid+"')"
    db=connection()
    db.insert(qry)
    return add_member_page_load(grpid)

@app.route('/admin_group_member_delete/<grpmemid>')
def admin_group_member_delete(grpmemid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM group_members WHERE `grpmemid`='"+grpmemid+"'"
    db=connection()
    db.delete(delete)
    grplid=session["grouplid"]
    return add_member_page_load(grplid)

@app.route('/admin_internal_assign')
def admin_internal_assign():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT `name`,`loginid` FROM `internal_guide`"
    qry2="SELECT `projectname`,`loginid` FROM `group_table` where loginid not in(select groupid from internal_assign)"
    db=connection()
    x=db.select(qry)
    y=db.select(qry2)
    return render_template('admin/internal_assign.html',a=x,b=y)

@app.route("/admin_internal_assign_post",methods=['post'])
def admin_internal_assign_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    guideid=request.form['select']
    grpid=request.form['select2']
    qry="INSERT INTO `internal_assign`(`igid`,`groupid`)VALUES('"+guideid+"','"+grpid+"')"
    db=connection()
    db.insert(qry)
    return admin_internal_assign()

@app.route('/admin_internal_assign_view')
def admin_internal_assign_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT `internal_guide`.`loginid`,`internal_guide`.`name`,`internal_assign`.`inassignid`,`group_table`.`loginid`,`group_table`.`projectname` FROM `internal_guide` INNER JOIN `internal_assign` ON`internal_guide`.`loginid`=`internal_assign`.`igid` INNER JOIN `group_table` ON `internal_assign`.`groupid`=`group_table`.`loginid`"
    db=connection()
    data=db.select(qry)
    return render_template('admin/internal_assign_view.html',d=data)

@app.route('/admin_intassing_delete/<intassingid>')
def admin_intassing_delete(intassingid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="DELETE FROM `internal_assign` WHERE `inassignid`='"+intassingid+"'"
    db=connection()
    db.delete(qry)
    return admin_internal_assign_view()

@app.route('/admin_internal_assign_edit/<intassingid>')
def admin_internal_assign_edit(intassingid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    session["intassid"]=intassingid
    qry="SELECT * FROM `internal_assign` WHERE `inassignid`='"+intassingid+"'"
    db=connection()
    data=db.selectOne(qry)
    qry = "SELECT `name`,`loginid` FROM `internal_guide`"
    qry2 = "SELECT `projectname`,`loginid` FROM `group_table`"
    x = db.select(qry)
    y = db.select(qry2)
    return render_template('admin/internal_assign_edit.html',d=data,a=x,b=y)

@app.route("/admin_internal_assing_edit_post",methods=['post'])
def admin_internal_assing_edit_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    assingid=session["intassid"]
    igid=request.form['select']
    grpid=request.form['select2']
    qry="UPDATE `internal_assign` SET `igid`='"+igid+"',`groupid`='"+grpid+"' WHERE `inassignid`='"+assingid+"'"
    db=connection()
    db.update(qry)
    return admin_internal_assign_view()

@app.route('/admin_internal_guide_registration')
def admin_internal_guide_registration():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('admin/internal_guide_registration.html')

@app.route("/admin_internal_guide_registration_post", methods=['POST'])
def admin_internal_guide_registration_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    name=request.form['textfield']
    email=request.form['textfield2']
    phone=request.form['textfield3']
    gender=request.form['radio']
    place=request.form['textfield4']
    pin=request.form['textfield7']
    pic=request.files['image']
    pic.save(static_path + "internal_guide\\"+pic.filename)
    path="/static/internal_guide/"+pic.filename
    # password=request.form['textfield6']
    password = str(random.randint(10000000, 99999999))
    db=connection()
    in1="INSERT INTO login (`username`,`password`,`type`)VALUES('"+email+"','"+password+"','internal')"
    loginid=db.insert(in1)
    qry12="INSERT INTO internal_guide(`name`,`email`,`phone`,`gender`,`place`,`pin`,`image`,`loginid`)VALUES('"+name+"','"+email+"','"+phone+"','"+gender+"','"+place+"','"+pin+"','"+path+"','"+str(loginid)+"')"
    db.insert(qry12)

    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("projectscheduler10@gmail.com", "Project@123")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from Project Scheduler"
    msg['From'] = "projectscheduler10@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Your Password for Project Scheduler"
    body = "Username  :  " + str(email)+"\nPassword  :  "+password
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)

    return admin_internal_guide_registration()


@app.route('/admin_internal_guide_view')
def admin_internal_guide_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM internal_guide"
    db=connection()
    data=db.select(qry)
    return render_template('admin/internal_guide_view.html',da=data)

@app.route('/admin_delete_internal_guide/<internallid>')
def admin_delete_internal_guide(internallid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM internal_guide WHERE `loginid`='"+internallid+"'"
    db=connection()
    db.delete(delete)
    return admin_internal_guide_view()

@app.route('/admin_internal_guide_edit/<internallid>')
def admin_internal_guide_edit(internallid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM internal_guide WHERE `loginid`='"+internallid+"'"
    db=connection()
    data=db.selectOne(qry)
    return render_template('admin/internal_guide_edit.html',name=data[1],email=data[2],phone=data[3],gender=data[4],place=data[5],pin=data[6],loginid=data[8])

@app.route("/admin_internal_guide_update_post",methods=['POST'])
def admin_internal_guide_update():
    id=request.form['lid']
    name=request.form['textfield']
    phone=request.form['textfield3']
    gender=request.form['radio']
    place=request.form['textfield4']
    pin=request.form['textfield5']
    db=connection()
    if 'image' in request.files :
        pic=request.files['image']
        if pic.filename != '' :
            pic.save(static_path + "internal_guide\\" + pic.filename)
            path = "/static/internal_guide/" + pic.filename
            qry="UPDATE internal_guide SET `name`='"+name+"',`phone`='"+phone+"',`gender`='"+gender+"',`place`='"+place+"',`pin`='"+pin+"',`image`='"+path+"' WHERE `loginid`='"+id+"' "
            db.update(qry)
        else:
            qry = "UPDATE internal_guide SET `name`='" + name + "',`phone`='" + phone + "',`gender`='" + gender + "',`place`='" + place + "',`pin`='" + pin + "' WHERE `loginid`='" + id + "' "
            db.update(qry)
    else:
        qry = "UPDATE internal_guide SET `name`='" + name + "',`phone`='" + phone + "',`gender`='" + gender + "',`place`='" + place + "',`pin`='" + pin + "' WHERE `loginid`='" + id + "' "
        db.update(qry)
    return admin_internal_guide_view()

@app.route('/admin_project_schedule_edit/<proscheduleid>')
def admin_project_schedule_edit(proscheduleid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM project_schedule WHERE `pschid`='"+proscheduleid+"'"
    db=connection()
    data=db.select(qry)
    return render_template('admin/project_schedule_edit.html',file=data[1],batch=data[2])

@app.route('/admin_project_schedule_delete/<proscheduleid>')
def admin_project_schedule_delete(proscheduleid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM project_schedule WHERE `pschid`='"+proscheduleid+"'"
    db=connection()
    db.delete(delete)
    return admin_project_schedule_view()

@app.route('/admin_project_schedule_management')
def admin_project_schedule_management():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT distinct batch FROM group_table"
    db = connection()
    data = db.select(qry)
    return render_template('admin/project_schedule_management.html',d=data)

@app.route("/admin_project_schedule_management_post",methods=['post'])
def admin_project_schedule_management_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    batch=request.form['select']
    file=request.files['fileField']
    file.save(static_path + "schedule\\" + file.filename)
    path = "/static/schedule/" + file.filename
    db=connection()
    qry="INSERT INTO project_schedule(`file`,`batch`)VALUES('"+path+"','"+batch+"')"
    db.insert(qry)
    return admin_project_schedule_management()

@app.route('/admin_project_schedule_view')
def admin_project_schedule_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM project_schedule"
    db=connection()
    data=db.select(qry)
    return render_template('admin/project_schedule_view.html',d=data)




@app.route('/admin_student_edit/<studentlid>')
def admin_student_edit(studentlid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM student WHERE `loginid`='"+studentlid+"'"
    db=connection()
    data=db.selectOne(qry)
    return render_template('admin/student_edit.html',name=data[1],place=data[2],pin=data[3],phone=data[4],gender=data[5],batch=data[8],loginid=data[9])

@app.route("/admin_student_update_post",methods=['POST'])
def admin_student_update_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    id=request.form['lid']
    name=request.form['textfield']
    place=request.form['textfield2']
    pin=request.form['textfield3']
    phone=request.form['textfield4']
    gender=request.form['radio']
    batch=request.form['textfield8']
    db=connection()
    if 'image' in request.files :
        pic=request.files['image']
        if pic.filename != '' :
            pic.save(static_path + "student\\" + pic.filename)
            path = "/static/student/" + pic.filename
            qry = " UPDATE student SET `name`='"+name+"',`place`='"+place+"',`pin`='"+pin+"',`phone`='"+phone+"',`gender`='"+gender+"',`pic`='"+path+"',`batch`='"+batch+"' WHERE `loginid`='"+id+"'"
            db.update(qry)
        else:
            qry = " UPDATE student SET `name`='" + name + "',`place`='" + place + "',`pin`='" + pin + "',`phone`='" + phone + "',`gender`='" + gender + "',`batch`='"+batch+"' WHERE `loginid`='"+id+"'"
            db.update(qry)
    else:
        qry = " UPDATE student SET `name`='" + name + "',`place`='" + place + "',`pin`='" + pin + "',`phone`='" + phone + "',`gender`='" + gender + "',`batch`='"+batch+"' WHERE `loginid`='"+id+"'"
        db.update(qry)
    return admin_student_view()


@app.route('/admin_student_registration')
def admin_student_registration():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('admin/student_registration.html')

@app.route("/admin_student_reg_post",methods=['POST'])
def admin_student_reg_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    name = request.form['textfield']
    place = request.form['textfield2']
    pin = request.form['textfield3']
    phone = request.form['textfield4']
    gender = request.form['radio']
    email = request.form['textfield6']
    pic = request.files['fileField']
    pic.save(static_path + "student\\" + pic.filename)
    path = "/static/student/" + pic.filename
    batch = request.form['textfield8']
    password = request.form['textfield10']
    db = connection()
    in1 = "INSERT INTO login (`username`,`password`,`type`)VALUES('" + email + "','" + password + "','student')"
    loginid = db.insert(in1)
    qry = "INSERT INTO student(`name`,`place`,`pin`,`phone`,`gender`,`email`,`pic`,`batch`,`loginid`)VALUES('"+name+"','"+place+"','"+pin+"','"+phone+"','"+gender+"','"+email+"','"+path+"','"+batch+"','"+str(loginid)+"')"
    db.insert(qry)

    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("projectscheduler10@gmail.com", "Project@123")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from Project Scheduler"
    msg['From'] = "projectscheduler10@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Your Password for Project Scheduler"
    body = "Username  :  " + str(email) + "\nPassword  :  " + password
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return admin_student_registration()

@app.route('/admin_student_view')
def admin_student_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM student"
    db=connection()
    data=db.select(qry)
    return render_template('admin/student_view.html',d=data)

@app.route('/admin_student_delete/<studentlid>')
def admin_student_delete(studentlid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM student WHERE `loginid`='"+studentlid+"'"
    db=connection()
    db.delete(delete)
    return admin_student_view()

@app.route('/admin_view_progress')
def admin_view_progress():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT DISTINCT `batch` FROM `group_table`"
    db=connection()
    data=db.select(qry)
    return render_template('admin/view_progress.html',d=data)

@app.route("/admin_view_progress_post",methods=['post'])
def admin_view_progress_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    batch=request.form['grp']
    qry="select progress.*, group_table.projectname,group_table.language from group_table, progress where progress.grouplid=group_table.loginid and batch='"+batch+"'"
    db=connection()
    data=db.select(qry)
    qry2 = "SELECT DISTINCT  `batch` FROM `group_table`"
    x=db.select(qry2)
    return render_template('admin/view_progress.html',c=data,d=x)


#*************************internal guide*************************#

@app.route("/inthome",methods=['POST'])
def inthome():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('internal_guide/int_guide_home.html')


@app.route('/int_guide_pro_view')
def int_guide_pro_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid=session["internallid"]
    qry="SELECT * FROM `internal_guide` WHERE `loginid`='"+str(lid)+"'"
    print(qry)
    db=connection()
    data=db.selectOne(qry)
    if data is not None:
        return render_template('internal_guide/igprofileview.html',name=data[1],mail=data[2],phone=data[3],gender=data[4],place=data[5],pin=data[6],pic=data[7])
    else:
        return "<script>alert('No Profile')</script>"


@app.route('/intguide_extorg_view')
def intguide_extorg_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM `ext_org`"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/ext_org_view.html',d=data)


@app.route("/int_chat_ext_org/<lid>")
def int_chat_ext_org(lid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    session["seluid"]=lid
    return render_template('internal_guide/ext_org_chat.html', toid=lid)


@app.route("/int_chat_ext_org_chk",methods=['post'])        # refresh messages chatlist
def int_chat_ext_org_chk():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    uid=request.form['idd']
    qry = "select date,message,formid from chat1 where (formid='" + str(
        session['internallid']) + "' and toid='" + uid + "') or ((formid='" + uid + "' and toid='" + str(
        session['internallid']) + "')) order by chatid desc"
    c = Db()
    res = c.select(qry)
    return jsonify(res)


@app.route("/int_chat_ext_org_post",methods=['POST'])
def int_chat_ext_org_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    id=str(session["seluid"])
    ta=request.form["ta"]
    qry="insert into chat1(message,date,formid,toid) values('"+ta+"',CURDATE(),'"+str(session['internallid'])+"','"+id+"')"
    d=Db()
    d.insert(qry)
    return render_template('internal_guide/ext_org_chat.html', toid=id)


# @app.route('/intguide_assigned_group_view')
# def intguide_assigned_group_view():
#     lid=session["internallid"]
#     qry="SELECT `group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid`, FROM `group_table` INNER JOIN `internal_assign` ON `group_table`.`loginid`=`internal_assign`.`groupid` WHERE `internal_assign`.`igid`='"+str(lid)+"'"
#     db=connection()
#     data=db.select(qry)
#     return render_template('d=data)

@app.route('/intguide_view_assgnd_grp')
def intguide_view_assgnd_grp():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid=session["internallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid`,`ext_org`.`orgname`,`ext_org`.`orgplace` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` INNER JOIN `external_assign` ON `external_assign`.`groupid`=`group_table`.`loginid` INNER JOIN `ext_org` ON `external_assign`.`eolid`=`ext_org`.`loginid`  WHERE `internal_assign`.`igid`='"+str(lid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/view_assigned_groups.html',d=data)

@app.route('/intguide_view_assgnd_grp_post',methods=['post'])
def intguide_view_assgnd_grp_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    name=request.form['textfield']
    lid=session["internallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid`,`ext_org`.`orgname`,`ext_org`.`orgplace` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` INNER JOIN `external_assign` ON `external_assign`.`groupid`=`group_table`.`loginid` INNER JOIN `ext_org` ON `external_assign`.`eolid`=`ext_org`.`loginid`  WHERE `internal_assign`.`igid`='"+str(lid)+"' and `group_table`.`projectname` like '%"+name+"%'"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/view_assigned_groups.html',d=data)

@app.route('/intguide_grp_assign_view/<grpid>')
def intguide_grp_assign_view(grpid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT `student`.`name`,`student`.`pic`,`student`.`loginid`,`student`.`email` FROM `student` INNER JOIN `group_members` ON `student`.`loginid`=`group_members`.`studentid` WHERE `group_members`.`groupid`='"+grpid+"'"
    print(qry)
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/view_assigned_group.html',d=data)

@app.route('/intguide_proj_schedule_view')
def intguide_proj_schedule_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid=session["internallid"]
    qry="SELECT * FROM `project_schedule`"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/project_schedule_view.html',d=data)

@app.route('/int_guide_extorg_grp_assign')
def int_guide_extorg_grp_assign():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT `loginid`,`orgname` FROM `ext_org`"
    qry2 = "SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`INNER JOIN `internal_assign` ON `group_table`.`loginid`=`internal_assign`.`groupid` WHERE `internal_assign`.`igid`='"+str(session["internallid"])+"' and `group_table`.`loginid` not in (select groupid from external_assign)"
    print(qry2)
    db=connection()
    x=db.select(qry)
    y=db.select(qry2)
    return render_template('internal_guide/group_assign.html',a=x,b=y)

@app.route('/int_guide_extorg_grp_assign_post', methods=['post'])
def int_guide_extorg_grp_assign_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    orglid=request.form['select']
    grpid=request.form['select2']
    qry="INSERT INTO external_assign (`groupid`,`eolid`)VALUES('" + grpid + "','" + orglid + "')"
    db=connection()
    db.insert(qry)
    return int_guide_extorg_grp_assign()

@app.route('/int_guide_attandance_view')
def int_guide_attandance_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db = connection()
    data = db.select(qry)
    return render_template('internal_guide/Attendance_view.html',d=data)

@app.route('/int_guide_attandance_view_post', methods=['post'])
def int_guide_attandance_view_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid=request.form['select']
    qry="SELECT `attandance`.`file`,`attandance`.`date`,`ext_org`.`orgname`,group_table.loginid FROM `attandance` INNER JOIN `group_table` ON `attandance`.`grouplid`=`group_table`.`loginid` INNER JOIN `ext_org` on attandance.exassignid=ext_org.loginid  WHERE `attandance`.`grouplid`='"+grpid+"'"
    qry2 = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db=connection()
    value=db.select(qry)
    data = db.select(qry2)
    return render_template('internal_guide/Attendance_view.html',s=value,d=data)

@app.route('/int_guide_project_schedule_view')
def int_guide_project_schedule_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM `project_schedule`"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/project_schedule_view.html',d=data)

@app.route('/int_guide_progress_view')
def int_guide_progress_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db = connection()
    data = db.select(qry)
    return render_template('internal_guide/progress_view.html', d=data)

@app.route('/int_guide_progress_view_post' ,methods=['post'])
def int_guide_progress_view_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid = request.form['select']
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname`,`progress`.`percentage`,`progress`.`file`,`progress`.`date` FROM `group_table` INNER JOIN `progress` ON `group_table`.`loginid`=`progress`.`grouplid` WHERE `group_table`.`loginid`='"+grpid+"'"
    qry2 = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db=connection()
    value=db.select(qry)
    data = db.select(qry2)
    return render_template('internal_guide/progress_view.html', v=value,d=data)

@app.route('/int_guide_view_file_frm_extorg')
def int_guide_view_file_frm_extorg():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db=connection()
    data=db.select(qry)
    return render_template('internal_guide/view_file_from_extorg.html',d=data)

@app.route('/int_guide_view_file_frm_extorg_post',methods=['post'])
def int_guide_view_file_frm_extorg_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid = request.form['select']
    qry="SELECT `group_table`.`groupid`,`group_table`.`projectname`,`file`.`fileid`,`file`.`grouplid`,`file`.`file`,`file`.`date` FROM `group_table` INNER JOIN `file` ON `group_table`.`loginid`=`file`.`grouplid` WHERE `group_table`.`loginid`='"+grpid+"'"
    qry2 = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    db=connection()
    value=db.select(qry)
    data = db.select(qry2)
    return render_template('internal_guide/view_file_from_extorg.html', v=value,d=data)

#*********************************external organisation*********************************#

@app.route("/exthome",methods=['POST'])
def exthome():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    return render_template('external_organisation/external_org_home.html')


@app.route('/ext_org_view_profile')
def ext_org_view_profile():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid=session["externallid"]
    qry="SELECT * FROM `ext_org` WHERE `loginid`='"+str(lid)+"'"
    db=connection()
    data=db.selectOne(qry)
    return render_template('external_organisation/ext_org_profileview.html',d=data)

@app.route('/ext_org_attendance_view')
def ext_org_attendance_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(lid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_org_attendance_view.html',d=data)

@app.route('/ext_org_attendance_view_post',methods=['post'])
def ext_org_attendance_view_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    grpid = request.form['select']
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(lid)+"'"
    qry2="SELECT `attandance`.`attandenceid`,`attandance`.`file`,`attandance`.`date` FROM `attandance` INNER JOIN `group_table` ON `attandance`.`grouplid`=`group_table`.`loginid` WHERE `attandance`.`grouplid`='"+str(grpid)+"'"
    db=connection()
    value=db.select(qry)
    data=db.select(qry2)
    return render_template('external_organisation/ext_org_attendance_view.html', d=value,v=data)

# @app.route("/download_att/<path>")
# def download_att(path):
#     try:
#         # path=attendence_path+path
#         return send_file(path, as_attachment=True)
#     except Exception as e:
#         return e

@app.route('/ext_org_attendance_add')
def ext_org_attendance_add():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(lid)+"'"
    # qry="SELECT `group_table`.`projectname`,`group_table`.`groupid` FROM `group_table`"
    db = connection()
    data = db.select(qry)
    return render_template('external_organisation/ext_attendance_add.html', d=data)

@app.route('/attendance_add',methods=['post'])
def attendance_add():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid = request.form['select']
    extlid=session["externallid"]
    file = request.files['file1']
    file.save(static_path + "attandance\\" + file.filename)
    path = "/static/attandance/" + file.filename
    qry="INSERT INTO `attandance`(`exassignid`,`file`,`date`,`grouplid`)VALUES('"+str(extlid)+"','"+path+"',curdate(),'"+str(grpid)+"')"
    db=connection()
    db.insert(qry)
    return "<script>window.location='/ext_org_attendance_add';alert('Added sucessfully')</script>"

@app.route('/attandance_delete/<attendanceid>')
def attandance_delete(attendanceid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    delete="DELETE FROM `attandance` WHERE `attandenceid`='"+attendanceid+"'"
    db=connection()
    db.delete(delete)
    return ext_org_attendance_view()

@app.route('/ext_org_add_file')
def ext_org_add_file():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='" + str(
        lid) + "'"
    db = connection()
    data = db.select(qry)
    return render_template('external_organisation/file_add.html', d=data)


@app.route('/ext_org_add_file_post', methods=['post'])
def ext_org_add_file_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid = request.form['select']
    # extlid = session["externallid"]
    file = request.files['files']
    file.save(static_path + "file\\" + file.filename)
    path = "/static/file/" + file.filename
    qry = "INSERT INTO `file`(`grouplid`,`file`,`date`)VALUES('" + str(
        grpid) + "','" + path + "',curdate())"
    db = connection()
    db.insert(qry)
    return "<script>window.location='/ext_org_add_file';alert('Added sucessfully')</script>"

@app.route('/ext_org_view_file')
def ext_org_view_file():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    # qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname`,`group_table`.`membercount`,`group_table`.`email`,`group_table`.`language`,`group_table`.`batch`,`group_table`.`status`,`group_table`.`date`,`internal_assign`.`igid`,`internal_assign`.`groupid` FROM `group_table` INNER JOIN `internal_assign` ON `internal_assign`.`groupid`=`group_table`.`loginid` WHERE `internal_assign`.`igid`='" + str(session["internallid"]) + "'"
    lid = session["externallid"]
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='" + str(
        lid) + "'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/file_view.html',d=data)

@app.route('/ext_org_view_file_post',methods=['post'])
def ext_org_view_file_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grpid = request.form['select']
    # qry="SELECT `group_table`.`groupid`,`group_table`.`projectname`,`file`.`fileid`,`file`.`grouplid`,`file`.`file`,`file`.`date` FROM `group_table` INNER JOIN `file` ON `group_table`.`loginid`=`file`.`grouplid` WHERE `group_table`.`loginid`='"+grpid+"'"
    lid = session["externallid"]
    qry = "SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='" + str(
        lid) + "'"
    qry2 = "SELECT file.*,group_table.projectname FROM FILE inner join group_table on group_table.loginid=file.grouplid WHERE grouplid='" + grpid + "'"
    db=connection()
    data=db.select(qry)
    value = db.select(qry2)
    print(qry2)
    return render_template('external_organisation/file_view.html', v=value,d=data)

@app.route("/ext_org_del_file/<fid>")
def ext_org_del_file(fid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    db=connection()
    db.delete("delete from file where fileid='"+fid+"'")
    return ext_org_view_file()

@app.route('/ext_org_grp_view')
def ext_org_grp_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    extlid=session["externallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`groupid`,`group_table`.`projectname`,group_table.`membercount`,group_table.`language` FROM `group_table` INNER JOIN `external_assign` ON `group_table`.`loginid`=`external_assign`.`groupid` WHERE `external_assign`.`eolid`='"+str(extlid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_org_grp_view.html',d=data)

@app.route('/ext_org_grp_view_post',methods=['post'])
def ext_org_grp_view_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    extlid=session["externallid"]
    prj=request.form['textfield']
    qry="SELECT `group_table`.`loginid`,`group_table`.`groupid`,`group_table`.`projectname`,group_table.`membercount`,group_table.`language` FROM `group_table` INNER JOIN `external_assign` ON `group_table`.`loginid`=`external_assign`.`groupid` WHERE `external_assign`.`eolid`='"+str(extlid)+"' and `group_table`.`projectname` like '%"+prj+"%'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_org_grp_view.html',d=data)


@app.route('/ext_org_grp_membr_view/<grpid>')
def ext_org_grp_membr_view(grpid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT `student`.`name`,`student`.`pic`,`student`.`batch` FROM `student` INNER JOIN `group_members` ON `group_members`.`studentid`=`student`.`loginid` WHERE `group_members`.`groupid`='"+str(grpid)+"'"
    db=connection()
    data=db.select(qry)
    print(qry)
    return render_template('external_organisation/ext_org_member_view.html',  d=data)

@app.route('/ext_org_progress_view')
def ext_org_progress_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    extlid=session["externallid"]    
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(extlid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_progress_view.html',d=data)

@app.route('/ext_org_progress_view_post',methods=['post'])
def ext_org_progress_view_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grplid = request.form['select']
    extlid=session["externallid"]
    qry="SELECT `progress`.`file`,`progress`.`percentage`,`progress`.`date`,`group_table`.`projectname`,`group_table`.`groupid`,progress.progressid FROM `progress` INNER JOIN `group_table` ON `progress`.`grouplid`=`group_table`.`loginid` WHERE `progress`.`grouplid`='"+str(grplid)+"'"
    qry2="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(extlid)+"'"
    db=connection()
    value=db.select(qry)
    data=db.select(qry2)
    return render_template('external_organisation/ext_progress_view.html',v=value,d=data)

@app.route("/ext_del_progress/<pid>")
def ext_del_progress(pid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="delete from progress where progressid='"+pid+"'"
    db=connection()
    db.delete(qry)
    return ext_org_progress_view()

@app.route('/ext_org_progress_add')
def ext_org_progress_add():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    extlid=session["externallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(extlid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_org_progress_add.html', d=data)

@app.route('/ext_org_progress_add_post',methods=['post'])
def ext_org_progress_add_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    grplid = request.form['select']
    file=request.files['file1']
    percentage=request.form['textfield']
    date=request.form['textfield2']
    file.save(static_path + "progress\\" + file.filename)
    path = "/static/progress/" + file.filename
    qry="INSERT INTO `progress`(`grouplid`,`file`,`percentage`,`date`)VALUES('"+grplid+"','"+path+"','"+percentage+"','"+date+"')"
    db=connection()
    db.insert(qry)
    return ext_org_progress_add()


@app.route('/ext_org_project_schedule_view')
def ext_org_project_schedule_view():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    qry="SELECT * FROM `project_schedule`"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/project_schedule_view.html',d=data)


@app.route('/ext_org_view_guides')
def ext_org_view_guides():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(lid)+"'"
    db=connection()
    data=db.select(qry)
    return render_template('external_organisation/ext_view_guides.html',d=data)

@app.route('/ext_org_view_guides_post', methods=['post'])
def ext_org_view_guides_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    lid = session["externallid"]
    grpid=request.form['select']
    qry="SELECT `group_table`.`loginid`,`group_table`.`projectname` FROM `group_table`,`external_assign` WHERE `external_assign`.`groupid`=`group_table`.`loginid` AND `external_assign`.`eolid`='"+str(lid)+"'"
    db=connection()
    data=db.select(qry)
    data2=db.selectOne("select internal_guide.* from internal_guide inner join internal_assign on internal_assign.igid=internal_guide.loginid where internal_assign.groupid='"+grpid+"'")
    return render_template('external_organisation/ext_view_guides.html',d=data, v=data2)

@app.route("/ext_chat_guide/<lid>")
def ext_chat_guide(lid):
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    session["seluid"]=lid
    return render_template('external_organisation/ext_chat_int.html', toid=lid)


@app.route("/ext_chat_guide_chk",methods=['post'])        # refresh messages chatlist
def ext_chat_guide_chk():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    uid=request.form['idd']
    qry = "select date,message,formid from chat1 where (formid='" + str(
        session['externallid']) + "' and toid='" + uid + "') or ((formid='" + uid + "' and toid='" + str(
        session['externallid']) + "')) order by chatid desc"
    c = Db()
    res = c.select(qry)
    return jsonify(res)


@app.route("/ext_chat_guide_post",methods=['POST'])
def ext_chat_guide_post():
    if session['lg']=="no":
        return "<script>alert('You are logged out.. Login to continue');window.location='/'</script>"
    id=str(session["seluid"])
    ta=request.form["ta"]
    qry="insert into chat1(message,date,formid,toid) values('"+ta+"',CURDATE(),'"+str(session['externallid'])+"','"+id+"')"
    d=Db()
    d.insert(qry)
    return render_template('external_organisation/ext_chat_int.html', toid=id)




#****************************************************Group******Android**********************************************#
from android_db_connect import Db
@app.route("/and_login",methods=['POST'])
def andlogin():
    uname = request.form['username']
    password = request.form['password']
    qry = "SELECT * FROM login WHERE username='" + uname + "' AND PASSWORD='" + password + "'"
    print(qry)
    db = connection()
    data = db.selectOne(qry)
    if data is not None:
        if data[3] == "group":
            q = "SELECT batch,projectname FROM group_table WHERE loginid='"+str(data[0])+"'"
            print(q)
            dat = db.selectOne(q)
            print(dat)
            return jsonify(status="ok",lid=data[0],batch=dat[0],projectname=dat[1])
        else:
            return jsonify(status="no")
    else:
        return jsonify(status="no")

@app.route("/and_profile",methods=['POST'])
def and_profile():
    lid = request.form['lid']
    # password = request.form['password']
    qry = "SELECT `projectname`,`membercount`,`email`,`language`,`batch`,`status`,`date` FROM group_table WHERE group_table.loginid='"+str(lid)+"'"
    db = connection()
    print(qry)
    data = db.selectOne(qry)
    print(data)
    if data is not None:

            return jsonify(status="ok",name=data[0],count=data[1],mail=data[2],lang=data[3],batch=data[4],state=data[5],date=data[6])

    else:
        return jsonify(status="no")

@app.route("/and_internal_guide",methods=['POST'])
def and_internal_guide():
    lid = request.form['lid']
    # password = request.form['password']
    qry = "SELECT `name`,`email`,`phone`,`gender`,`place`,`pin`,`image` FROM `internal_guide` inner join internal_assign on internal_assign.igid=internal_guide.loginid WHERE internal_assign.groupid='"+str(lid)+"'"
    db = connection()
    print(qry)
    data = db.selectOne(qry)
    print(data)
    if data is not None:
            return jsonify(status="ok",name=data[0],email=data[1],phone=data[2],gender=data[3],place=data[4],pin=data[5],image=data[6])
    else:
        return jsonify(status="no")

@app.route("/and_progress",methods=['POST'])
def and_progress():
    path = request.form['file']
    percentage = request.form['percentage']
    lid= request.form['lid']
    a = base64.b64decode(path)
    dt = datetime.datetime.now()
    dd = str(dt).replace(" ", "_").replace(":", "_").replace("-", "_")
    fh = open(static_path + "progress\\" + dd + ".jpg", "wb")
    path = "/static/progress/" + dd + ".jpg"
    fh.write(a)
    fh.close()
    qry = "INSERT INTO `progress`(`grouplid`,`file`,`percentage`,`date`)VALUES('" + lid + "','" + path + "','" + percentage + "',curdate())"
    db = connection()
    db.insert(qry)
    return jsonify(status="ok")

@app.route("/and_view_progress",methods=['POST'])
def and_view_progress():
    lid = request.form['lid']
    qry = "SELECT * FROM `progress` WHERE progress.grouplid='"+str(lid)+"'"
    db = Db()
    print(qry)
    data = db.select(qry)
    print(data)



    if data is not None:

            return jsonify(status="ok",data=data)

    else:
        return jsonify(status="no")


@app.route("/and_member",methods=['POST'])
def and_member():
    lid = request.form['lid']
    # password = request.form['password']

    qry = "SELECT `student`.*,`group_members`.* FROM `student`INNER JOIN `group_members` ON `group_members`.studentid=`student`.loginid WHERE `group_members`.groupid='"+lid+"'"
    db = Db()
    print(qry)
    data = db.select(qry)
    print(data)
    if data is not None:

            return jsonify(status="ok",data=data)
    else:
        return jsonify(status="no")

@app.route('/and_project_schedule',methods=['POST'])
def and_project_schedule():
    lid = request.form['lid']
    batch=request.form['batch']
    qry = "SELECT * FROM `project_schedule`WHERE batch='"+str(batch)+"'"
    print(qry)
    db = Db()
    data = db.select(qry)
    print(data)
    if data is not None:

        return jsonify(status="ok",data=data)

    else:
            return jsonify(status="no")

@app.route('/and_view_file',methods=['POST'])
def and_view_file():
    lid = request.form['lid']
    qry = "SELECT * FROM `file` WHERE grouplid='"+str(lid)+"'"
    db = Db()
    data = db.select(qry)
    print(data)
    if data is not None:
        return jsonify(status="ok",data=data)
    else:
        return jsonify(status="no")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# , host='0.0.0.0'