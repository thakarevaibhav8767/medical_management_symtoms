from django.shortcuts import render
from . import forms
from .models import medicines, diseas,orderdetails,admin1,customer,purchase
import pandas as pd

from django.utils.timezone import now
from datetime import datetime
from datetime import timedelta


def registerfrm(req):
    if req.method == 'POST':
        form = forms.registerfrm(req.POST)
        if form.is_valid():
            a1 =form.cleaned_data['User_Id']
            a = form.cleaned_data['User_Name']
            b = form.cleaned_data['Password']
            b2 = form.cleaned_data['confrm_pwd']
            c = form.cleaned_data['Gender']
            h = form.cleaned_data['Phone_Number']
            i = form.cleaned_data['Email']


            # Password confirmation check


            # Save the data to the database
            user_instance = customer(
                User_Id=a1, User_Name=a, Password=b, Gender=c,
                 Phone_Number=h, Email=i
            )
            user_instance.save()
            return render(req, 'register.html', {'msg': 'Record inserted successfully', 'form': forms.registerfrm()})
        else:
            # Handle invalid form case
            return render(req, 'register.html', {'form': form, 'msg': 'Invalid data, please try again'})
    else:
        # Handle GET request
        form = forms.registerfrm()
        return render(req, 'register.html', {'form': form})


def user1(req):
    if req.method=='POST':
        a = req.POST.get('userid')
        b = req.POST.get('password')
        try:
            c = customer.objects.get(User_Id=a)
            d = customer.objects.get(Password=b)
            return render(req, 'welcome.html', {'c': c, 'd': d})
        except Exception as e:
            msg = 'User id and password does not match'
            return render(req, 'userlogin.html', {'msg': msg})

    else:
        form1 = forms.user()
        return render(req, 'userlogin.html', {'form1': form1})

def admin2(req):
    if req.method=='POST':
        a=req.POST.get('adminid')
        b=req.POST.get('password')
        try:
            c=admin1.objects.get(Admin_Id=a)
            d=admin1.objects.get(Admin_password=b)
            return render(req,'Awelcome.html',{'c':c,'d':d})
        except Exception as e:
            msg='Your id  or password does not match '
            return  render(req,'adminlogin.html',{'msg':msg})
    else:
        form = forms.admin()
        return render(req,'adminlogin.html',{'form':form})
def home(req):
    return render(req,'home.html')
def aboutus(req):
   return render(req,'about.html')
def contactus(req):
    return render(req,'contactus.html')
def userlogin(req):
    if req.method=='POST':
        a = req.POST.get('userid')
        b = req.POST.get('password')
        try:
            c = customer.objects.get(User_Id=a)
            d = customer.objects.get(Password=b)
            return render(req, 'Uwelocme.html',{'c': c, 'd': d})
        except Exception as e:
            msg = 'User id and password does not match'
            return render(req, 'userlogin.html', {'msg': msg})

    else:
        form  = forms.user()
        return render(req, 'userlogin.html', {'form': form})

def adminlogin(req):
    if req.method=='POST':
        a=req.POST.get('adminid')
        b=req.POST.get('password')
        try:
            c=admin1.objects.get(Admin_Id=a)
            d=admin1.objects.get(Admin_password=b)
            return render(req,'Awelcome.html',{'c':c,'d':d})
        except Exception as e:
            msg='Your id  or password does not match '
            return  render(req,'adminlogin.html',{'msg':msg})
    else:
        form = forms.admin()
        return render(req,'adminlogin.html',{'form':form})
def uwelcome(req):
    return render(req,'Uwelocme.html')
def awelcome(req):
    return render(req,'Awelcome.html')

def insertmed(req):
    if req.method=='POST':
        a=int(req.POST.get('mid'))
        b=req.POST.get('mname')
        b2=int(req.POST.get('qun'))
        c=int(req.POST.get('prc'))
        e=req.POST.get('mfgdt')
        f=req.POST.get('expdt')
        g=medicines(med_Id=a,med_Name=b,Available_quantity=b2,Price=c,mfg_Date=e,Exp_Date=f)
        g.save()
        return render(req,'insert.html',{'msg':"inserted"})
    else:
        return render(req,'insert.html')
def updatemed(req):
    if req.method=='POST':
        a=req.POST.get('mid')
        try:
            b3 = medicines.objects.get(med_Id=a)
            c=req.POST.get('mname')
            d = req.POST.get('qun')
            e= req.POST.get('prc')
            f=req.POST.get('mfgdt')
            g= req.POST.get('expdt')
            h=medicines(med_Id=a,med_Name=c,Available_quantity=d,Price=e,mfg_Date=f,Exp_Date=g)

            h.save()
            msg = "Record Updated Successfully!"
        except medicines.DoesNotExist:
           msg = "Medicine ID not found!"
           b3 = None
        return render(req, 'update.html', {'b3': b3, 'msg': msg})
    else:
        return render(req, 'update.html')

def deleterec(req):
    if req.method=='POST':
        a=req.POST.get('medid')
        b=medicines.objects.get(med_Id=a)
        b.delete()
        msg='Record Deleted succesfully'
        return render(req,'delete.html',{'msg':msg})
    else:
        return render(req,'delete.html')
def display(req):
    a=medicines.objects.all()
    return render(req,'display.html',{'a':a})


def purchase_med(req):
    if 'cart' not in req.session:
        req.session['cart'] = []  # Initialize an empty cart in session

    if req.method == 'POST':
        a = int(req.POST.get('uid'))  # Get User ID
        req.session['user_id'] = a  # Store User ID in session

        b = req.POST.get('mid')  # Medicine ID
        c = req.POST.get('medname')  # Medicine Name
        d = int(req.POST.get('quan'))  # Quantity
        d1 = req.POST.get('date')  # Purchase Date

        try:
            e1 = medicines.objects.get(med_Id=b)
        except medicines.DoesNotExist:
            return render(req, 'purchase.html', {'msg': 'Medicine not found'})

        if d > e1.Available_quantity:
            return render(req, 'purchase.html', {'msg': 'Insufficient stock'})

        # ✅ Convert Decimal to float before storing in session
        price_per_unit = float(e1.Price)
        total_price= price_per_unit * d

        # Store the medicine details in session cart (Ensuring all values are JSON serializable)
        cart = req.session['cart']
        cart.append({
            'med_id': b,
            'med_name': c,
            'quantity': d,
            'date': d1,
            'price': price_per_unit,  # ✅ Ensure it's a float
            'total_price' : total_price
        })
        req.session['cart'] = cart  # Save back to session

        return render(req, 'purchase.html', {'msg': 'Medicine added! Add more or confirm purchase.'})

    elif req.GET.get('confirm') == '1':  # When user confirms purchase
        cart = req.session.get('cart', [])
        user_id = req.session.get('user_id')  # Retrieve stored User ID

        if not user_id:
            return render(req, 'purchase.html', {'msg': 'User ID missing. Please add a medicine first.'})

        if not cart:
            return render(req, 'purchase.html', {'msg': 'No medicines in cart'})

        medicines_list = []
        purchases_list = []

        for item in cart:
            try:
                med = medicines.objects.get(med_Id=item['med_id'])
            except medicines.DoesNotExist:
                return render(req, 'purchase.html', {'msg': f"Medicine {item['med_name']} not found"})

            if item['quantity'] > med.Available_quantity:
                return render(req, 'purchase.html', {'msg': f"Insufficient stock for {item['med_name']}"})

            # ✅ Ensure total_price is stored as a float before JSON operations
            total_price = float(item['quantity'] * item['price'])  # Convert to float

            med.Available_quantity -= item['quantity']

            purchase_entry = purchase(
                User_Id=user_id,
                med_id=item['med_id'],
                med_name=item['med_name'],
                quantity=item['quantity'],
                price=Decimal(total_price),  # ✅ Convert back to Decimal for database
                date=item['date']
            )

            medicines_list.append(med)
            purchases_list.append(purchase_entry)

        # Save all medicines and purchases
        for med in medicines_list:
            med.save()
        for purchase_entry in purchases_list:
            purchase_entry.save()

        req.session['cart'] = []  # Clear cart after purchase
        del req.session['user_id']  # Remove User ID from session

        return render(req, 'purchase.html', {'msg': 'Purchase completed successfully!'})

    return render(req, 'purchase.html')


def search(req):
    if req.method=='POST':
        a=req.POST.get('med')
        b=medicines.objects.get(med_Name=a)
        return render(req,'serch.html',{'b':b})
    else:
        return render(req,'serch.html')
def diseas_1(req):
    if req.method=='POST':
        a=req.POST.get('dis')
        b = req.POST.get('med')
        e=diseas(diseas1=a,medicines=b)
        e.save()
        return render(req,'diseas.html',{'msg':'Insearted Succesfully'})
    else:
        return render(req,'diseas.html')
def purchasehist(req):
    if req.method=='POST':
        a=req.POST.get('uid')
        b=req.POST.get('det')
        c=purchase.objects.filter(User_Id=a,date=b)
        return render(req,'order.html',{'c':c})
    else:
        return render(req,'order.html')


from decimal import Decimal
from django.shortcuts import render
from datetime import date
from .models import diseas  # Ensure your model is imported
from .predctions import disease_predictor  # Import the modified predictor


def symtoms(req):
    if req.method == 'POST':
        if 'predict_disease' in req.POST:
            req.session['cart'] = []  # Clear cart when new symptoms are submitted

            symptom1 = req.POST.get('symtom1', '').strip()
            symptom2 = req.POST.get('symtom2', '').strip()
            symptom3 = req.POST.get('symtom3', '').strip()
            symptoms = [symptom for symptom in [symptom1, symptom2, symptom3] if symptom]

            if not symptoms:
                return render(req, 'symtoms.html', {'msg': "Please enter at least one symptom."})

            # Use ML Model to Predict Disease
            predicted_disease = disease_predictor.predict_disease(symptoms)
            if "Prediction Error" in predicted_disease:
                return render(req, 'symtoms.html', {'msg': predicted_disease})

            # Fetch Disease Details from Database
            disease_obj = diseas.objects.filter(diseas1=predicted_disease).first()
            if not disease_obj:
                return render(req, 'symtoms.html', {'msg': "Disease not found in database."})

            # Get Recommended Medicines
            medicines_list = [med.strip() for med in disease_obj.medicines.split(",")]

            # Store Data in Session
            req.session['predicted_disease'] = predicted_disease
            req.session['medicines_list'] = medicines_list

            return render(req, 'symtoms.html', {
                'msg': f"Predicted Disease: {predicted_disease}",
                'medicines_list': medicines_list,
                'cart': req.session.get('cart', []),
                'today_date': date.today().isoformat()
            })

    return render(req, 'symtoms.html', {
        'medicines_list': req.session.get('medicines_list', []),
        'cart': req.session.get('cart', []),
        'today_date': date.today().isoformat()
    })
