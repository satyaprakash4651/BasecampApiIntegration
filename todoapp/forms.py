from django import forms


class TodoForm(forms.Form):
    title = forms.CharField(max_length=50)
    audio_file = forms.FileField()

    def clean_audio_file(self):
        audio_file = self.cleaned_data['audio_file']

        allowed_content_types = ['audio/x-m4a']
        if audio_file.content_type not in allowed_content_types:
            raise forms.ValidationError('You must upload an audio file of type {}'.format(', '.join(allowed_content_types)))

        return audio_file
