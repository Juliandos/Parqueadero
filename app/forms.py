from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Usuario, Rol
from wtforms.validators import Regexp


def documento_unico(form, field):
    if Usuario.query.filter_by(documento=field.data).first():
        raise ValidationError('Este documento ya está registrado')

def email_unico(form, field):
    if Usuario.query.filter_by(email=field.data.lower()).first():
        raise ValidationError('Este email ya está registrado')

class UsuarioForm(FlaskForm):
    # Campo Documento
    documento = StringField('Documento de Identidad', 
        validators=[
            DataRequired('El documento es obligatorio'),
            documento_unico
        ],
        render_kw={"placeholder": "Número de documento sin espacios"}
    )
    
    # Campos de Nombre y Apellidos
    nombres = StringField('Nombres',
        validators=[
            DataRequired('Los nombres son obligatorios'),
            Length(max=32, message='Máximo 32 caracteres')
        ]
    )
    apellidos = StringField('Apellidos',
        validators=[
            DataRequired('Los apellidos son obligatorios'),
            Length(max=32, message='Máximo 32 caracteres')
        ]
    )

    # Campo Teléfono con validación de formato
    telefono = StringField('Teléfono',
        validators=[
            DataRequired('El teléfono es obligatorio'),
            Length(max=16, message='Máximo 16 caracteres'),
            Regexp(r'^\+?[0-9]+$', message='Formato de teléfono inválido')
        ],
        render_kw={"placeholder": "+57 300 1234567"}
    )

    # Campo Email con validación de formato y unicidad
    email = StringField('Email',
        validators=[
            DataRequired('El email es obligatorio'),
            Email('Formato de email inválido'),
            Length(max=64, message='Máximo 64 caracteres'),
            email_unico
        ],
        render_kw={"placeholder": "ejemplo@dominio.com"}
    )

    # Campos de Ubicación
    ciudad = StringField('Ciudad',
        validators=[
            DataRequired('La ciudad es obligatoria'),
            Length(max=64, message='Máximo 64 caracteres')
        ]
    )
    direccion = StringField('Dirección',
        validators=[
            DataRequired('La dirección es obligatoria'),
            Length(max=255, message='Máximo 255 caracteres')
        ]
    )

    # Selector de Rol
    rol_id = SelectField('Tipo de Usuario',
        coerce=int,
        # validators=[DataRequired('Selecciona un tipo de usuario')],
        render_kw={"class": "form-select"}
    )

    submit = SubmitField('Guardar Cambios')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        # Cargar opciones de roles desde la base de datos
        self.rol_id.choices = [(r.id, r.nombre) for r in Rol.query.order_by(Rol.nombre).all()]