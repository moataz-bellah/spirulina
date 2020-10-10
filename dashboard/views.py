from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pyrebase
import uuid
import json
config = {
    "apiKey": "AIzaSyCM_ndwendF8lbfck8tyY4_EOJtJ0WN5g4",
    "authDomain": "spirulinaproducts-9a7a4.firebaseapp.com",
    "databaseURL": "https://spirulinaproducts-9a7a4.firebaseio.com",
    "projectId": "spirulinaproducts-9a7a4",
    "storageBucket": "spirulinaproducts-9a7a4.appspot.com",
    "messagingSenderId": "703319341201",
    "appId": "1:703319341201:web:1795f61f6eb281e215a730",
    "measurementId": "G-FRLWXY1MQR"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
imgName = "Capture.PNG"
path_on_cloud = f"images/{imgName}"
path_local = "Capture.PNG"
cred = credentials.Certificate('./spirulinaproducts-9a7a4-firebase-adminsdk-8qwf7-3b5d20ff72.json')
default_app = firebase_admin.initialize_app(cred)


def dashboard(request):
    return render(request, 'admin2/dashboard.html', {})


def addProduct(request):
    db = firestore.client()
    restaurants = db.collection(u'restaurants').stream()
    data = [i.to_dict() for i in restaurants]
    ID = uuid.uuid4()
    print(str(ID))
    user = auth.sign_in_with_email_and_password('admin@admin.com', '123456')
    if request.method == 'POST':
        name = request.POST['name']
        price = int(request.POST['price'])
        about = request.POST['about']
        image = request.POST.get('url')
        restaurant = request.POST['rest']
        data = {
            'name': name, 'price': price, 'description': about,
             'image': image,'restaurantId': restaurant,
            'id': str(ID)
        }
        doc2 = db.collection(u'products').document(str(ID)).set(data)
        # db.collection(u'products').document(doc2[1].id).update({u"id":doc2[1].id})
    return render(request, 'admin2/add_product.html', {'doc': data})

def productsList(request):
    db = firestore.client()
    doc = db.collection(u'products').stream()
    restaurants = db.collection(u'restaurants').stream()
    data = [i.to_dict() for i in doc]
    return render(request,'admin2/products_list.html',{'doc':data})
def updateProduct(request,product_id):
    db = firestore.client()
    doc = db.collection(u'products').document(product_id).get().to_dict()
    doc2 = db.collection(u'products').document(product_id)
    restaurants = db.collection(u'restaurants').stream()
    rests = [i.to_dict() for i in restaurants]
    if request.method == 'POST':
        name = request.POST['name']
        price = int(request.POST['price'])
        about = request.POST['about']
        image = request.POST.get('url')
        restaurant = request.POST['rest']

        doc2.update({u"name":name,u"price":price,u"description":about,u'image':image,u'restaurantId':restaurant})
    return render(request,'admin2/update_product.html',{'doc':doc,'res':rests})
def deleteProduct(request,product_id):
    db = firestore.client()
    db.collection(u'products').document(product_id).delete()
    return HttpResponseRedirect('products_list')
def ordersListPage(request):
    db = firestore.client()
    doc = db.collection(u'orders').stream()
    data = [i.to_dict() for i in doc]
    cart = [j['cart'] for j in data]
    print(cart)
    #user = [l['userId'] for l in data]
    data2 = json.dumps(data)
    return render(request, 'admin2/orders_list.html', {'doc': data,'data':data2})
def viewOrderDetails(request,order_id):
  db = firestore.client()
  doc = db.collection(u'orders').document(order_id)
  data = doc.get().to_dict()
  user = db.collection(u"users").document(data['userId']).get().to_dict()
  return render(request,'admin2/view_order.html',{'doc':data,'user':user})
def viewCartDetails(request,order_id):
    db = firestore.client()
    doc = db.collection(u'orders').document(order_id).get().to_dict()
    cart = doc['cart']
    print(cart)
    return render(request,'admin2/view_cart.html',{'cart':cart})
