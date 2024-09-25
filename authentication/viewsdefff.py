# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .models import PublisherTable as Publisher
from .models import PassengerTable as Passenger
from .models import ClientTable as Client
from .models import PassengerDTable 
from .models import PublisherDTable
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime
from django.core.mail import send_mail
# Define a view function for the home page
def home(request):

    return render(request, 'home.html')

# Define a view function for the login page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_name'] = user.username
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            return redirect('/mainpage/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
    return render(request, 'login.html')

# Define a view function for the registration page
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        dob = request.POST.get('dateofbirth')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phonenumber')
        email = request.POST.get('email')
        e=str(email)
        #print(e)
        p=str(phone_number)
        profile_pic = request.FILES.get('profile_pic')  # Use FILES to get file uploads

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        # Parse the date of birth and calculate age
        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        age = calculate_age(birthdate)
        # Check if profile picture is uploaded; if not, use default
        if not profile_pic:
            default_profile_pic = 'profile_pics/download_1TlHrl9.png'
        else:
            default_profile_pic = profile_pic

        # Create client profile
        client = Client.objects.create(
            username=username,
            age=age,
            gender=gender,
            phone_number=p,
            email=e,
            profile_pic=default_profile_pic,
        )
        client.save()

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username

        )
        user.set_password(password)
        user.save()
        # Send welcome email
        subject = 'Welcome to RideShare!'
        message = f'Dear {first_name},\n\nWelcome to RideShare! We are excited to have you as a part of our community. ' \
                  f'Feel free to explore and enjoy our services.\n\nBest Regards,\nThe RideShare Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.info(request, "Account created successfully! A welcome email has been sent.")
        except Exception as e:
            messages.warning(request, f"Account created successfully, but there was an error sending the welcome email: {e}")

        return redirect('/login/')

    return render(request, 'register.html')

   

# Custom decorator to check if the user is logged in
def login_required_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_name' not in request.session:
            messages.error(request, "You need to log in first.")
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_decorator
def main_page(request):
    user_name = request.session.get('user_name')
    return render(request, 'mainpage.html', {'user_name': user_name})

@login_required_decorator
def publisher_page(request):
    user_name = request.session.get('user_name')
    return render(request, 'publisher.html')

@login_required_decorator
def publisher_database(request):
    if request.method == "POST":
        username = request.session['user_name']
        c = Client.objects.get(username__iexact=username)
        phonenumber = c.phone_number
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        date = request.POST.get("date")
        time = request.POST.get("time")
        seats = request.POST.get("seats")
        wheeler = request.POST.get("wheeler")
        vehicle = request.POST.get("vehicle")
        discription = request.POST.get("discription")
        print(date,"date")
        # Check if a ride with the same publisher and date already exists
        existing_rides = Publisher.objects.filter(username=username, date=date)
        if existing_rides.exists():
            messages.error(request, "A ride on the same date already exists. You cannot publish another ride on the same date.")
            return redirect("/publisher/")  # Adjust this to the appropriate page
        print(date,existing_rides ,"ex sdara")
        # If no existing ride is found, save the new ride
        pub = Publisher(
            username=username,
            phoneNumber=phonenumber,
            source=source,
            destination=destination,
            date=date,
            time=time,
            seats=seats,
            wheele=wheeler,
            vehicle=vehicle,
            discription=discription,
            requested_by="EMO"
        )
        pub.save()
        return redirect("/mainpage/")
    else:
        return redirect("/publisher/")  # Adjust this to the appropriate page if accessed via GET request


@login_required_decorator
def request_page(request):
    return render(request, "Request.html")


@login_required_decorator
def search_for_publisher(request):
    name = request.session['user_name'].strip()
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        pub = Publisher.objects.filter(source=source, destination=destination)
        a=[]
        if not pub:
            messages.error(request, "No publishers found")
            return redirect("/mainpage/")    
        for p in pub:
            if not p.username==name:
                if p.req1!=name and p.req2!=name and p.req3!=name and p.req1!=name+"None" and p.req2!=name+"None" and p.req3!=name+"None":
                    b=[]
                    name1=p.username
                    c=Client.objects.filter(username__iexact=name1)
                    for i in c:
                        b.append(i.username)
                        b.append(i.gender)
                        b.append(i.age)
                        b.append(i.rating)
                    for req in [p.req1,p.req2,p.req3]:
                        if  "None" in  req or "NONE" in req:
                            b.append("@")
                            b.append("@")
                            b.append("@")
                            b.append("@")  
                        else:    
                            name1=req
                            c=Client.objects.filter(username__iexact=name1)
                            for i in c:
                                b.append(i.username)
                                b.append(i.gender)
                                b.append(i.age)
                                b.append(i.rating)       
                    b.append(p.source)        
                    b.append(p.destination)
                    b.append(p.date)
                    b.append(p.time)
                    b.append(p.seats)
                    b.append(p.wheele)
                    b.append(p.vehicle)
                    a.append(b)        
        context = {'a': a}
        return render(request, "Request.html", context)
    return redirect("/mainpage/")

@login_required_decorator
def chat_page(request):
    name = request.session['user_name'].strip()
    pub = Publisher.objects.filter(username__iexact=name)
    #print("Queryset:", pub)

    if pub.exists():
        users = []
        for publisher in pub:
            s = int(publisher.seats)
            if s > 0:
                for req in [publisher.req1, publisher.req2, publisher.req3]:
                    if "None" in req:
                        a = req.replace("None", "")
                        c=Client.objects.filter(username__iexact=a)
                        b=[]
                        for i in c:
                            b.append(i.username)
                            b.append(i.rating)
                            b.append(i.gender)
                            b.append(i.age)
                        b.append(publisher.date)
                        b.append(publisher.time)
                        users.append(b)    
                
        print(users,"u")
        return render(request, 'chat.html', {'users': users})
    else:
        messages.error(request, "Publisher not found")
        return redirect("/chat/")

@login_required_decorator
def sendingrequest_page(request):
    if request.method == "POST":
        name = request.session['user_name']
        publishername = request.POST.get("publishername").strip()
        pub = Publisher.objects.filter(username__iexact=publishername)
        if pub.exists():
            for publisher in pub:
                s = int(publisher.seats)
                if publisher.req1 == "NONE" and s > 0:
                    publisher.req1 = name + "None"
                elif publisher.req2 == "NONE" and s > 0:
                    publisher.req2 = name + "None"
                elif publisher.req3 == "NONE" and s > 0:
                    publisher.req3 = name + "None"
                else:
                    messages.error(request, "Seats are full")
                    return redirect("/mainpage/")
                publisher.save()

                # Send email notification to publisher
                try:
                    client = Client.objects.get(username__iexact=publishername)
                    if client.email:
                        subject = 'New Ride Request'
                        message = f'Hello {publishername},\n\nYou have received a new ride request from {name}.'
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [client.email])
                        messages.info(request, "Request sent successfully and notification email sent to the publisher.")
                    else:
                        messages.info(request, "Request sent successfully, but no email found for the publisher to notify.")
                except Client.DoesNotExist:
                    messages.error(request, "Request sent successfully, but publisher email not found.")
                except Exception as e:
                    messages.error(request, f"Error sending email: {e}")

                return redirect("/mainpage/")
        else:
            messages.error(request, "Something went wrong")
            return redirect("/mainpage/")
    else:
        messages.error(request, "Something went wrong")
        return redirect("/mainpage/")

from django.conf import settings


@login_required_decorator
def acceptrequest_page(request):
    if request.method == "POST":
        name = request.session['user_name'].strip()
        date=request.POST.get("date") 
        time=request.POST.get("time")
        pub = Publisher.objects.filter(username__iexact=name)
        username = request.POST.get("username").strip()
        print(date,"datuu ")

        clean_time = time.replace('.', '').lower()
        date_iso = time.replace('.', '').lower()

        try:
            clean_time = datetime.strptime(clean_time, '%I:%M %p').strftime('%H:%M') 
        except ValueError as e:
            print(f"Error parsing time: {e}")
        try:
            date_iso = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")    
            messages.error(request, "Invalid time format.")
        t=str(clean_time)    
        d=str(date_iso)
        pub= Publisher.objects.filter(username__iexact=name,date=d)
        for publisher in pub:
            dd=str(publisher.date)
            print("hi im in acc pub")
            print(d,dd,"hi bef if")
            if d in dd:
                print(d,dd)
                s = int(publisher.seats)
                if s > 0:
                    if username + "None" in publisher.req1:
                        publisher.req1 = username
                        s -= 1
                    elif username + "None" in publisher.req2:
                        publisher.req2 = username
                        s -= 1
                    elif username + "None" in publisher.req3:
                        publisher.req3 = username
                        s -= 1
                    publisher.seats = str(s)
                    publisher.save()
                    
                else:
                    messages.error(request, "No available seats")
                    return redirect("/chat/")
        
        # Save the accepted passenger information
        pas = Passenger(
            username1=username,
            username2=name
        )
        pas.save()

        # Send email notification
        try:
            client = Client.objects.get(username__iexact=username)
            if client.email:
                subject = 'Ride Request Accepted'
                message = f'Hello {username},\n\nYour ride request has been accepted by {name}. \n\n Wanna chat with you co-passengers and publisher here is the room id {name} '
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [client.email])
                messages.info(request, f"Accepted {username} and notification email sent.")
            else:
                messages.info(request, f"Accepted {username}, but no email found to notify.")
        except Client.DoesNotExist:
            messages.error(request, f"Accepted {username}, but user email not found.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("/chat/")
    else:
        messages.error(request, "Something went wrong")
        return redirect("/chat/")



@login_required_decorator
def rejectrequest_page(request):
    if request.method == "POST":
        name = request.session['user_name'].strip()
        pub = Publisher.objects.filter(username__iexact=name)
        username = request.POST.get("username").strip()
        


        date=request.POST.get("date") 
        time=request.POST.get("time")
        pub = Publisher.objects.filter(username__iexact=name)
        username = request.POST.get("username").strip()
        print(date,"datuu ")

        clean_time = time.replace('.', '').lower()
        date_iso = time.replace('.', '').lower()

        try:
            clean_time = datetime.strptime(clean_time, '%I:%M %p').strftime('%H:%M') 
        except ValueError as e:
            print(f"Error parsing time: {e}")
        try:
            date_iso = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")    
            messages.error(request, "Invalid time format.")
        t=str(clean_time)    
        d=str(date_iso)
        pub= Publisher.objects.filter(username__iexact=name)
        for publisher in pub:
            dd=str(publisher.date)
            print("hi im in acc pub")
            print(d,dd,"hi bef if")
            if d in dd:
                print(d,dd)
                if username + "None" in publisher.req1:
                    publisher.req1 = "NONE"
                    request_rejected = True
                elif username + "None" in publisher.req2:
                    publisher.req2 = "NONE"
                    request_rejected = True
                elif username + "None" in publisher.req3:
                    publisher.req3 = "NONE"
                    request_rejected = True
                publisher.save()
        
        if request_rejected:
            # Send email notification
            try:
                client = Client.objects.get(username__iexact=username)
                if client.email:
                    subject = 'Ride Request Rejected'
                    message = f'Hello {username},\n\nYour ride request has been rejected by {name}.'
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [client.email])
                    messages.info(request, f"Rejected {username} and notification email sent.")
                else:
                    messages.info(request, f"Rejected {username}, but no email found to notify.")
            except Client.DoesNotExist:
                messages.error(request, f"Rejected {username}, but user email not found.")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
        else:
            messages.info(request, f"No pending request from {username} found to reject.")
        
        return redirect("/mainpage/")
    else:
        messages.error(request, "Something went wrong")
        return redirect("/mainpage/")


from django.contrib.auth.models import User
from django.db.models import TextField
@login_required_decorator
def profile_page(request):
    try:
        name = request.session['user_name'].strip()
        u= User.objects.get(username__iexact=name)

        user_info = []
        user_info.append(u.username)
        user_info.append(u.first_name) 
        user_info.append(u.last_name)

        u= Client.objects.get(username__iexact=name)
        user_info.append(u.email)
        user_info.append(u.phone_number) 
        user_info.append(u.age)
        user_info.append(u.gender)
        user_info.append(u.rating)
        user_info.append(u.profile_pic)
        #print(u.profile_pic)


    except User.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("/mainpage/")

    context = {
        'user_info': user_info,
    }

    return render(request, 'profile.html', context)

@login_required_decorator
def edit_page(request):
    user = request.user
    client_data = Client.objects.get(username=user.username)

    context = {
        'user': client_data,
        'first_name': user.first_name,  # Accessing first name from the User model
        'last_name': user.last_name,
    }
    return render(request, 'edit.html', context)

@login_required_decorator    
def edited_page(request):
    try:
        name = request.session['user_name'].strip()
        u= User.objects.get(username__iexact=name)
        c=Client.objects.get(username__iexact=name)
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email") 
        phonenumber = request.POST.get("phonenumber")
        p=str(phonenumber)
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        profile_pic= request.POST.get("profile_pic")
        if username:

            if User.objects.filter(username=username).exists() and username != name:
                messages.info(request, "Username already taken!")
                return redirect('/edit/')
            u.username=username
            c.username=username    
        if first_name:

            u.first_name=first_name
        if last_name:

            u.last_name=last_name
        if email:

            c.email=email
        if phonenumber:

            c.phone_number=p
        if age:

            c.age=age
        if gender:
            
            c.gender=gender
        if profile_pic:
            c.profile_pic=profile_pic                    
        u.save()    
        c.save()
        messages.info(request, "succesfull")
        return redirect('/mainpage/')
    except:
        messages.error(request, "somthing went wrong")
        return redirect('/login/')



def delete_published_ride(request):
    name = request.session['user_name'].strip()
    source = request.POST.get('source')
    destination = request.POST.get('destination')
    
    
    time = request.POST.get('time')
    date=request.POST.get("date")
    clean_time = time.replace('.', '').lower()
    date_iso = time.replace('.', '').lower()

    try:
        clean_time = datetime.strptime(clean_time, '%I:%M %p').strftime('%H:%M') 
    except ValueError as e:
        print(f"Error parsing time: {e}")
    try:
        date_iso = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error parsing date: {e}")    
        messages.error(request, "Invalid time format.")
    t=str(clean_time)    
    d=str(date_iso)
    pub= Publisher.objects.filter(username__iexact=name)
    a=[]
    for p in pub:
        tt=str(p.time)
        dd=str(p.date)
        #print(p.source,source,p.time,tt,p.date,dd)  
        if t in tt and d in dd and source==p.source:

            for req in [p.req1,p.req2,p.req3]:
                if req!="NONE" and not "None" in req:
                    c= Client.objects.filter(username__iexact=req)
                    for i in c:
                        a.append(i.email)  
            p.delete()            
    notify_copassengers(name,a,source,destination,date,time)
    return redirect('/your_rides/')
    
from django.conf import settings

def notify_copassengers(username,sendMail,source,destination,date,time):

    if sendMail:
        subject = 'Ride Cancellation Notification'
        message = f'The ride from {source} to {destination} on {date} at {time} has been canceled by the {username}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(sendMail))

def delete_passenger_ride(request):
    name = request.session['user_name'].strip()
    source = request.POST.get('source')
    time = request.POST.get('time')
    date=request.POST.get("date")
    head=request.POST.get("head")
    clean_time = time.replace('.', '').lower()
    date_iso = time.replace('.', '').lower()

    try:
        clean_time = datetime.strptime(clean_time, '%I:%M %p').strftime('%H:%M') 
    except ValueError as e:
        print(f"Error parsing time: {e}")
    try:
        date_iso = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error parsing date: {e}")    
        messages.error(request, "Invalid time format.")
    t=str(clean_time)    
    d=str(date_iso)
    pub= Publisher.objects.filter(username__iexact=head)
    for p in pub:
        tt=str(p.time)
        dd=str(p.date)
        #print(p.source,source,p.time,tt,p.date,dd)  
        if t in tt and d in dd and source==p.source:

            if p.req1==name:
                pasd=PassengerDTable.objects.create(
                username2=head,
                username1=name,
                )
                pasd.save()
                #print(p.req1)
                p.req1="NONE"
                p.seats=str(int(p.seats)+1)
                p.save()
                #print(p.req1)
                #print("DONE")

            if p.req2==name:
                pasd=PassengerDTable.objects.create(
                username2=head,
                username1=name,
                )
                pasd.save()
                p.req2="NONE"
                p.seats=str(int(p.seats)+1)
                p.save()

            if p.req3==name:
                pasd=PassengerDTable.objects.create(
                username2=head,
                username1=name,
                )
                pasd.save()
                p.req3="NONE"
                p.seats=str(int(p.seats)+1)
                p.save()
    pas= Passenger.objects.filter(username1=name,username2=head)        
    for p in pas:
        p.delete()
        break
    c=Client.objects.filter(username__iexact=head)    
    name1=""
    for i in c:
        name1=i.email
        break
    a=[name1]    
    notify_copassengers2(name,a)
    return redirect('/your_rides/')

def notify_copassengers2(username,sendMail):

    if sendMail:
        subject = 'Ride Cancellation Notification'
        message = f'your co passenger {username} has canceled the ride.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(sendMail))

 
@login_required_decorator 
def yourrides_page(request): 
    name = request.session['user_name'].strip() 
    publishers = Publisher.objects.filter(username__iexact=name) 
    passengers = Passenger.objects.filter(username1__iexact=name) 
    pub_details = [] 
    for publisher in publishers: 
        p=[name] 
        for req in [publisher.req1, publisher.req2, publisher.req3]:
             
            if not "none" in req.lower(): 
                print(req) 
                p.append(req) 
        pub_details.append((publisher.source, publisher.destination, publisher.date, publisher.time, publisher.vehicle, p)) 
    for i in pub_details: 
        print(i)     
 
    pass_details = [] 
    pp=[] 
    for passenger in passengers: 
        associated_publishers = Publisher.objects.filter(username__iexact=passenger.username2) 
        for publisher in associated_publishers: 
            pp= [passenger.username2] 
            for req in [publisher.req1, publisher.req2, publisher.req3]: 
                if not "none" in req.lower(): 
                    if "over" in req: 
                        req=req[0:-4] 
                    pp.append(req) 
            pass_details.append((publisher.source, publisher.destination, publisher.date, publisher.time, publisher.vehicle, pp)) 
    context = { 
        'pub_details': pub_details, 
        'pass_details': pass_details, 
    } 
 
    return render(request, 'your_rides.html', context) 


def thank_you(request):
    return render(request, 'thank_you.html')
from .models import PublisherTable, PassengerTable, ClientTable

from datetime import datetime

@login_required_decorator 


def finish_ride(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        time = request.POST.get('time')
        date = request.POST.get('date')

        clean_time = time.replace('.', '').lower()
        date_iso = date.replace('.', '').lower()

        if time.lower() == "midnight":
            clean_time = "00:00"
        else:
            try:
                clean_time = datetime.strptime(clean_time, '%I:%M %p').strftime('%H:%M')
            except ValueError as e:
                print(f"Error parsing time: {e}")

        try:
            date_iso = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")
            messages.error(request, "Invalid date format.")

        t = str(clean_time)
        d = str(date_iso)

        user_name = request.session['user_name'].strip()
        co_travelers = []
        publisher_name = None
        #print("pubrides")
        try:
            pub_rides = PublisherTable.objects.filter(source=source, destination=destination, date=d, time=t)
            pass_rides = PassengerTable.objects.filter(username1=user_name)

            if pub_rides.exists() and pub_rides.filter(finished=True).exists():
                return redirect('thank_you')

            if pass_rides.exists() and pass_rides.filter(finished=True).exists():
                return redirect('thank_you')

            for pub_ride in pub_rides:
                if pub_ride.username == user_name:  # User is the publisher
                    co_travelers.extend([req for req in [pub_ride.req1, pub_ride.req2, pub_ride.req3] if req and req != "NONE" and req != user_name])
                else:  # User is a passenger
                    publisher_name = pub_ride.username
                    co_travelers.extend([req for req in [pub_ride.req1, pub_ride.req2, pub_ride.req3] if req and req != "NONE" and req != user_name])

        except PublisherTable.DoesNotExist:
            pub_rides = None

                   

        print(f"Co-travelers: {co_travelers}")

        if not co_travelers and not publisher_name:
            messages.error(request, "No co-travelers found for this ride.")
            return redirect('your_rides')

        travelers = ClientTable.objects.filter(username__in=co_travelers)
        if publisher_name and publisher_name != user_name:
            travelers |= ClientTable.objects.filter(username=publisher_name)

        print(f"Travelers: {travelers}")
        ride_details = f"{source}|{destination}|{date_iso}|{clean_time}"
        return render(request, 'rate_ride.html', {'travelers': travelers, 'ride_details': ride_details})
    else:
        return redirect('rate_ride.html')

@login_required
def submit_rating(request):
    if request.method == 'POST':
        ride_details = request.POST.get('ride_details')
        if not ride_details:
            messages.error(request, "No ride details provided.")
            return redirect('your_rides')

        source, destination, date, time = ride_details.split('|')
        user_name = request.session['user_name'].strip()

        pub_ride = PublisherTable.objects.filter(source=source, destination=destination, date=date, time=time, username=user_name).first()
        pass_ride = PassengerTable.objects.filter(username1=user_name).first()

        if pub_ride:
            pub_ride.finished = True
            pub_ride.save()
        elif pass_ride:
            pass_ride.finished = True
            pass_ride.save()

        for key, value in request.POST.items():
            if key.startswith('rating_'):
                username = key.split('rating_')[1]
                rating = int(value)

                try:
                    client = ClientTable.objects.get(username=username)
                    client.sumofrating += rating
                    client.ppl += 1
                    client.rating = client.sumofrating / client.ppl
                    client.save()
                except ClientTable.DoesNotExist:
                    messages.error(request, f"Client {username} does not exist.")
                    continue

        messages.success(request, 'Ratings submitted successfully.')
        return redirect('thank_you')
    else:
        return redirect('your_rides')



