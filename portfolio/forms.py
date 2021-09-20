from django import forms
from django.core.mail import EmailMessage

# from .models import Diary
from .models import Task, Members


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'お名前をここに入力してください。',
    }))

    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'メールアドレスをここに入力してください。',
    }))

    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'タイトルをここに入力してください。',
    }))

    message = forms.CharField(label='メッセージ', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'メッセージをここに入力してください。',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['class'] = 'form-control col-11'
        # self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'
        #
        # self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        # self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'
        #
        # self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        # self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'
        #
        # self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        # self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)

        message.send()


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('content', 'date', 'time', 'minutes', 'memo')

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        start = kwargs['initial']['start']
        end = kwargs['initial']['end']
        self.fields['time'] = forms.ChoiceField(label='時間', choices=[(v, v) for v in range(start, end + 1)])

    content = forms.CharField(label='タスク名', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ex) 読書'
    }))

    date = forms.DateField(label='日付', widget=forms.DateInput(attrs={'type': 'date'}))
    minutes = forms.ChoiceField(label='分', choices=[('0', '0'), ('30', '30')])

    def save(self, commit=True):
        task_create_form = super(TaskCreateForm, self).save(False)
        date_object = self.cleaned_data['date']
        task_create_form.year = date_object.year
        task_create_form.month = date_object.month
        task_create_form.day = date_object.day
        if commit:
            task_create_form.save()
        return task_create_form


class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ('start', 'end', 'name')

    start = forms.ChoiceField(label='開始時間', choices=[('{:02}:00:00'.format(v), v) for v in range(0, 24)])
    end = forms.ChoiceField(label='終了時間', choices=[('{:02}:00:00'.format(v), v) for v in range(0, 24)])
    name = forms.CharField(label='ユーザー名', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
#
# class DiaryCreateForm(forms.ModelForm):
#     class Meta:
#         model = Diary
#         fields = ('title', 'content', 'photo1', 'photo2', 'photo3',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
