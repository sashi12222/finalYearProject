from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pymysql
from django.core.files.storage import FileSystemStorage
from datetime import date
import numpy as np
import random
import smtplib

global uname, filename, otp

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def HospitalLogin(request):
    if request.method == 'GET':
       return render(request, 'HospitalLogin.html', {})

def RevenueLogin(request):
    if request.method == 'GET':
       return render(request, 'RevenueLogin.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def AddActivities(request):
    if request.method == 'GET':
       return render(request, 'AddActivities.html', {})

def UploadCertificateAction(request):
    if request.method == 'POST':
        global uname
        person = request.POST.get('t1', False)
        ctype = request.POST.get('t2', False)
        image = request.FILES['t3']
        imagename = request.FILES['t3'].name
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update certificate set certificate_file='"+imagename+"' where username='"+person+"' and certificate_type='"+ctype+"' and certificate_file='Pending'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        fs = FileSystemStorage()
        if os.path.exists('ServicesApp/static/files/'+imagename):
            os.remove('ServicesApp/static/files/'+imagename)
        filename = fs.save('ServicesApp/static/files/'+imagename, image)
        status = "Certificate successfully updated to user account"
        context= {'data': status}
        return render(request, 'AdminScreen.html', context)    

def UploadCertificate(request):
    if request.method == 'GET':
        user = request.GET['user']
        ctype = request.GET['ctype']
        status = request.GET['status']
        output = '<tr><td><font size='' color="black"><b>Person&nbsp;Name</b></td><td><input name="t1" type="text" size="30" value="'+user+'" readonly></td></tr>'
        output += '<tr><td><font size='' color="black"><b>Certificate&nbsp;Type</b></td><td><input name="t2" type="text" size="30" value="'+ctype+'" readonly></td></tr>'
        context= {'data1':output}
        return render(request, 'UploadCertificate.html', context)

def ViewApproval(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Certificate Type</th><th><font size="" color="black">Applied Date</th>'
        output+='<th><font size="" color="black">Status</th><th><font size="" color="black">Certificate Filename</th>'
        output+='<th><font size="" color="black">Upload Certificate</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from certificate where status='Approved' and certificate_file='Pending'")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><font size="" color="black">'+row[5]+'</td>'
                output+='<td><a href=\'UploadCertificate?user='+row[0]+'&ctype='+row[2]+'&status=Approved\'><font size=3 color=black>Click Here</font></a></td></tr>'
               
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)     

def AddActivitiesAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        applicable_date = request.POST.get('t3', False)
        contact_person = request.POST.get('t4', False)
        status = "Error in adding upcoming activity"
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO activities(event_name,event_description,applicable_date,contact_person) VALUES('"+name+"','"+desc+"','"+applicable_date+"','"+contact_person+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Upcoming activity details added ro database"
        context= {'data': status}
        return render(request, 'AddActivities.html', context)
    

def RevenueLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'revenue' and password == 'revenue':
            context= {'data':'welcome '+username}
            return render(request, 'RevenueScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'RevenueLogin.html', context)    

def HospitalLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'hospital' and password == 'hospital':
            context= {'data':'welcome '+username}
            return render(request, 'HospitalScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'HospitalLogin.html', context)    

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)

def getUserDetails(username):
    father = ""
    dob = ""
    gender = ""
    phone = ""
    address=""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select father_name,birth_date,gender,contact_no,address FROM signup where username='"+username+"'")
        rows = cur.fetchall()
        for row in rows:
            father = row[0]
            dob = row[1]
            gender = row[2]
            phone = row[3]
            address = row[4]
    return father, dob, gender, phone, address

def HospitalAccept(request):
    if request.method == 'GET':
        user = request.GET['user']
        ctype = request.GET['ctype']
        status = request.GET['status']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update certificate set status='"+status+"' where username='"+user+"' and certificate_type='"+ctype+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':"Selected "+user+" Certificate status updated to "+status}
        return render(request, 'HospitalScreen.html', context) 

def ViewCertificateRequest(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Certificate Type</th><th><font size="" color="black">Applied Date</th>'
        output+='<th><font size="" color="black">Father Name</th><th><font size="" color="black">Birth Date</th>'
        output+='<th><font size="" color="black">Gender</th><th><font size="" color="black">Contact No</th>'
        output+='<th><font size="" color="black">Address</th><th><font size="" color="black">Genuine Details</th>'
        output+='<th><font size="" color="black">Fake Details</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from certificate where status='Pending'")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                if row[2] == 'Birth Certificate' or row[2] == 'Death Certificate':
                    father, dob, gender, phone, address = getUserDetails(row[0])
                    output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                    output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                    output+='<td><font size="" color="black">'+father+'</td>'
                    output+='<td><font size="" color="black">'+dob+'</td><td><font size="" color="black">'+gender+'</td>'
                    output+='<td><font size="" color="black">'+phone+'</td><td><font size="" color="black">'+address+'</td>'
                    output+='<td><a href=\'HospitalAccept?user='+row[0]+'&ctype='+row[2]+'&status=Approved\'><font size=3 color=black>Genuine Click Here</font></a></td>'
                    output+='<td><a href=\'HospitalAccept?user='+row[0]+'&ctype='+row[2]+'&status=Rejected\'><font size=3 color=black>Fake Click Here</font></a></td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'HospitalScreen.html', context)        


def RevenueAccept(request):
    if request.method == 'GET':
        user = request.GET['user']
        ctype = request.GET['ctype']
        status = request.GET['status']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update certificate set status='"+status+"' where username='"+user+"' and certificate_type='"+ctype+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':"Selected "+user+" Certificate status updated to "+status}
        return render(request, 'RevenueScreen.html', context)  
        
        
def ViewRevenueCertificateRequest(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Certificate Type</th><th><font size="" color="black">Applied Date</th>'
        output+='<th><font size="" color="black">Father Name</th><th><font size="" color="black">Birth Date</th>'
        output+='<th><font size="" color="black">Gender</th><th><font size="" color="black">Contact No</th>'
        output+='<th><font size="" color="black">Address</th><th><font size="" color="black">Genuine Details</th>'
        output+='<th><font size="" color="black">Fake Details</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from certificate where status='Pending'")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                if row[2] == 'Income Certificate' or row[2] == 'Community Certificate':
                    father, dob, gender, phone, address = getUserDetails(row[0])
                    output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                    output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                    output+='<td><font size="" color="black">'+father+'</td>'
                    output+='<td><font size="" color="black">'+dob+'</td><td><font size="" color="black">'+gender+'</td>'
                    output+='<td><font size="" color="black">'+phone+'</td><td><font size="" color="black">'+address+'</td>'
                    output+='<td><a href=\'RevenueAccept?user='+row[0]+'&ctype='+row[2]+'&status=Approved\'><font size=3 color=black>Genuine Click Here</font></a></td>'
                    output+='<td><a href=\'RevenueAccept?user='+row[0]+'&ctype='+row[2]+'&status=Rejected\'><font size=3 color=black>Fake Click Here</font></a></td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'RevenueScreen.html', context)        

def SignupAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        father = request.POST.get('t2', False)
        dob = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        contact = request.POST.get('t5', False)
        email = request.POST.get('t6', False)
        qualification = request.POST.get('t7', False)
        address = request.POST.get('t8', False)
        username = request.POST.get('t9', False)
        password = request.POST.get('t10', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(person_name,father_name,birth_date,gender,contact_no,email,qualification,address,username,password) VALUES('"+name+"','"+father+"','"+dob+"','"+gender+"','"+contact+"','"+email+"','"+qualification+"','"+address+"','"+username+"','"+password+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup process completed. You can login with "+username
        context= {'data': status}
        return render(request, 'Signup.html', context)

def ApplyCertificate(request):
    if request.method == 'GET':
       return render(request, 'ApplyCertificate.html', {})

def ApplyCertificateAction(request):
    if request.method == 'POST':
        global uname
        ctype = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        today = str(date.today())
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM certificate where username='"+uname+"' and certificate_type='"+ctype+"'")
            rows = cur.fetchall()
            if len(rows) > 0:
                status = "You already applied  or certificate under process"                
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO certificate(username,description,certificate_type,applied_date,status,certificate_file) VALUES('"+uname+"','"+desc+"','"+ctype+"','"+today+"','Pending','Pending')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Your application successfully submitted"
        context= {'data': status}
        return render(request, 'ApplyCertificate.html', context)

def ViewUpcomingActivity(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Activity Name</th><th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Applicable Date</th><th><font size="" color="black">Contact Person</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from activities")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'UserScreen.html', context)


def getEmail(uname):
    email = ""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select email from signup where username='"+uname+"'")
        rows = cur.fetchall()
        for row in rows:
            email = row[0]
            break
    return email        

def sendMail(email, otp_value):
    em = []
    em.append(email)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        email_address = 'kaleem202120@gmail.com'
        email_password = 'xyljzncebdxcubjq'
        connection.login(email_address, email_password)
        connection.sendmail(from_addr="kaleem202120@gmail.com", to_addrs=em, msg="Subject : Your OTP : "+otp_value+" to download certificate")
        
def DownloadCertificate(request):
    if request.method == 'GET':
        global uname, filename, otp
        filename = request.GET['file']
        otp = str(random.randint(1001, 9999))
        email = getEmail(uname)
        sendMail(email, otp)
        context= {'data':'OTP send to your mail'}
        return render(request, 'OTPScreen.html', context)

def OTPAction(request):
    if request.method == 'POST':
        global uname, filename, otp
        otp_value = request.POST.get('t1', False)
        if otp == otp_value:
            with open("ServicesApp/static/files/"+filename, "rb") as myfile:
                data = myfile.read()
            myfile.close()
            response = HttpResponse(data,content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename='+filename
            return response
        else:
            context= {'data':'Invalid OTP! Please retry'}
            return render(request, 'OTPScreen.html', context)
                         

def ViewStatus(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Person Name</th><th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Certificate Type</th><th><font size="" color="black">Applied Date</th>'
        output+='<th><font size="" color="black">Status</th><th><font size="" color="black">Download</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'government',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from certificate where username='"+uname+"'")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                if row[4] == 'Approved':
                    output+='<td><a href=\'DownloadCertificate?file='+row[5]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
                else:
                    output+='<td><font size="" color="black">--</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
    
