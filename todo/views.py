from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Todo

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('/login')
    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todo')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login')

# Main Todo view
@login_required
def todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            Todo.objects.create(title=task, user=request.user)
        return redirect('/todo')

    todos = Todo.objects.filter(user=request.user).order_by('-date')
    total = todos.count()
    completed = todos.filter(completed=True).count()
    context = {'todos': todos, 'total': total, 'completed': completed}
    return render(request, 'todo.html', context)

# Delete task
@login_required
def delete_task(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)
    task.delete()
    return redirect('/todo')

# Mark as done
@login_required
def toggle_complete(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('/todo')

# Edit task
@login_required
def edit_task(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        if new_title:
            task.title = new_title
            task.save()
        return redirect('/todo')
    return render(request, 'edit.html', {'task': task})
