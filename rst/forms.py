from django import forms


class UploadRstFileForm(forms.Form):
    file = forms.FileField(
        label="Selecione o arquivo",
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-input',
            'accept': '.rs3,.xml'
        }),
        required=True,
        allow_empty_file=False,
    )
