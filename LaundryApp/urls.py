from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="home"),
	       path("index.html", views.index, name="index"),
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('UserLogin', views.UserLogin, name="UserLogin_no_ext"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
	       path('Register.html', views.Register, name="Register"), 
	       path('Register', views.Register, name="Register_no_ext"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),
	       path('LaundryService', views.LaundryService, name="LaundryService"),
	       path('LaundryServiceAction', views.LaundryServiceAction, name="LaundryServiceAction"),	 
	       path('YoloGraph', views.YoloGraph, name="YoloGraph"),
	       path('ViewLaundry', views.ViewLaundry, name="ViewLaundry"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('AdminLogin', views.AdminLogin, name="AdminLogin_no_ext"),
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	       path('ViewCustomers', views.ViewCustomers, name="ViewCustomers"),
	       path('ViewOrderStatus', views.ViewOrderStatus, name="ViewOrderStatus"),
	       path('UploadImageAction', views.UploadImageAction, name="UploadImageAction"),
	       path('WriteDescription', views.WriteDescription, name="WriteDescription"), 
	       path('WriteDescriptionAction', views.WriteDescriptionAction, name="WriteDescriptionAction"),
               path('Logout', views.Logout, name="Logout"),
]