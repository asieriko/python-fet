from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import os
from django.utils import timezone

from .teachereval import evaluate

from .models import Computer,Thread,Assignment,File,Result
from .forms import AssignementForm, FileForm

def status_page(request, computer, thread):
    comp = Computer.objects.get(name=computer)
    thr = Thread.objects.get(computer=comp,name=thread)
    thr.lastping = timezone.now()
    thr.save()
    if thr.active:
        assig = Assignment.objects.filter(thread=thr)
        return JsonResponse({'status':'active','file_id':str(assig[0].fetfile.id),'file_name':str(assig[0].fetfile.name),'file':str(assig[0].fetfile.fetfile)})
    else:
        return JsonResponse({'status':'Stop'})

def return_file(request,file_id):
    file = File.objects.get(pk=file_id)
    file_path = file.fetfile.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return "Error"

def show_results(request):
    rs = Result.objects.all()
    return render(request,"results.html",{'results':rs})


def show_threads(request):
    threads = Thread.objects.all()
    return render(request,"threads.html",{'threads':threads})

def return_result_fet(request,file_id):
    r = Result.objects.get(pk=file_id)
    file_path = r.rfile.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Access-Control-Allow-Origin'] = '*'
            return response
    print("Error")
    return HttpResponse('<h1>Error</h1>')

def return_result_teacher(request,file_id):
    r = Result.objects.get(pk=file_id)
    file_path = r.tfile.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Access-Control-Allow-Origin'] = '*'
            return response
    return HttpResponse('<h1>Error</h1>')


def view_teacher(request,file_id):
    r = Result.objects.get(pk=file_id)
    return render(request,"teacher.html",{'file':r.tfile.name,'id':file_id})


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        computerName = request.POST["computer"]
        threadName = request.POST["thread"]
        time = request.POST["time"]
        #save files in model...
        result = Result()
        computer = Computer.objects.get(name=computerName)
        thread = Thread.objects.get(computer=computer,name=threadName)
        thread.lastping = timezone.now()
        thread.save()
        assignment = Assignment.objects.get(thread=thread)
        result.fetfile = assignment.fetfile
        result.rfile = request.FILES['fet_file']
        result.tfile = request.FILES['teachers_file']
        result.time = time
        result.computer = computer
        result.assignment = assignment
        
        tdic, sumdic, sumtotal = evaluate(result.tfile)
        s = "Resumen\n"
        for k in sorted(sumdic.keys()):
            s += str(k)+" días completos: "+str(sumdic[k])+" docentes\n"
        result.stats = s
        result.save()
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
                assignment = Assignment.objects.get(pk=formAssignement)
                assignment.fetfile = file
                assignment.save()
        if formFile.is_valid():
            f = formFile.save()
    
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
