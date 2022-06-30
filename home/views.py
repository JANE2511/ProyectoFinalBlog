from pickle import GET
from django.shortcuts import render , redirect

# Create your views here.

from .form import *
from django.contrib.auth import logout



def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs' : BlogModel.objects.all()}
    return render(request , 'home.html' , context)

def login_view(request):
    return render(request , 'login.html')

def blog_detail(request , slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request , 'blog_detail.html' , context)


def see_blog(request):
    context = {}
    
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    except Exception as e: 
        print(e)
    
    print(context)
    return render(request , 'see_blog.html' ,context)


def add_blog(request):
    context = {'form' : BlogForm}
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
                        
        if form.is_valid():
            print(form.cleaned_data)              
            blog_obj = BlogModel(
                user = request.user, 
                **form.cleaned_data
            )
            blog_obj.save()
            return redirect('blog_detail', slug=blog_obj.slug)
        else:
           form = BlogForm(request.POST, request.FILES)
           context['form']=form   
    return render(request , 'add_blog.html' , context)


def blog_update(request , slug):
    context = {}
    try:
        
        
        blog_obj = BlogModel.objects.get(slug = slug)
       
        
        if blog_obj.user != request.user:
            return redirect('/')
        if request.method == 'GET':
            initial_dict = {'content': blog_obj.content}
            form = BlogForm(initial = initial_dict, instance=blog_obj)
            context['blog_obj'] = blog_obj
            context['form'] = form
            return render(request , 'update_blog.html' , context)

        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog_obj)
                        
            if form.is_valid():
                form.save()     
                return redirect('blog_detail', slug=blog_obj.slug)         
      

    except Exception as e :
        print(e)

    return render(request , 'update_blog.html' , context)

def blog_delete(request , id):
    try:
        blog_obj = BlogModel.objects.get(id = id)
        
        if blog_obj.user == request.user:
            blog_obj.delete()
        
    except Exception as e :
        print(e)

    return redirect('/see-blog/')


def  register_view(request):
    return render(request , 'register.html')



def verify(request,token):
    try:
        profile_obj = Profile.objects.filter(token = token).first()
        
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e : 
        print(e)
    
    return redirect('/')