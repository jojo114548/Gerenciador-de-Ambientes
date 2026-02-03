
from flask import Blueprint, request, jsonify

from service.usuario_service import UsuarioService

from flask_jwt_extended import (get_jwt_identity, jwt_required, get_jwt)

import uuid, os

from werkzeug.utils import secure_filename


usuario_bp = Blueprint("usuario", __name__)



@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
@jwt_required()  
def editar_usuario(id):
    """
    Edita os dados de um usuário existente.
    
    """
    try:
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()
        
        # Obtém todos os dados (claims) do token JWT, incluindo role
        logado = get_jwt()

    
        # Permite edição apenas se for o próprio usuário OU se for admin
        if id != id_logado and logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
      
        # Obtém o arquivo de imagem enviado no formulário
        imagem = request.files.get("image")
        image_path = None  # Inicializa como None (sem imagem)

        # Se uma imagem foi enviada e tem nome de arquivo
        if imagem and imagem.filename != "":
            # Cria o diretório para armazenar imagens (se não existir)
            os.makedirs("static/imgs", exist_ok=True)
            
            # Gera um nome único para o arquivo usando UUID + nome original seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            
            # Define o caminho completo onde a imagem será salva
            caminho = os.path.join("static/imgs", filename)
            
            # Salva o arquivo fisicamente no servidor
            imagem.save(caminho)
            
            # Define o caminho relativo da imagem para ser armazenado no banco
            image_path = f"/static/imgs/{filename}"


        # Obtém os campos obrigatórios do formulário
        name = request.form.get("name")
        email = request.form.get("email")

        #  Verifica se os campos obrigatórios foram preenchidos
        if not name or not email:
            return jsonify({"erro": "Nome e email são obrigatórios"}), 400

        # Monta um dicionário com todos os dados do usuário
        dados = {
            "name": name,
            "email": email,
            "cpf": request.form.get("cpf"),
            "rg": request.form.get("rg"),
            "data_nascimento": request.form.get("data_nascimento"),
            "telefone": request.form.get("telefone"),
            "endereco": request.form.get("endereco"),
            "departamento": request.form.get("departamento"),
            "funcao": request.form.get("funcao"),
            "role": request.form.get("role"),
            "status": request.form.get("status"),
            "image": image_path  # Caminho da imagem (ou None se não foi enviada)
        }

        # Log para debug: imprime os arquivos recebidos
        print(request.files)

        # Chama o serviço para atualizar o usuário no banco de dados
        UsuarioService.atualizar(id, dados)

        # Retorna resposta de sucesso
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@usuario_bp.route("/usuarios/<id>/senha", methods=["PUT"])
@jwt_required()  
def alterar_senha(id):
    """
    Altera a senha de um usuário.

    """
    try:
        # Obtém o ID do usuário logado
        id_logado = get_jwt_identity()
        
        # Obtém todos os dados do token JWT
        logado = get_jwt()
        
        # Obtém os dados JSON enviados no corpo da requisição
        dados = request.get_json()

     
        # Permite alteração apenas se for o próprio usuário OU se for admin
        if id != id_logado and logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403

        # Extrai senha atual e nova senha do JSON
        senha_atual = dados.get("senha_atual")
        senha_nova = dados.get("senha_nova")
 

        
        # O usuário está alterando sua própria senha
        if id == id_logado:
            # Validação: Usuário próprio DEVE informar a senha atual
            if not senha_atual:
                return jsonify({"erro": "Senha atual é obrigatória"}), 400
            
            # Chama o serviço para alterar senha (valida senha atual internamente)
            UsuarioService.alterar_senha(id, senha_atual, senha_nova)
            
            return jsonify({"mensagem": "Senha alterada com sucesso"}), 200
        
        #  Admin está resetando a senha de outro usuário
        else:
            # Admin pode resetar sem precisar da senha atual
            # A senha é resetada para o padrão: "User" + últimos 4 dígitos do CPF
            UsuarioService.resetar_senha_padrao(id)

            return jsonify({
                "mensagem": "Senha resetada para o padrão (User + últimos 4 dígitos do CPF)"
            }), 200
    
    except ValueError as e:
        # Captura erros de validação (ex: senha atual incorreta)
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(e)
        return jsonify({"erro": "Erro ao alterar senha"}), 500



@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
@jwt_required()  # Requer autenticação JWT válida
def deletar_usuario(id):
    """
    Remove um usuário do sistema.
    
    """
    try:
        # Obtém o ID do usuário logado
        id_logado = get_jwt_identity()
        
        # Obtém todos os dados do token JWT
        logado = get_jwt()

       
        # Permite deleção apenas se for o próprio usuário OU se for admin
        if id != id_logado and logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Chama o serviço para deletar o usuário do banco de dados
        UsuarioService.deletar(id)

       
        # Se o usuário deletou sua própria conta, avisa que será deslogado
        if id == id_logado:
            return jsonify({
                "mensagem": "Conta excluída com sucesso. Você será deslogado."
            }), 200
        
        # Se admin deletou outro usuário
        return jsonify({"mensagem": "Usuário removido"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:

        return jsonify({"erro": str(e)}), 500



@usuario_bp.route("/novo-usuario", methods=["POST"])
@jwt_required()  
def novo_usuario():
    """
    Cadastra um novo usuário no sistema.
    
    """
    try:
        # Obtém o ID do usuário logado
        id_logado = get_jwt_identity()
        
        # Obtém todos os dados do token JWT
        logado = get_jwt()


        # APENAS administradores podem cadastrar novos usuários
        if logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
  
        # Obtém o arquivo de imagem enviado no formulário
        imagem = request.files.get("image")
        image_path = None  # Inicializa como None

        # Se uma imagem foi enviada
        if imagem and imagem.filename != "":
            # Cria o diretório para armazenar imagens
            os.makedirs("static/imgs", exist_ok=True)
            
            # Gera nome único: UUID + nome original sanitizado
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            
            # Define caminho completo para salvar
            caminho = os.path.join("static/imgs", filename)
            
            # Salva o arquivo no servidor
            imagem.save(caminho)
            
            # Define caminho relativo para o banco
            image_path = f"/static/imgs/{filename}"


        dados = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "cpf": request.form.get("cpf"),
            "rg": request.form.get("rg"),
            "data_nascimento": request.form.get("data_nascimento"),
            "telefone": request.form.get("telefone"),
            "endereco": request.form.get("endereco"),
            "departamento": request.form.get("departamento"),
            "funcao": request.form.get("funcao"),
            "role": request.form.get("role"),  
            "status": request.form.get("status"), 
            "senha": request.form.get("senha"),
        }
        
        # Adiciona o caminho da imagem ao dicionário
        dados["image"] = image_path

        # ===== VALIDAÇÃO 1: CPF =====
        if dados["cpf"]:
            # Converte para inteiro (valida se é numérico)
            int(dados["cpf"])
            
            # Verifica se tem exatamente 11 dígitos
            if len(dados["cpf"]) != 11:
                return "CPF inválido. Deve conter 11 dígitos numéricos.", 400
        
        # ===== VALIDAÇÃO 2: EMAIL =====
        if dados["email"]:
            email = dados["email"]
            
            # Validação complexa de email:
            # 1. Deve conter "@"
            # 2. "@" não pode estar no início ou fim
            # 3. Deve ter "." depois do "@"
            # 4. Deve terminar com um dos provedores permitidos
            if (
                "@" not in email or
                email.index("@") <= 0 or
                email.index("@") >= len(email) - 1 or
                email.rfind(".") <= email.index("@") + 1 or
                not (
                    email.endswith("@gmail.com") or
                    email.endswith("@hotmail.com") or
                    email.endswith("@yahoo.com") or
                    email.endswith("@outlook.com")
                )
            ):
                return "Email inválido.", 400
        
        # ===== VALIDAÇÃO 3: SENHA =====
        if dados["senha"]:
            #  Tamanho mínimo de 8 caracteres
            if len(dados["senha"]) < 8:
                return "Senha muito curta. Deve conter no minimo 8 caracteres ", 400
            
            # Deve conter pelo menos um caractere especial
            elif not (set(dados["senha"]) & set("!@#$%^&*()-_=+[{]};:'\",<.>/?\\|")):
                return "Senha inválida. Deve conter ao menos um caractere especial (@ ou #).", 400
            
            # Deve conter pelo menos uma letra (maiúscula ou minúscula)
            elif not (set(dados["senha"]) & set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")):
                return "Senha inválida. Deve conter ao menos uma letra.", 400
            
            #  Deve conter pelo menos um número
            elif not (set(dados["senha"]) & set("0123456789")):
                return "Senha inválida. Deve conter ao menos um numero.", 400

       
        # cadastrar o usuário no banco
        resultado = UsuarioService.cadastrar(dados)
        
        # Retorna sucesso com status 201 (Created)
        return jsonify({
            "mensagem": "Usuário cadastrado com sucesso",
            "usuario": resultado
        }), 201
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:

        return jsonify({"erro": str(e)}), 500