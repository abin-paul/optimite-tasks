from django.shortcuts import render, redirect

from library.models import User
from library.api.serializers.user import UserSerializer
from library.forms import UserForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([AllowAny,])
def get_all_users(request):
    output = {}
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
    except:
        output['status'] = 'failed'
        output['status_text'] = 'Failed to fetch the users'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    output['users'] = serializer.data
    output['status'] = 'success'
    output['status_text'] = "Successfully fetched all the users"
    return Response(output, status=status.HTTP_200_OK)

def get_all_user_landing(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    print(users, serializer.data)
    form = UserForm()
    if users.exists():
        context = {
            "user_form": form,
            "users": serializer.data,
            "status": "success",
            "status_text": "Successfully fetched all the users"
        }
        return render(request, 'library/users.html', context)
    else:
        context = {
            "user_form": form,
            "status": "failed",
            "status_text": "Failed to fetch the users"
        }
        return render(request, 'library/users.html', context)
    
def create_user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        context = {
            "status": "success",
            "status_text": "Successfully created the user"
        }

        return redirect('get_users_landing')

def view_or_update_user(request, pk):
    user = User.objects.get(pk=pk)
    users = User.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('get_users_landing')
    else:
        form = UserForm(instance=user)

    context = {
        "status": "success",
        "status_text": "Successfully viewed the user",
        'users': users, 
        'user_update_form': form
    }
    return render(request, 'library/users.html', context)

def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('get_users_landing')
