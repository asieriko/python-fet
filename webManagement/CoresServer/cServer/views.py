from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import os

from .models import Computer,Thread,Assignment,File,Result
from .forms import AssignementForm, FileForm

def status_page(request, computer, thread):
    comp = Computer.objects.get(name=computer)
    thr = Thread.objects.filter(computer=comp,name=thread)
    if thr[0].active:
        assig = Assignment.objects.filter(thread=thr)
        return JsonResponse({'status':'active','file_id':str(assig[0].fetfile.id),'file_name':str(assig[0].fetfile.name),'file':str(assig[0].fetfile.fetfile)})
    else:
        return JsonResponse({'status':'Stop'})

def return_file(request,file_id):
    print("return_file",file_id)
    file = File.objects.get(pk=file_id)
    file_path = file.fetfile.path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return "Error"

def show_results(request):
    rs = Result.objects.all()
    return render(request,"results.html",{'results':rs})

def return_result_fet(request,file_id):
    print(file_id)
    r = Result.objects.get(pk=file_id)
    file_path = r.rfile.path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Access-Control-Allow-Origin'] = '*'
            return response
    print("Error")
    return HttpResponse('<h1>Error</h1>')

def return_result_teacher(request,file_id):
    print(file_id)
    r = Result.objects.get(pk=file_id)
    file_path = r.tfile.path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Access-Control-Allow-Origin'] = '*'
            return response
    print("Error")
    return HttpResponse('<h1>Error</h1>')


def view_teacher(request,file_id):
    r = Result.objects.get(pk=file_id)
    return render(request,"teacher.html",{'file':r.tfile.name,'id':file_id})


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        print(request.FILES)
        print(request.POST)
        computer = request.POST["computer"]
        thread = request.POST["thread"]
        time = request.POST["time"]
        print(computer,thread)
        #save files in model...
        r = Result()
        c = Computer.objects.get(name=computer)
        t = Thread.objects.get(computer=c,name=thread) 
        f = Assignment.objects.get(thread=t)
        r.fetfile = f.fetfile
        r.rfile = request.FILES['fet_file']
        r.tfile = request.FILES['teachers_file']
        r.time = time
        r.save()
        return JsonResponse({'status':'ok'})

@login_required(login_url='loginForm')    
def AssignmentFormView(request):
    
    if request.method == 'POST':
        formAssignement = AssignementForm(request.POST)
        formFile = FileForm(request.POST, request.FILES)
        if 'files' in request.POST:
            assignements = request.POST.getlist('assignements')
            for formAssignement in assignements:
                file = File.objects.get(pk=request.POST['files'])
                assignement = Assignment.objects.get(pk=formAssignement)
                assignement.fetfile = file
                assignement.save()
        if formFile.is_valid():
            f = formFile.save()
                
    else:
        formAssignement = AssignementForm()
        formFile = FileForm()
        
    return render(request,'assignementform.html',{'formAssignement':formAssignement,'formFile':formFile})



def logUserIn(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            print("User is valid, active and authenticated")

        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def logUserOut(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def loginForm(request):
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')
