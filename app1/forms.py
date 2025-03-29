from django import forms
import datetime
class admin(forms.Form):
    adminid = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
class user(forms.Form):
    userid = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerfrm(forms.Form):
    User_Id=forms.IntegerField()
    User_Name=forms.CharField()
    def clean_UserName(self):
        lc = 0
        uc = 0
        dc = 0
        sc = 0

        username= self.cleaned_data['User_Name']

        for i in username:
            if (i.islower()):
                    lc += 1
            elif (i.isupper()):
                    uc += 1
            elif (i.isdigit()):
                    dc += 1
            else:
                sc += 1
        if lc < 1 or uc < 1 or dc > 1 or sc == 1:
            raise forms.ValidationError('user name dont contain any digit and any symbol')
        return username

    Password=forms.CharField(widget=forms.PasswordInput)
    confrm_pwd=forms.CharField(widget=forms.PasswordInput)
    Choices=[
         ('Male','Male'),
        ('Female','Female'),
        ("Others",'Others')
    ]
    Gender=forms.ChoiceField(choices=Choices,widget=forms.RadioSelect)
    Phone_Number=forms.IntegerField()

    Email=forms.EmailField()
    def clean_Password(self):
        lc=0
        uc=0
        dc=0
        sc=0

        pwd = self.cleaned_data['Password']
        if len(pwd)>8 and len(pwd)<16:
            for i in pwd:
                if(i.islower()):
                    lc+=1
                elif(i.isupper()):
                    uc+=1
                elif(i.isdigit()):
                    dc+=1
                else:
                    sc+=1
        if lc<1 or uc<1 or dc<1 or sc<1:
            raise forms.ValidationError('password must be one upper case one lower and one digit one symbol')
        return pwd


class search(forms.Form):
    medicine_id=forms.IntegerField()
    meidcine_name=forms.CharField(max_length=30)
class update(forms.Form):
    uid=forms.IntegerField()
    Date=forms.DateField()
class adminreg1(forms.Form):
    Admin_Id=forms.IntegerField()
    Admin_Name=forms.CharField()
    Admin_password=forms.CharField(widget=forms.PasswordInput)

    def clean_Password(self):
        lc = 0
        uc = 0
        dc = 0
        sc = 0

        pwd = self.cleaned_data['Admin_password']
        if len(pwd) > 8 and len(pwd) < 16:
            for i in pwd:
                if (i.islower()):
                    lc += 1
                elif (i.isupper()):
                    uc += 1
                elif (i.isdigit()):
                    dc += 1
                else:
                    sc += 1
        if lc < 1 or uc < 1 or dc < 1 or sc < 1:
            raise forms.ValidationError('password must be one upper case one lower and one digit one symbol')
        return pwd



class update(forms.Form):
    User_Id=forms.IntegerField()
    Date = forms.DateField(initial=datetime.date.today)