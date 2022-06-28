import secrets
from projeto_site.forms import FormCriar, FormLogin, FormEditarPerfil, FormPost, FormEditarPost
from projeto_site import app, database, bcrypt
from flask import render_template, redirect, flash, url_for, request, abort
from projeto_site.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import os
from PIL import Image
from datetime import datetime






@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts, datetime=datetime)



@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('home'))

#@app.route('/contato')
#def contato():

    #return render_template('contact.html')



@app.route('/usuarios')
@login_required
def usuarios():
    lista_user = Usuario.query.all()
    return render_template('users.html', lista_user=lista_user)


@app.route('/login', methods=["POST", "GET"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form_login.password.data): # Se usuário existe e se a senha é igual a que esta no banco de dados
            login_user(usuario)
            flash("Login feito com sucesso", "alert-success")
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash("E-mail ou Senha Incorretos", "alert-danger")

    return render_template('login.html', form_login=form_login)


@app.route('/criar', methods=["POST", "GET"])
def create():
    form_criar = FormCriar()
    if form_criar.validate_on_submit():
        # Criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criar.password.data)
        
        # Criar o usuario
        usuario = Usuario(username=form_criar.username.data, email=form_criar.email.data, password=senha_cript)
        
        # Adicionar na sessão
        database.session.add(usuario)
        
        # Colocar no Banco de dados
        database.session.commit()
        flash("Conta Criada com sucesso", "alert-success")
        return redirect(url_for('home'))
    return render_template('create.html', form_criar=form_criar)



@app.route('/meu-perfil')
@login_required
def meu_perfil():
    foto_perfil = url_for(f'static', filename=f'foto_perfil/{current_user.foto_perfil}')


    return render_template('meu_perfil.html', foto_perfil=foto_perfil)


def salvar_imagem_post(imagem):
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + cod + extensao
    caminho_completo = os.path.join(app.root_path, 'static/imagem_post', nome_arquivo)

    tamanho = (300, 300)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route("/criar-post", methods=['POST', 'GET'])
@login_required
def criar():
    form_post = FormPost()
    if form_post.validate_on_submit():
        post = Post(titulo=form_post.titulo.data, corpo=form_post.corpo.data, autor=current_user)
        if form_post.imagem_post.data:
            nome_img = salvar_imagem_post(form_post.imagem_post.data)
            post.imagem = nome_img
        database.session.add(post)
        database.session.commit()
        flash('Post Publicado', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form_post=form_post)



def salvar_imagem(imagem):
    # Add o cod no nome da imagem
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + cod + extensao
    caminho_completo = os.path.join(app.root_path, 'static/foto_perfil', nome_arquivo)
    
    # Reduzir a imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a imagem
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_curso = [campo.label.text for campo in form if 'curso' in campo.name and campo.data]
    return ';'.join(lista_curso)


@app.route("/editar-perfil", methods=['POST', 'GET'])
@login_required
def editar_perfil():
    form_editar = FormEditarPerfil()
    if form_editar.validate_on_submit():
        current_user.username = form_editar.username.data
        current_user.email = form_editar.email.data
        current_user.profissao = form_editar.profissao.data
        if form_editar.foto_perfil.data:
            foto_antiga = current_user.foto_perfil
            if foto_antiga != 'default.jpg':
                arquivo = os.path.join(app.root_path, 'static/foto_perfil', foto_antiga)
                if os.path.isfile(arquivo):
                    os.remove(arquivo)
            nome_imagem = salvar_imagem(form_editar.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_editar)
        database.session.commit()
        flash('Perfil Atualizado', 'alert-success')
        return redirect(url_for('meu_perfil'))
    elif request.method == 'GET':
        form_editar.username.data = current_user.username
        form_editar.email.data = current_user.email
    foto_perfil = url_for(f'static', filename=f'foto_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html', form_editar=form_editar, foto_perfil=foto_perfil)



@app.route("/post/<post_id>", methods=['POST', 'GET'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editar_post = FormEditarPost()
        post = Post.query.get(post_id)
        if form_editar_post.validate_on_submit():
            post.titulo = form_editar_post.titulo.data
            post.corpo = form_editar_post.corpo.data
            if form_editar_post.img_edit.data:
                nome_img = salvar_imagem_post(form_editar_post.img_edit.data)
                post.imagem = nome_img
            database.session.commit()
            flash('Post Atualizado', 'alert-success')
            return redirect(url_for('home'))
    else:
        form_editar_post = None
    return render_template('post.html', post=post, datetime=datetime, form_editar_post=form_editar_post)


@app.route("/post/<post_id>/excluir", methods=['POST', 'GET'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post exlcuido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route("/post/<post_id>/excluir_imagem", methods=['POST', 'GET'])
@login_required
def excluir_img(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        post.imagem = None
        database.session.commit()
        flash('Imagem exlcuida', 'alert-danger')
        return redirect(url_for('exibir_post', post_id=post.id))


@app.route("/usuario/<id_user>")
@login_required
def exibir_usuario(id_user):
    usuario = Usuario.query.get(id_user)
    return render_template('exibir_user.html', usuario=usuario)

