from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
import pymysql
import os
import matplotlib.pyplot as plt #use to visualize dataset vallues
import io
import base64
from datetime import date

import torch
import cv2
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Empty password for XAMPP MySQL
    'database': 'laundry',
    'charset': 'utf8'
}

# Initialize model only when needed
_model = None
def get_model():
    global _model
    if _model is None:
        _model = torch.hub.load('yolov5', 'custom', path='model/best.pt', force_reload=True, source='local')
    return _model

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def WriteDescriptionAction(request):
    if request.method == 'POST':
        # Check if user is logged in and is an admin
        if not request.session.get('username') or not request.session.get('is_admin'):
            return redirect('/AdminLogin')
            
        lid = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()
        student_sql_query = "update laundry_service set delivery_status = '"+desc+"' where laundry_id='"+lid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':'Delivery Task Completed'}
        return render(request, 'AdminScreen.html', context)

def WriteDescription(request):
    if request.method == 'GET':
        # Check if user is logged in and is an admin
        if not request.session.get('username') or not request.session.get('is_admin'):
            return redirect('/AdminLogin')
            
        name = request.GET['name']
        output = '<tr><td><font size="" color="black">Laundry&nbsp;ID</b></td><td><input type="text" name="t1" size="15" value="'+name+'" readonly/></td></tr>'
        context= {'data1':output}
        return render(request, 'WriteDescription.html', context)  

def ViewOrderStatus(request):
    if request.method == 'GET':
        # Check if user is logged in and is an admin
        if not request.session.get('username') or not request.session.get('is_admin'):
            return redirect('/AdminLogin')
        
        output = '''
        <div class="card shadow mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="bi bi-list-check me-2"></i>All Customer Orders</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover table-striped">
                        <thead class="table-primary">
                            <tr>
                                <th>ID</th>
                                <th>Customer</th>
                                <th>Date</th>
                                <th>Service</th>
                                <th>Items</th>
                                <th>Stain Result</th>
                                <th>Delivery Date</th>
                                <th>Status</th>
                                <th>Image</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
        '''
        
        con = get_db_connection()
        with con:
            cur = con.cursor()
            cur.execute("select * from laundry_service")
            rows = cur.fetchall()
            
            for row in rows:
                # Calculate total items
                items_count = int(row[4]) + int(row[5]) + int(row[6]) + int(row[7]) + int(row[8]) + int(row[9]) + int(row[10]) + int(row[11]) + int(row[12]) + int(row[13])
                items_detail = []
                
                if int(row[4]) > 0: items_detail.append(f"{row[4]} Shirts")
                if int(row[5]) > 0: items_detail.append(f"{row[5]} T-Shirts")
                if int(row[6]) > 0: items_detail.append(f"{row[6]} Shorts")
                if int(row[7]) > 0: items_detail.append(f"{row[7]} Pants")
                if int(row[8]) > 0: items_detail.append(f"{row[8]} Towels")
                if int(row[9]) > 0: items_detail.append(f"{row[9]} Suits")
                if int(row[10]) > 0: items_detail.append(f"{row[10]} Inner Wear")
                if int(row[11]) > 0: items_detail.append(f"{row[11]} Kurtas")
                if int(row[12]) > 0: items_detail.append(f"{row[12]} Paijamas")
                if int(row[13]) > 0: items_detail.append(f"{row[13]} Skirts")
                
                items_html = f"<span class='badge bg-info text-dark'>{items_count} items</span><div class='small text-muted mt-1'>" + ", ".join(items_detail[:3])
                if len(items_detail) > 3:
                    items_html += f" <span class='text-primary'>+{len(items_detail)-3} more</span>"
                items_html += "</div>"
                
                # Format status with appropriate badge
                status = row[18]
                if status == "Pending":
                    status_badge = f"<span class='badge bg-warning text-dark'>{status}</span>"
                elif status == "Completed":
                    status_badge = f"<span class='badge bg-success'>{status}</span>"
                else:
                    status_badge = f"<span class='badge bg-primary'>{status}</span>"
                
                # Format date for better display
                laundry_date = row[2]
                
                # Format action button
                action_html = ""
                if status == "Pending":
                    action_html = f'''
                    <a href="WriteDescription?name={row[0]}" class="btn btn-sm btn-primary">
                        <i class="bi bi-pencil-fill me-1"></i> Update
                    </a>
                    '''
                else:
                    action_html = f'<span class="text-muted small">No action needed</span>'
                
                output += f'''
                <tr>
                    <td><span class="fw-bold">#{row[0]}</span></td>
                    <td>{row[1]}</td>
                    <td>{laundry_date}</td>
                    <td><span class="badge bg-primary">{row[3]}</span></td>
                    <td>{items_html}</td>
                    <td><span class="badge bg-{'success' if row[15]=='Found' else 'secondary'}">{row[15]}</span></td>
                    <td>{row[16]}</td>
                    <td>{status_badge}</td>
                    <td>
                        <a href="static/files/{row[14]}" data-lightbox="laundry-{row[0]}" data-title="Order #{row[0]} - Customer: {row[1]}">
                            <img src="static/files/{row[14]}" class="img-thumbnail-custom" alt="Laundry Image" />
                        </a>
                    </td>
                    <td>{action_html}</td>
                </tr>
                '''
        
        output += '''
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        '''
        
        context = {'data': output}
        return render(request, 'AdminScreen.html', context)        

def ViewCustomers(request):
    if request.method == 'GET':
        # Check if user is logged in and is an admin
        if not request.session.get('username') or not request.session.get('is_admin'):
            return redirect('/AdminLogin')
        
        output = '''
        <div class="card shadow mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="bi bi-people-fill me-2"></i>Registered Customers</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover table-striped">
                        <thead class="table-primary">
                            <tr>
                                <th>Username</th>
                                <th>Password</th>
                                <th>Contact Number</th>
                                <th>Email Address</th>
                                <th>Home Address</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
        '''
        
        con = get_db_connection()
        with con:
            cur = con.cursor()
            cur.execute("select * from register")
            rows = cur.fetchall()
            
            for row in rows:
                # Count user orders
                user_orders = 0
                with get_db_connection() as order_con:
                    order_cur = order_con.cursor()
                    order_cur.execute(f"SELECT COUNT(*) FROM laundry_service WHERE username='{row[0]}'")
                    user_orders = order_cur.fetchone()[0]
                
                status_badge = ""
                if user_orders > 0:
                    status_badge = f'<span class="badge bg-success">{user_orders} orders</span>'
                else:
                    status_badge = '<span class="badge bg-secondary">No orders</span>'
                
                output += f'''
                <tr>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center me-2" style="width: 35px; height: 35px;">
                                <i class="bi bi-person-fill"></i>
                            </div>
                            <div>
                                <span class="fw-bold">{row[0]}</span>
                                <div class="small text-muted">Customer</div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="text-muted">••••••••</span>
                        <button class="btn btn-sm btn-link p-0 ms-2" 
                                onclick="this.previousElementSibling.textContent = '{row[1]}'; 
                                         this.style.display = 'none';">
                            <i class="bi bi-eye-fill"></i>
                        </button>
                    </td>
                    <td><i class="bi bi-telephone-fill text-muted me-1"></i> {row[2]}</td>
                    <td><i class="bi bi-envelope-fill text-muted me-1"></i> {row[3]}</td>
                    <td><i class="bi bi-geo-alt-fill text-muted me-1"></i> {row[4]}</td>
                    <td>{status_badge}</td>
                </tr>
                '''
        
        output += '''
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        '''
        
        context = {'data': output}
        return render(request, 'AdminScreen.html', context)   

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            # Store admin username in session
            request.session['username'] = username
            request.session['is_admin'] = True
            context= {'data':'Welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)

def predict(filename):
    model = get_model()
    img = cv2.imread(filename)
    img = cv2.resize(img, (512, 512))
    results = model(img)
    results.xyxy[0]  # im predictions (tensor)
    out = results.pandas().xyxy[0]  # im predictions (pandas)
    print(out)
    result = "Not Found"
    if len(out) > 0:
        for i in range(len(out)):
            xmin = int(out['xmin'].ravel()[i])
            ymin = int(out['ymin'].ravel()[i])
            xmax = int(out['xmax'].ravel()[i])
            ymax = int(out['ymax'].ravel()[i])
            name = out['name'].ravel()[i]
            confidence = float(out['confidence'].ravel()[i])
            if confidence > 0.80:
                result = "Found"
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                cv2.putText(img, name, (xmin, ymin-20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    return img, result            

def UploadImageAction(request):
    if request.method == 'POST':
        # Get username from session
        username = request.session.get('username', '')
        if not username:
            return render(request, 'UserLogin.html', {'data': 'Please login first'})
            
        # Get service details from session
        service = request.session.get('service', '')
        shirt = request.session.get('shirt', '')
        tshirt = request.session.get('tshirt', '')
        shorts = request.session.get('shorts', '')
        pants = request.session.get('pants', '')
        towels = request.session.get('towels', '')
        suits = request.session.get('suits', '')
        inner = request.session.get('inner', '')
        kurta = request.session.get('kurta', '')
        paijama = request.session.get('paijama', '')
        skirt = request.session.get('skirt', '')
        address = request.session.get('address', '')
        delivery_date = request.session.get('delivery_date', '')
        
        today = str(date.today())
        image = request.FILES['t1']
        imagename = request.FILES['t1'].name
        fs = FileSystemStorage()
        if os.path.exists('LaundryApp/static/files/'+imagename):
            os.remove('LaundryApp/static/files/'+imagename)
        filename = fs.save('LaundryApp/static/files/'+imagename, image)
        img, result = predict('LaundryApp/static/files/'+imagename)
        os.remove('LaundryApp/static/files/'+imagename)
        cv2.imwrite('LaundryApp/static/files/'+imagename, img)
        con = get_db_connection()
        lid = 0
        with con:
            cur = con.cursor()
            cur.execute("select max(laundry_id) from laundry_service")
            rows = cur.fetchall()
            for row in rows:
                lid = row[0]
        if lid is not None:
            lid = lid + 1
        else:
            lid = 1
        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO laundry_service(laundry_id,username, submit_date, service_type, num_shirts, num_tshirts, num_shorts, num_pants, num_towels, num_suits, num_innerwears, num_kurtas, num_paijamas, num_skirts, image_file, stain_condition,delivery_date,delivery_address,delivery_status) VALUES('"+str(lid)+"','"+username+"','"+today+"','"+service+"','"+shirt+"','"+tshirt+"','"+shorts+"','"+pants+"','"+towels+"','"+suits+"','"+inner+"','"+kurta+"','"+paijama+"','"+skirt+"','"+imagename+"','"+result+"','"+delivery_date+"','"+address+"','Pending')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        context= {'data': 'Stains '+result+"<br/>Laundry data successfully saved in Databse", 'img': img_b64}
        return render(request, 'UserScreen.html', context) 
        

def LaundryServiceAction(request):
    if request.method == 'POST':
        # Check if user is logged in
        username = request.session.get('username', '')
        if not username:
            return redirect('/UserLogin')
            
        # Store form data in session instead of global variables
        request.session['service'] = request.POST.get('t1', False)
        request.session['shirt'] = request.POST.get('t2', False)
        request.session['tshirt'] = request.POST.get('t3', False)
        request.session['shorts'] = request.POST.get('t4', False)
        request.session['pants'] = request.POST.get('t5', False)
        request.session['towels'] = request.POST.get('t6', False)
        request.session['suits'] = request.POST.get('t7', False)
        request.session['inner'] = request.POST.get('t8', False)
        request.session['kurta'] = request.POST.get('t9', False)
        request.session['paijama'] = request.POST.get('t10', False)
        request.session['skirt'] = request.POST.get('t11', False)
        request.session['address'] = request.POST.get('t12', False)
        request.session['delivery_date'] = request.POST.get('t13', False)
           
        context= {'data': 'Upload Image'}
        return render(request, 'UploadImage.html', context)   

def YoloGraph(request):
    if request.method == 'GET':
        # Check if user is logged in
        if not request.session.get('username'):
            return redirect('/UserLogin')
            
        img = cv2.imread("model/results.png")
        img = cv2.resize(img, (1000, 800))
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        context= {'data': 'Yolo Performance Graph', 'img': img_b64}
        return render(request, 'UserScreen.html', context) 

def ViewLaundry(request):
    if request.method == 'GET':
        # Get username from session
        username = request.session.get('username', '')
        if not username:
            return render(request, 'UserLogin.html', {'data': 'Please login first'})
            
        output = '''
        <div class="card shadow mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="bi bi-clipboard-data me-2"></i>My Laundry Orders</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover table-striped">
                        <thead class="table-primary">
                            <tr>
                                <th>ID</th>
                                <th>Date</th>
                                <th>Service</th>
                                <th>Items</th>
                                <th>Stain Result</th>
                                <th>Delivery Date</th>
                                <th>Status</th>
                                <th>Image</th>
                            </tr>
                        </thead>
                        <tbody>
        '''
        
        con = get_db_connection()
        with con:
            cur = con.cursor()
            cur.execute("select * from laundry_service where username='"+username+"'")
            rows = cur.fetchall()
            
            for row in rows:
                # Calculate total items
                items_count = int(row[4]) + int(row[5]) + int(row[6]) + int(row[7]) + int(row[8]) + int(row[9]) + int(row[10]) + int(row[11]) + int(row[12]) + int(row[13])
                items_detail = []
                
                if int(row[4]) > 0: items_detail.append(f"{row[4]} Shirts")
                if int(row[5]) > 0: items_detail.append(f"{row[5]} T-Shirts")
                if int(row[6]) > 0: items_detail.append(f"{row[6]} Shorts")
                if int(row[7]) > 0: items_detail.append(f"{row[7]} Pants")
                if int(row[8]) > 0: items_detail.append(f"{row[8]} Towels")
                if int(row[9]) > 0: items_detail.append(f"{row[9]} Suits")
                if int(row[10]) > 0: items_detail.append(f"{row[10]} Inner Wear")
                if int(row[11]) > 0: items_detail.append(f"{row[11]} Kurtas")
                if int(row[12]) > 0: items_detail.append(f"{row[12]} Paijamas")
                if int(row[13]) > 0: items_detail.append(f"{row[13]} Skirts")
                
                items_html = f"<span class='badge bg-info text-dark'>{items_count} items</span><div class='small text-muted mt-1'>" + ", ".join(items_detail[:3])
                if len(items_detail) > 3:
                    items_html += f" <span class='text-primary'>+{len(items_detail)-3} more</span>"
                items_html += "</div>"
                
                # Format status with appropriate badge
                status = row[18]
                if status == "Pending":
                    status_badge = f"<span class='badge bg-warning text-dark'>{status}</span>"
                elif status == "Completed":
                    status_badge = f"<span class='badge bg-success'>{status}</span>"
                else:
                    status_badge = f"<span class='badge bg-primary'>{status}</span>"
                
                # Format date for better display
                laundry_date = row[2]
                
                output += f'''
                <tr>
                    <td><span class="fw-bold">#{row[0]}</span></td>
                    <td>{laundry_date}</td>
                    <td><span class="badge bg-primary">{row[3]}</span></td>
                    <td>{items_html}</td>
                    <td><span class="badge bg-{'success' if row[15]=='Found' else 'secondary'}">{row[15]}</span></td>
                    <td>{row[16]}</td>
                    <td>{status_badge}</td>
                    <td>
                        <a href="static/files/{row[14]}" data-lightbox="laundry-{row[0]}" data-title="Order #{row[0]} Image">
                            <img src="static/files/{row[14]}" class="img-thumbnail-custom" alt="Laundry Image" />
                        </a>
                    </td>
                </tr>
                '''
        
        output += '''
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        '''
        
        context = {'data': output}
        return render(request, 'UserScreen.html', context)            

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def LaundryService(request):
    if request.method == 'GET':
        # Check if user is logged in
        if not request.session.get('username'):
            return redirect('/UserLogin')
            
       return render(request, 'LaundryService.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
                
        status = "none"
        con = get_db_connection()
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = get_db_connection()
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup completed<br/>You can login with "+username
        context= {'data': status}
        return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        index = 0
        con = get_db_connection()
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    # Store username in session instead of global variable
                    request.session['username'] = username
                    index = 1                    
                    break		
        if index == 1:
            context= {'data':'Welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)                 

def Logout(request):
    if 'username' in request.session:
        del request.session['username']
        request.session.flush()  # Completely clear the session
    
    return redirect('/')  # Redirect to home page using the URL name


