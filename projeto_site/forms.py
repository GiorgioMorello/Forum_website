from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, TextAreaField
from wtforms.validators import DataRequired, length, Email, EqualTo
from projeto_site.models import Usuario
from flask_wtf.file import FileField, FileAllowed

class FormCriar(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Crie uma Senha", validators=[DataRequired(), length(6, 40)])
    confirmar_senha = PasswordField("Confirme sua Senha", validators=[DataRequired(), EqualTo('password')])
    botao_sub = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este e-mail já está em uso')



class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), length(6, 40)])
    botao_sub = SubmitField('Fazer Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profissao = StringField('Sua Profissão', validators=[DataRequired()])
    botao_editar = SubmitField('Confirmar Edição')
    foto_perfil = FileField('Atualizar Foto de Perfil',validators=[FileAllowed(['jpg', 'png'])], )
    curso_cc = BooleanField("Ciência da Computação")
    curso_mat = BooleanField("Matematica")
    curso_ec = BooleanField("Engenharia da Computação")
    curso_si = BooleanField("Sistemas de Informação")
    curso_mc = BooleanField("Matemática Computacional")
    curso_ads = BooleanField("Análise e Desenvolvimento de Sistemas")
    curso_rc = BooleanField("Redes de Computadores")
    curso_em = BooleanField("Engenharia Mecânica")



class FormPost(FlaskForm):
    titulo = StringField('Escreva um Título', validators=[DataRequired(), length(2, 110)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    botao_pub = SubmitField('Publicar Post')
    imagem_post = FileField('Adicionar uma Imagem',validators=[FileAllowed(['jpg', 'png'])])


class FormEditarPost(FlaskForm):
    titulo = StringField('Escreva um Título', validators=[DataRequired(), length(2, 110)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    botao_att = SubmitField('Atualizar Post')
    img_edit = FileField('Adicionar uma Imagem', validators=[FileAllowed(['jpg', 'png'])])
