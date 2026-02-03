from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.ambientes_service import AmbientesService
import uuid,os
from werkzeug.utils import secure_filename


# Cria o Blueprint para as rotas de ambientes
ambientes_bp = Blueprint("ambientes", __name__)

@ambientes_bp.route('/ambientes')
@jwt_required()
def ambientes():
    """
    Rota para exibir a página de listagem de ambientes.
    
    """
    # Obtém os dados completos do JWT 
    logado = get_jwt()
    # Obtém o ID do usuário logado a partir do token JWT
    id_logado = get_jwt_identity()
    # Busca todos os usuários cadastrados no sistema
    usuarios = UsuarioService.listar()
    # Busca todos os ambientes cadastrados
    ambientes = AmbientesService.listar()
   
    # Renderiza o template de ambientes passando todos os dados necessários
    return render_template('ambientes.html',ambientes=ambientes,id_logado=id_logado,logado=logado,usuarios=usuarios)


@ambientes_bp.route('/ambientes/<id>', methods=['POST'])
@jwt_required()
def atualizar_ambiente(id):
    """
    Rota para atualizar um ambiente existente.
    
    """

    try:
       
        # Obtém os dados completos do JWT 
        logado = get_jwt()

        # Verifica se o usuário tem permissão de administrador
        if  logado["role"] != "admin":
            # Retorna erro 403  se não for admin
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Obtém o caminho da imagem atual (caso não seja enviada nova imagem)
        image_path = request.form.get("image_atual")

        # Se uma nova imagem foi enviada
        if imagem:
            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho onde a imagem será salva
            caminho = f"static/imgs/{filename}"
            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/{caminho}"

        # Monta o dicionário com todos os dados do ambiente a serem atualizados
        dados = {
            "id": id,  # ID do ambiente vindo da URL
            "name": request.form.get("name"),  # Nome do ambiente
            "type": request.form.get("type") or "sala",  # Tipo (padrão: "sala")
            "capacidade": request.form.get("capacidade"),  # Capacidade máxima
            "status": request.form.get("status") or "Disponivel",  # Status (padrão: "Disponivel")
            "descricao": request.form.get("descricao"),  # Descrição do ambiente
            "localizacao": request.form.get("localizacao"),  # Localização física
            "area": request.form.get("area"),  # Área do ambiente
            "image": image_path,  # Caminho da imagem (nova ou atual)
            "recursos": request.form.getlist("recursos[]")  # Lista de recursos do ambiente
        }

        # Atualiza o ambiente no banco de dados
        AmbientesService.atualizar_ambiente(dados)
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Ambiente atualizado com sucesso"}), 200
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro ao Atualizar Ambiente"}), 500

@ambientes_bp.route("/novo-ambiente", methods=['POST'])
@jwt_required()
def novo_ambiente():
    """
    Rota para cadastrar um novo ambiente no sistema.
    
    """
    try:
        # Obtém os dados completos do JWT 
        logado = get_jwt()

        # Verifica se o usuário tem permissão de administrador
        if  logado["role"] != "admin":
            # Retorna erro 403 (Forbidden) se não for admin
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Inicializa caminho da imagem como None (caso não seja enviada)
        image_path = None

        # Se uma imagem foi enviada e tem nome de arquivo válido
        if imagem and imagem.filename != "":
            # Cria o diretório para salvar imagens se não existir
            os.makedirs("static/imgs", exist_ok=True)

            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho completo onde a imagem será salva
            caminho = os.path.join("static/imgs", filename)

            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/static/imgs/{filename}"

        # Monta o dicionário com todos os dados do novo ambiente
        dados = {
            "name": request.form.get("name"),  # Nome do ambiente
            "type": request.form.get("type"),  # Tipo do ambiente
            "capacidade" : int(request.form.get("capacidade")),  # Capacidade convertida para inteiro
            "status": request.form.get("status", "Disponivel"),  # Status (padrão: "Disponivel")
            "descricao": request.form.get("descricao"),  # Descrição do ambiente
            "localizacao": request.form.get("localizacao"),  # Localização física
            "area": request.form.get("area"),  # Área do ambiente
            "image": image_path,  # Caminho da imagem (ou None se não enviada)
            "recursos": request.form.getlist("recursos[]")  # LISTA de recursos do ambiente
        }

        # Insere o novo ambiente no banco de dados
        AmbientesService.inserir_ambiente(dados)

        # Retorna mensagem de sucesso com status 201 (Created)
        return jsonify({"mensagem": "Ambiente cadastrado com sucesso"}), 201
        
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro cadastrar Ambiente "}), 500

    


@ambientes_bp.route("/ambientes/<id>/", methods=["DELETE"])
@jwt_required()
def deletar_ambiente(id):
    """
    Rota para excluir um ambiente do sistema.
    
    Funcionalidade:
    - Requer autenticação JWT e permissão de administrador
    - Deleta o ambiente pelo ID informado na URL
    - Remove o ambiente e seus dados relacionados (recursos) do banco
    
    Args:
        id (str): ID do ambiente a ser excluído (da URL)
    
    Decorators:
        @jwt_required(): Exige token JWT válido para acessar a rota
    
    Returns:
        tuple: JSON com mensagem de sucesso (200) ou erro (400, 403, 500)
    """

    try:
        # Obtém os dados completos do JWT (incluindo role/função do usuário)
        logado = get_jwt()

        # Verifica se o usuário tem permissão de administrador
        if  logado["role"] != "admin":
            # Retorna erro 403 (Forbidden) se não for admin
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Deleta o ambiente do banco de dados pelo ID
        AmbientesService.deletar_ambiente(id)
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({'mensagem': 'Ambiente excluído com sucesso'}), 200

    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        print(e)
        return jsonify({"erro": "Erro ao deletar ambiente "}), 500