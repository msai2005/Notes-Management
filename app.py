from flask import Flask,request,redirect,url_for,render_template,flash,session#session package store
from flask_session import Session # fro secure
from otp import genotp
from cmail import sendmail
from stoken import endata,dndata
import mysql.connector
import flask_excel as excel
mydb=mysql.connector.connect(user='root',password='krishna',host='localhost',db='notes')
app=Flask(__name__)
excel.init_excel(app)
app.config['SESSION_TYPE']='filesystem'
Session(app) #integreat
app.secret_key   ='code0909'
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])

def register():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['email']
        userpassword=request.form['password']
        try:
            cursor=mydb.cursor()
            cursor.execute('select count(useremail) from userdata where useremail=%s',[useremail])
            count_email=cursor.fetchone()#(1,or 0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verified email')
            return redirect(url_for('register'))
        else:
            if count_email[0]==0:
                gotp=genotp()
                userdata={'username':username,'useremail':useremail,'userpassword':userpassword,'server_otp':gotp}
                subject=f'SNM APP Verification'
                body=f'Use the OTP for verify:{gotp}'
                sendmail(to=useremail,subject=subject,body=body)
                flash('otp is sent to your email')
                return redirect(url_for('otpverification',serverdata=endata(userdata)))
            elif count_email[0]==1:
                flash('Email already exist')
    return render_template('register.html')
@app.route('/otpverification/<serverdata>',methods=['GET','POST'])
def otpverification(serverdata):
    try:
        de_otp=dndata(serverdata)
    except Exception as e:
        print(e)
        flash('not verified otp')
        return redirect(url_for('register'))
    else:
        if request.method=='POST':
            user_otp=request.form['otp']
            if user_otp==de_otp['server_otp']:
                cursor=mydb.cursor() #it is mysql cursor created using mysqldb conncetion object
                cursor.execute('insert into userdata(username,useremail,userpassword)values(%s,%s,%s)',[de_otp['username'],de_otp['useremail'],de_otp['userpassword']])
                mydb.commit()
                cursor.close()
                flash('Details registered Successfully')
                return redirect(url_for("login"))
            else:
                flash('otp was wrong')
                return redirect(url_for('otpverification'),serverotp=serverdata)
    return render_template('otp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_useremail=request.form['email']
        login_password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(useremail) from userdata where useremail=%s',[login_useremail])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('could not verify user email')
            return redirect(url_for('login'))
        else:
            if count_email[0]==1:
                cursor.execute('select userpassword from userdata where useremail=%s',[login_useremail])
                stored_password=cursor.fetchone()
                if stored_password[0]==login_password:
                    session['user']=login_useremail
                    flash('user logged is successfully')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Password was wrong')
                    return redirect(url_for('login'))
            elif count_email[0]==0:
                flash('no Email found')
                return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        flash('plz login')
        return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    else:
        flash('pls login to logout')
        return redirect(url_for('login'))
@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if not session.get('user'):
        flash('pls login to add notes')
        return redirect(url_for('login'))
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone() #(1,) or (2,)
            if user_id[0]:
                cursor.execute('insert into notesdata(notes_title,notes_description,userid) values(%s,%s,%s)',[title,description,user_id[0]])
                mydb.commit()
                cursor.close()
            else:
                flash('could not fetch user details')
                return redirect(url_for('addnotes'))
        except Exception as e:
            print(e)
            flash('could not store notes details')
            return redirect(url_for('addnotes'))
        else:
            flash('Notes added successfully')
            return redirect(url_for('addnotes'))
    return render_template('addnotes.html')
@app.route('/viewallnotes')
def viewallnotes():
    if  not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,created_at from notesdata where userid=%s',[user_id])
        stored_allnotesdata=cursor.fetchall()
        print(stored_allnotesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewallnotes.html',
        stored_allnotesdata=stored_allnotesdata)
@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if  not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        stored_notesdata=cursor.fetchone()
        print(stored_notesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewnotes.html',
        stored_notesdata=stored_notesdata)
@app.route('/deletenote/<nid>')
def deletenote(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('delete from notesdata where userid=%s and notesid=%s',[user_id,nid])
        mydb.commit()
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not delete notes details')
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('viewallnotes'))
@app.route('/updatenotes/<nid>',methods=['POST','GET'])
def updatenotes(nid):
    if not session.get('user'):
        flash('pls login to access the dashboard feature')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,notes_description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        stored_notesdata=cursor.fetchone()
        print(stored_notesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch notes details')
        return redirect(url_for('viewallnotes'))
    else:
        if request.method=='POST':
            updated_title=request.form['title']
            updated_description=request.form['description']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone() #(1,) or (2,)
                if user_id[0]:
                    cursor.execute('update notesdata set notes_title=%s,notes_description=%s where userid=%s and notesid=%s',[updated_title,updated_description,user_id[0],nid])
                    mydb.commit()
                    cursor.close()
                else:
                    flash('could not fetch user details')
                    return redirect(url_for('updatenotes',nid=nid))
            except Exception as e:
                print(e)
                flash('could not store notes details')
                return redirect(url_for('updatenotes',nid=nid))
            else:
                flash('Notes updated successfully')
                return redirect(url_for('updatenotes',nid=nid))
        return render_template('updatenotes.html',stored_notesdata=stored_notesdata)
@app.route('/getexceldata')
def getexceldata():
    if  not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,notes_description,created_at from notesdata where userid=%s',[user_id])
        stored_allnotesdata=cursor.fetchall()
        print(stored_allnotesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        array_data=[list(i) for i in stored_allnotesdata]
        columns=['Notesid','Notestitle','Notesdescription','created_at']
        array_data.insert(0,columns)
        return excel.make_response_from_array(array_data,'xlsx',file_name='Allnotesdata')
app.run(debug=True,use_reloader=True)