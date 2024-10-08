from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
 
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
 
   path('initiate',views.initiatekhalti,name="initiate"),
#    path('verify',views.verifyKhalti,name="verify")

]