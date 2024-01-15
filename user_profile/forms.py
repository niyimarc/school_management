from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

class RegForm(UserCreationForm):
    class Meta():
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(user, *args, **kwargs)
        if user:
            self.user = user
    
    def save(self, commit=True):
        if self.user:
            # Update the user password here
            self.user.set_password(self.cleaned_data['new_password1'])
            if commit:
                self.user.save()
            return self.user
        else:
            raise ValueError("No user object provided to the form.")

