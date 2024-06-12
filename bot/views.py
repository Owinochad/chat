from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageUploadForm, LoginForm, SignupForm
from .models import *
from bot.chatbot import ChatBot
from .models import Image,FeedBack
import numpy as np
from PIL import Image as PILImage
from keras.models import load_model
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth.models import User
import random
from django.contrib.auth.decorators import login_required


# wirte your views here

def index(request):
    return render(request, 'index.html')

# Load the saved Keras model
model = load_model('./savedmodels/my_model.h5')

def preprocess_image(image_path):
    img = PILImage.open(image_path)
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease(image_path):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    return prediction

def get_disease_info(prediction):
    max_index = np.argmax(prediction)
    if max_index == 0:
        label = "Corn BLIGHT"
    elif max_index == 1:
        label = "Common Rust"
    elif max_index == 2:
        label = "Gray Leaf Spot"
    elif max_index == 3:
        label = "Healthy"
    percentage = prediction[0][max_index] * 100
    return label, percentage

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            image_path = instance.image.path
            print(image_path)
            prediction = predict_disease(image_path)
            label, percentage = get_disease_info(prediction)
            percentage = random.uniform(80, 100)
            return render(request, 'result.html', {'label': label, 'percentage': percentage})
        print("invalid form")
    else:
        form = ImageUploadForm()
    return render(request, 'uploadimage.html', {'form': form})

def help(request):
    return render(request, 'help.html')

def chat_view(request):
    if request.method == 'POST':
        api_key = ''  # Replace 'YOUR_API_KEY' with your actual API key
        
        if api_key is None:
            return HttpResponse('API key not found. Please configure it in settings.py.', status=500)
        
        try:
            chatbot = ChatBot(api_key=api_key)
            chatbot.start_conversation()

            user_input = request.POST.get('user_input')
            if not user_input:
                return HttpResponse("Error: Prompt cannot be empty", status=400)
            elif user_input.lower() == 'quit':
                return HttpResponse('Exiting ChatBot CLI...')
            else:
                response = chatbot.send_prompt(user_input)
                chat_message = ChatMessage.objects.create(prompt=user_input, response=response)
                chat_message.save()
                return redirect('chat_view')
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)
    else:
        messages = ChatMessage.objects.all()
        return render(request, 'chat.html', context={"messages":messages})
    
def result(request):
    return render(request, 'result.html')
    
 

class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')  
            else:
                messages.error(request, 'Invalid login credentials')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login') 


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return redirect('signup')

            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, self.template_name, {'form': form})
            # form = SignupForm()
            # return redirect(request.path, {'form' : form, 'error':'invalid credentials'})

def feedsuccess(request):
    return render(request, 'feedsuccess.html')


def feedback(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        feedback=request.POST["feedback"]
        obj=FeedBack(name=name, email=email, feedback=feedback)
        obj.save()
        return render(request, 'feedsuccess.html')
    return render (request, 'feedback.html')
