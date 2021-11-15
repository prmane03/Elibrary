from django.shortcuts import render, HttpResponse,redirect
from .models import Bookstbl,Adminstbl,Userstbl
from django.contrib.sessions.models import Session
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'login.html')

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        isadmin = request.POST.get('isadmin')
        if(isadmin):
            try:
                admin = Adminstbl.objects.get(adminEmail=email)
                if (password == admin.Password):
                    request.session['username']=email
                    request.session['isadmin']=isadmin
                    request.session['islogged']=True
                    return redirect('/dashboard')
                    # return render(request,'dashboard.html',{'useremail':admin.adminEmail,'isadmin':True})
                else:
                    return render(request,'login.html',{'e':'Password Doesn`t Match'})
            except Exception as e:
                return render(request,'login.html',{'e':'Admin Dosen`t Exists'})
        else:
            try:
                user = Userstbl.objects.get(userEmail=email)
                if password == user.Password:
                    request.session['username']=email
                    request.session['isadmin']=isadmin
                    request.session['islogged']=True
                    return redirect('/dashboard')
                    # return render(request,'dashboard.html',{'useremail':user.userEmail,'isadmin':False})
                else:
                    return render(request,'login.html',{'e':'Password Doesn`t Match'})
            except Exception as e:
                return render(request,'login.html',{'e':'User Dosen`t Exists'})



    return render(request,'login.html')

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        name = fname+" "+lname
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        isadmin = request.POST.get('isadmin')
        
        if password == cpassword:
            if(isadmin):
                org = request.POST.get('org')
                admin = Adminstbl(Name=name,adminEmail=email,Password=password,Orgnization=org);
                admin.save()
                return redirect('/signin')
            else:
                adminemail = request.POST.get('adminemail')
                try:
                    admin = Adminstbl.objects.get(adminEmail=adminemail)
                    user = Userstbl(Name=name,userEmail=email,Password=password,admin=admin);
                    user.save()
                    return redirect('/signin')
                except Exception as e:
                    return render(request,'register.html',{'e':"check admin email"})
        else:
            return render(request,'register.html',{'e':"password dosen`t match"})
       
    return render(request,'register.html')

def dashboard(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if 'username' in request.session:
            username =  request.session['username']
            isadmin = request.session['isadmin']
            if(isadmin): 
                Admin = Adminstbl.objects.get(adminEmail=username)
                Books = Bookstbl.objects.filter(admin=Admin,isebook=False)
                Ebooks = Bookstbl.objects.filter(admin=Admin,isebook=True)
                return render(request,'dashboard.html',{'Ebooks':Ebooks,'Books':Books,'User':Admin})
            else:
                User = Userstbl.objects.get(userEmail=username)
                Books = Bookstbl.objects.filter(admin=User.admin,isebook=False)
                Ebooks = Bookstbl.objects.filter(admin=User.admin,isebook=True)
                return render(request,'dashboard.html',{'Ebooks':Ebooks,'Books':Books,'User':User})
    
def account(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if 'username' in request.session:
            username =  request.session['username']
            isadmin = request.session['isadmin']
            if(isadmin): 
                Admin = Adminstbl.objects.get(adminEmail=username)
                Students = Userstbl.objects.filter(admin=Admin)
                Books = Bookstbl.objects.filter(admin=Admin)
                fname,lname = Admin.Name.split(' ')
                return render(request,'profile-page.html',{'Books':Books,'User':Admin,'Students':Students,'fname':fname,'lname':lname})
            else:
                User = Userstbl.objects.get(userEmail=username)
                fname,lname = User.Name.split(' ')
                return render(request,'profile-page.html',{'User':User,'fname':fname,'lname':lname})
    
def logout(request):
    request.session.flush()
    return redirect('/signin')

def deletebook(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if request.method == "POST":
            book_id = request.POST.get('book_id')[1:]
            useremail = request.session['username']
            try: 
                admin = Adminstbl.objects.get(adminEmail=useremail)
            except Exception as e:
                return HttpResponse(e)
            
            Book = Bookstbl.objects.get(id=book_id,admin=admin);
            Book.delete()
        return redirect('/dashboard')

def addbook(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            publication = request.POST.get('publication')
            author = request.POST.get('author')
            category = request.POST.get('category')
            tcopies = request.POST.get('tcopies')
            useremail = request.session['username']
            isebook = request.POST.get('isebook',False)
            try: 
                admin = Adminstbl.objects.get(adminEmail=useremail)
            except Exception as e:
                return HttpResponse(e)
            if 'isebook' in request.POST:
                ebook = request.FILES['pdfebook']
                Book = Bookstbl(Name=name,Publication=publication,Author=author,Category=category,AvailableCopies=1,IssuedCopies=0,TotalCopies=1,admin=admin,isebook=True,Pdf_file=ebook);
            else:
                Book = Bookstbl(Name=name,Publication=publication,Author=author,Category=category,AvailableCopies=tcopies,IssuedCopies=0,TotalCopies=tcopies,admin=admin);
            Book.save()
        return redirect('/dashboard')


def updatebook(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if request.method == "POST":
            isebook = request.POST.get('isebook')
            book_id = request.POST.get('book_id')[1:]
            name = request.POST.get('name')
            publication = request.POST.get('publication')
            author = request.POST.get('author')
            category = request.POST.get('category')
            useremail = request.session['username']

            try: 
                admin = Adminstbl.objects.get(adminEmail=useremail)
            except Exception as e:
                return HttpResponse(e)
            

            Book = Bookstbl.objects.get(id=book_id,admin=admin);
            Book.Name = name
            Book.Publication = publication
            Book.Author = author
            Book.Category = category
            if  isebook == 'false':
                Book.AvailableCopies = request.POST.get('tcopies')
                Book.IssuedCopies = 0
                Book.TotalCopies = request.POST.get('tcopies')
            else :
                if request.FILES['update_ebook']:
                    Book.Pdf_file = request.FILES['update_ebook']
                else:
                    messages.warning(request,"Couldn't Update Book")
            Book.save()
        return redirect('/dashboard')

def completeprofile(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if request.method == "POST":
            # image = request.POST.get('image')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            birthday = request.POST.get('birthday')
            mobile = request.POST.get('mobile')
            useremail = request.session['username']
            isadmin = request.session['isadmin']
            try: 
                if(isadmin):
                    user = Adminstbl.objects.get(adminEmail=useremail)
                else:
                    user = Userstbl.objects.get(userEmail=useremail)
            except Exception as e:
                return HttpResponse(e)

            if len(request.FILES) != 0:
                image = request.FILES['image']
            else:
                image=user.Profile_pic

            user.Profile_pic = image
            user.Address = address
            user.Gender = gender
            user.Birthday = birthday
            user.Mobile = mobile
            messages.success(request,"Profile Updated")
            user.save()
        return redirect('/account')
    

def editprofile(request):
    if(not request.session.has_key("islogged")):
        return redirect('/logout')
    else:
        if request.method == "POST":
            # image = request.POST.get('image')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            name = fname+" "+lname
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            birthday = request.POST.get('birthday')
            mobile = request.POST.get('mobile')
            useremail = request.session['username']
            isadmin = request.session['isadmin']
            try: 
                if(isadmin):
                    user = Adminstbl.objects.get(adminEmail=useremail)
                else:
                    user = Userstbl.objects.get(userEmail=useremail)
            except Exception as e:
                return HttpResponse(e)

            if len(request.FILES) != 0:
                image = request.FILES['image']
            else:
                image=user.Profile_pic

            user.Name = name
            user.Profile_pic = image
            user.Address = address
            user.Gender = gender
            user.Birthday = birthday
            user.Mobile = mobile
            messages.success(request,"Profile Updated")
            user.save()
        return redirect('/account')
    
