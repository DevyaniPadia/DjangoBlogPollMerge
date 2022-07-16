from django import forms
from .models import Post, Comment, User
from django.contrib.auth.forms import UserCreationForm



choice = [('coding', 'coding'), ('sports', 'sports')]

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text', 'slug','category','tag','thumbnailimage','featureimage')
         
        # widgets = {
        #    'category': forms.Select(choices=choice, 
        #     attrs={'class': 'form-control'}),
		# 	}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class UpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email','city','state','country','mobile_no','profile_img')    
 

class LogoutForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password')    

class NewUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','city','state','country','mobile_no')

