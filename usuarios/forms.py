from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese una contraseña segura'}),
        help_text="Requerido para el inicio de sesión."
    )
    confirmar_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita la contraseña'}),
        help_text="Vuelva a escribir la contraseña para verificarla."
    )

    class Meta:
        model = Usuario
        fields = [
            'tipo_documento',
            'documento',
            'first_name',
            'last_name',
            'email',
            'fecha_nacimiento',
            'password',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Ej: 1049641572'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['email'].help_text = "Se utilizará para iniciar sesión en el sistema."
        self.fields['documento'].help_text = "Se asignará automáticamente como usuario de la cuenta."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if password and confirmar_password and password != confirmar_password:
            self.add_error('confirmar_password', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # El número de documento es el usuario
        usuario.username = str(usuario.documento)
        # Por defecto el rol es TURISTA
        usuario.rol = 'TURISTA'
        password = self.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        if commit:
            usuario.save()
        return usuario


class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'tipo_documento',
            'documento',
            'first_name',
            'last_name',
            'email',
            'fecha_nacimiento',
            'rol',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Ej: 1049641572'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['email'].help_text = "Se utilizará para iniciar sesión en el sistema."
        self.fields['documento'].disabled = True
        self.fields['documento'].help_text = "El número de documento no se puede modificar."
        self.fields['tipo_documento'].disabled = True
        self.fields['tipo_documento'].help_text = "El tipo de documento no se puede modificar."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = Usuario.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado con otro usuario.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Mantener el usuario sincronizado con el documento
        usuario.username = str(usuario.documento)
        if commit:
            usuario.save()
        return usuario
