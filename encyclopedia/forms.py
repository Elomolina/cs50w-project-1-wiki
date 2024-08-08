from django import forms

class createForm(forms.Form):
    title = forms.CharField(label = "Title", required=True, error_messages={
        'required': "This field cannot be empty"
    })
    
    content = forms.CharField(widget=forms.Textarea(
        attrs= {
            'placeholder': 'Enter content here'
        }
    ), label="Enter content", required=True, error_messages={
        'required': "This field cannot be empty"
    })

class editMarkdown(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'edit'
        }
    ), required=True, error_messages={
        'required': 'This field cannot be empty'
    })