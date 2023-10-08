from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.db.models import Count
import json
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *
from .forms import *

# Create your views here.

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
razorpay_client.set_app_details({"title" : "Django", "version" : "4.0.4"})


def welcome(request):
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def pronites(request):
    return render(request, 'pronites.html')

def speakers(request):
    return render(request,'speakers.html')

def ifestTeam(request):
    ifestTeam = {
        "Mentors" : {
            "Prabhav Shah": "+91 91065 05620",
            "Rinkal Naik": "+91 70969 70451",
            "Siddharth Rathod": "+91 70460 98218",
            "Nirmit Ghughu": "+91 83809 01222",
            "Akshita Jindal": "+91 79996 79397",
            "Jaimit Joshi": "+91 93270 35369",
            "Miti Purohit": "+91 91069 54865",  
        },
        "PR Team" : {
            "Dhrupal Kukadia":"+91 63542 14284",
            "Om Jhaveri":"+91 84878 52103",
            "Divyam Oza":"+91 93133 58815",
            "Rishi Arora":"+91 85305 96040",
            "Vrishin Shah":"+91 91062 17688",
        },
        "Sponsorship" : {
            "Aryan Shah":"+91 92656 88299",
            "Harsh Patel":"+91 98792 79079",
            "Hemang Joshi":"+91 79849 80206",
            "Nilav Shah":"+91 90999 97204",
            "Aditya Tanna":"+91 76004 43472",
            "Arsh Jindal":"+91 96627 88275",
            "Dhruv Shah":"+91 92659 57423",
            "Nisha Savaliya":"+91 90548 48232",
            "Yash Kodwani":"+91 94093 94707",
        },
        "Content & Designing" : {
            "Aastha Shetty":"+91 94096 14997",
            "Dev Jadav":"+91 94265 80215",
            "Hitarth Vyas":"+91 70169 11050",
            "Priya Vinda":"+91 97273 69045",
            "Bhavya Shah":"+91 82000 90380",
            "Hirmi Patel":"+91 99252 08744",
            "Jahnvi Verma":"+91 90164 93012",
            "Mustafa Lokhandwala":"+91 99743 63143",
            "Sakshi Patadiya":"+91 63541 97694",
        },
        "Event Management" : {
            "Darshan Kheni":"+91 63566 05363",
            "Kathan Shah":"+91 90547 34134",
            "Pranav Patil":"+91 76239 55135",
            "Kenil Vaghasiya":"+91 63533 03550",
            "Dhruvil Thakor":"+91 63516 71439",
            "Jay Dobariya":"+91 98249 29996",
            "Manav Shah":"+91 95106 94577",
        },
        "Website Team" : {
            "Vishesh Patel":"+91 9428307630",
            "Shrey Pobaru":"+91 63542 49801",
            "Kavan Buch":"+91 78744 39824",
            "Divya Patel":"+91 91068 87095",
            "Devdeep JS":"+91 92658 16294",

            "Het Patel":"+91 70467 83821",
            "Adit Parekh":"+91 94266 15872",
            "Bhavya Dudhagara":"+91 88966 55557",
            "Jay Sanghani":"+91 99245 90036",
            "Jahanvi Thakkar":"+91 82003 30645"
        },
    }
    return render(request,'members.html', {"ifest" : ifestTeam})

def sponsors(request):
    return render(request,'sponsors.html')

def login_func(request):
    if request.user.is_anonymous == False:
        return redirect('profile')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_staff == False and user.profile.payment == False:
                # if user.profile.referral_code:
                #     CA = campusAmbassador.objects.filter(referralCode=user.profile.referral_code)
                #     newCount = CA[0].count - 1
                #     CA.update(
                #         count=newCount,
                #     )
                user.delete()
                messages.error(request,'Account does not exist.')
                return redirect("login_page")
            else:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('login_page')
    else :
        return render(request, 'registration/login.html')

def logout_func(request):
    logout(request)
    return redirect('home')


# def signup(request):
#     if request.user.is_anonymous==False:
#         return redirect('profile')
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST or None)
#         email = request.POST['email']
#         ieee_id = request.POST['ieee_id']
#         currency = 'INR'
#         amount = 10000  # Rs. 100
#         #if email.find("@daiict.ac.in") != -1:
#         #    if ieee_id:
#         #        amount = 5000 # Rs. 50
#         #    else:
#         #        amount = 10000  # Rs. 100
#         if ieee_id:
#             amount = 5000 # Rs. 50
#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                            currency=currency,
#                                                            payment_capture='0'))
#         #print(razorpay_order)
#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         razorpay_order_status = razorpay_order['status']
#         #callback_url = 'paymenthandler/'
#         # we need to pass these details to frontend.
#         #context = {}
#         #context['razorpay_order_id'] = razorpay_order_id
#         #context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         #context['razorpay_amount'] = amount
#         #context['currency'] = currency
#         #context['callback_url'] = callback_url
#         #context['form'] = form
#         #if User.objects.filter(username=request.POST['username']).exists():
#         #    messages.error(request, "The username you entered is already taken")
#         #    return redirect('signup')
#         if User.objects.filter(email=request.POST['email']).exists():
#             messages.error(request, "The email you entered is already registered")
#             return redirect('signup')
#         if request.POST['ieee_id']:
#             if Profile.objects.filter(ieee_id=request.POST['ieee_id']).exists():
#                 messages.error(request, "The IEEE ID you entered is already registered")
#                 return redirect('signup')
#         if request.POST['referral_code']:
#             if not campusAmbassador.objects.filter(referralCode=request.POST['referral_code']).exists():
#                 messages.error(request, "The referral code you entered is incorrect")
#                 return redirect('signup')
#         CA = campusAmbassador.objects.filter(referralCode=request.POST['referral_code'])
#         if form.is_valid():
#             if razorpay_order_status=='created':
#                 if CA:
#                     newCount = CA[0].count + 1
#                     CA.update(
#                         count=newCount,
#                     )
#                 form.save()
#                 user = form.save()
#                 user.refresh_from_db()  # load the profile instance created by the signal
#                 user.username = user.email
#                 #user.profile.DOB = form.cleaned_data.get('DOB')
#                 user.profile.university = form.cleaned_data.get('university')
#                 user.profile.contact_number = form.cleaned_data.get('contact_number')
#                 user.profile.ieee_id = form.cleaned_data.get('ieee_id')
#                 user.profile.referral_code = form.cleaned_data.get('referral_code')
#                 user.profile.payment = 0
#                 user.profile.order_id = razorpay_order_id
#                 user.save()
#                 #print(user)
#                 username = form.cleaned_data['email']
#                 razorpay_order['name'] = username
#                 #print(razorpay_order)
#                 return render(request, "register.html", {
#                     'userProfile': user,
#                     'payment': razorpay_order,
#                     #'callback_url': callback_url,
#                     'razor_key_id': settings.RAZOR_KEY_ID,
#                 })
#                 #messages.success(request, 'Account was created for ' + username)
#                 #return render(request, "registration/signup.html", {'form': form, 'payment':razorpay_order})
#                 #return redirect("login_page")
#                 #return redirect("register")
#         else:
#             messages.error(request, "Invalid form entries.")
#             return redirect('signup')
#     else:
#         return render(request, "registration/signup.html", {'form':form})
def signup(request):
    if request.user.is_anonymous == False:
        return redirect('profile')
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email']).exists():
            u = User.objects.get(email=request.POST['email'])
            if u.profile and not u.profile.payment:
                u.delete()
            else:
                messages.error(request, "The email you entered is already registered.")
                return redirect('signup')

        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "The passwords entered do not match.")
            return redirect('signup')

        if len(request.POST['password1']) < 8:
            messages.error(request, "Password must be of atleast 8 characters.")
            return redirect('signup')

        if request.POST.get('ieee_id', ''):
            if Profile.objects.filter(ieee_id=request.POST.get('ieee_id', '')).exists():
                messages.error(request, "The IEEE ID you entered is already registered.")
                return redirect('signup')

        form = CreateUserForm(request.POST or None)
        
            # if request.POST['referral_code']:
            #     if not campusAmbassador.objects.filter(referral_code=request.POST['referral_code']).exists():
            #         messages.error(request, "The referral code you entered is incorrect")
            #         return redirect('signup')

            #CA = campusAmbassador.objects.filter(referral_code=request.POST['referral_code'])

        if form.is_valid():
            user = form.save()
            #user.refresh_from_db()
            user.username = form.cleaned_data.get('email')
            user.profile.university = form.cleaned_data.get('university')
            user.profile.contact_number = form.cleaned_data.get('contact_number')
            user.profile.ieee_id = form.cleaned_data.get('ieee_id')
            user.profile.referral_code = form.cleaned_data.get('referral_code')
            user.profile.payment = False            # Is payment done ?
            passtype = request.POST.get('passtype', '')
            if passtype == "gold":
                user.profile.gold = True
            user.save()
        else:
            messages.error(request, "Invalid Form")
            return redirect('signup')

        if request.POST.get('payMethod') == "Online":
            currency = 'INR'
            email = request.POST.get('email')

            if request.POST.get('passtype') == "gold":
                amount = 600*100
            else:
                amount = 150*100

            if email.find("@daiict.ac.in") != -1:
                amount = 100*100
                # if ieee_id:
                #     amount = 50*100   # Rs. 50
                # else:
                #     amount = 100*100  # Rs. 100

            razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))
            razorpay_order_id = razorpay_order['id']
            # user.profile.order_id = razorpay_order_id

            razorpay = "https://razorpay.com/payment-button/pl_KUZgoST3g7fCfg/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button"
            if amount == 600*100:
                razorpay = "https://razorpay.com/payment-button/pl_KUZixexenxkv4C/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button"

            elif amount == 150*100:
                razorpay = "https://razorpay.com/payment-button/pl_KUZgoST3g7fCfg/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button"

            elif amount == 100*100:
                razorpay = "https://razorpay.com/payment-button/pl_KUZjexpVFbuNSo/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button"

            request.session['user'] = user.email
            request.session.set_expiry(0)

            return HttpResponseRedirect(razorpay)

            callback_url = 'paymenthandler/'

            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context['form'] = form
            context['razorpay'] = 1

            return render(request, "signup22.html", context=context)

        else:   # Offline Payment
            return redirect('authenticate', username=user.username)

                # html_text = render_to_string('registrationEmail.html', {'user':user})
                # plain_text = strip_tags(html_text)
                # send_mail(
                #     subject="i.Fest '22 : Registeration Successful",
                #     from_email='ieee_noreply@daiict.ac.in',
                #     recipient_list=[user.email],
                #     message=plain_text,
                #     html_message=html_text,
                # )

    form = CreateUserForm()
    return render(request, "signup22.html", {'form':form})


# @csrf_exempt
# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
            
#             user = User.object.get(order_id=razorpay_order_id)
#             print(user)

#             if user.profile.gold == True:
#                 amount = 600*100
#             else:
#                 amount = 150*100

#             if user.email.find("@daiict.ac.in") != -1:
#                 amount = 100*100
#                 # if user.profile.ieee_id:
#                 #     amount = 50*100   # Rs. 50
#                 # else:
#                 #     amount = 100*100

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             if result is not None: 
#                 try:
#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)
#                     # render success page on successful caputre of payment
#                     user.profile.payment = True
#                     return render(request, 'success.html')
#                 except:
#                     # if there is an error while capturing payment.
#                     return render(request, 'fail.html')
#             else:
#                 # if signature verification fails.
#                 return render(request, 'fail.html')
#         except:
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()


def staffAuth(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('signup')
    
    if user.profile.payment == True:
        return redirect('login_page')

    if request.method == 'POST':
        staffUsername = request.POST['staff_username']
        staffPass = request.POST['staff_pass']
        staffUser = authenticate(request, username=staffUsername, password=staffPass)

        if staffUser is None or (not staffUser.is_staff):
            messages.error(request, "Staff Authentication Failed.")
            return redirect('authenticate', username=username)
        else:
            user.profile.payment = True
            user.profile.staffAuth = staffUser.get_full_name()
            user.save()
            return redirect('offlinesuccess')

    return render(request, 'staffauth.html')


def success(request, amount):
    if not request.session.get('user'):
        return redirect('home')

    if User.objects.filter(username=request.session.get('user')).exists():
        user = User.objects.get(username=request.session['user'])
        user.profile.payment = True
        user.profile.amount = amount
        user.profile.payment_id = request.GET.get('payment_id', '')
        user.save()
        request.session.pop('user')
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html')


def offlinesuccess(request):
    return render(request, 'success.html')


def events(request):
    events = Event.objects.all()
    return render(request,'events.html',{"events": events})

@login_required(login_url='login_page')
def dashboard(request):
    registrations = Registration.objects.filter(userProfile=request.user)
    events = []
    for registration in registrations:
        events.append(registration.event)
    if events:
        return render(request,'events.html',{"events":events,
                                             "dashboard": "1"})
    else:
        return render(request,'events.html',{"dashboard": "1"})

def moreInfo(request):
    user = request.user
    event_id = request.GET.get('id')
    event = Event.objects.filter(id=event_id)
    reg = not event[0].paid
    if request.user.is_anonymous==False:
        registration = Registration.objects.filter(userProfile=user).filter(event=event[0])
        flag = 0
        if registration:
            flag = 1
        if request.method == 'GET':
            now = datetime.datetime.now()
            if flag:
                return render(request, 'moreInfo.html', {
                    "event": event[0],
                    "now": now,
                    "button": 'De-Register',
                    "links": "links",
                    "register":reg,
                })
            else:
                return render(request,'moreInfo.html', {
                    "event": event[0],
                    "now": now,
                    "button": 'Register',
                    "register":reg,
                })
        else:
            if flag == 0:
                #if (event[0].paid==1 and user.profile.payment==1) or event[0].paid==0 :
                if user.profile.payment==1:
                    new_registration = Registration.objects.create(
                        userProfile = user,
                        event = event[0],
                    )
                    new_registration.save()
                    messages.success(request, f"You have successfully registered for {event[0].name}.")
                    return redirect('events')
                else:
                    user.delete()
                    return redirect('login_page')
            else:
                registration.delete()
                messages.success(request, f"You have de-registered from {event[0].name}.")
                return redirect('dashboard')
    else:
        now = datetime.datetime.now()
        return render(request, 'moreInfo.html', {
            "event": event[0],
            "now": now,
            "button": 'Register',
            "register":reg,
        })


@login_required(login_url='login_page')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login_page')
def editProfile(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id)
    form = UpdateUserForm(initial={
        'first_name': user[0].first_name,
        'last_name': user[0].last_name,
        'university': user[0].profile.university,
        'contact_number': user[0].profile.contact_number,
    })
    if request.method == 'GET':
        return render(request, 'editProfile.html', {
            'form': form
        })
    else:
        form = UpdateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            #DOB = form.cleaned_data.get('DOB')
            university = form.cleaned_data.get('university')
            contact_number = form.cleaned_data.get('contact_number')
            user.first_name = first_name
            user.last_name = last_name
            #user.profile.DOB = DOB
            user.profile.university = university
            user.profile.contact_number = contact_number
            user.save()
            return redirect('profile')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('editProfile')




@staff_member_required()
def uploadData(request):
    if request.method == "POST":
        csvfile = request.FILES['csvfile']
        csvdata = csvfile.read().decode("utf-8-sig")
        data = csvdata.split('\r\n')
        header = data.pop(0)
        header = header.split(',')
        failed = []
        for line in data:
            if not line:
                continue
            fields = line.split(',')
            email = fields[header.index('email_id')]
            first_name = fields[header.index('first_name')]
            last_name = fields[header.index('last_name')]
            contact_number = fields[header.index('contact_number')]
            payment_id = fields[header.index('payment_id')]
            college = fields[header.index('college')]
            if request.POST['pass'] == 'gold':
                gold = True
            else:
                gold = False
            amount = fields[header.index('amount')]
            try:
                user = User.objects.create_user(username=email, email=email, password=contact_number, first_name=first_name, last_name=last_name)
                user.profile.payment = True
                user.profile.university = college
                user.profile.contact_number = contact_number
                user.profile.payment_id = payment_id
                user.profile.gold = gold
                user.profile.amount = amount
                user.save()
            except:
                failed.append(email)
        return render(request, 'upload.html', {'failed':failed})
    return render(request, 'upload.html')


@staff_member_required()
def Stats(request):
    goldPass = Profile.objects.filter(payment=True, gold=True)
    eventData = Registration.objects.values('event__name').annotate(count=Count('event')).order_by('count')
    collegeData = Profile.objects.filter(payment=True).values('university').annotate(count=Count('university')).order_by('count')
    print(collegeData)
    return render(request, 'stats.html', {'gold':goldPass, 'eventData':eventData, 'collegeData':collegeData})