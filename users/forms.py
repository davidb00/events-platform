from events import forms
from users.models import Message, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','username','password1','password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'

            

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','username','location','img_url','short_intro',)
        labels = {'location':'Location (zip)'}

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'short_intro': forms.Textarea(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.NumberInput(attrs={'class':'form-control'}),

        }

class SignUpForm(UserCreationForm):
    #bootstrap widget formatting
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class MessageForm2(forms.Form):
    body = forms.CharField(widget=forms.TextInput(attrs={'size':50, 'maxlength':250}))

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        labels = {'body':''}
    def __init__(self, *args, **kwargs):
        super(MessageForm,self).__init__(*args,**kwargs)
        self.fields['body'].widget = forms.TextInput(attrs={'class':'form-control', 'maxlength':250})
        self.fields['body'].widget.attrs.update({'autofocus': 'autofocus'})

class CreateMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['recipient','body']
    def __init__(self, *args, **kwargs):
        super(CreateMessageForm,self).__init__(*args,**kwargs)
        self.fields['recipient'].widget.attrs.update({'class': 'btn btn-light dropdown-toggle',})
        self.fields['body'].widget = forms.Textarea(attrs={'class':'form-control', 'maxlength':250})

        
class UserLoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(UserLoginForm,self).__init__(*args,**kwargs)
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))

