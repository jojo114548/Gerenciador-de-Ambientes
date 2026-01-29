from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService
from flask_jwt_extended import (get_jwt_identity, jwt_required,get_jwt)
import uuid,os
from werkzeug.utils import secure_filename



usuario_bp = Blueprint("usuario", __name__)
    
@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
@jwt_required()
def editar_usuario(id):
    try:
        id_logado = get_jwt_identity()
        logado = get_jwt()

        if id != id_logado and logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        imagem = request.files.get("image")
        image_path = None

        if imagem and imagem.filename != "":
            os.makedirs("static/imgs", exist_ok=True)
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = os.path.join("static/imgs", filename)
            imagem.save(caminho)
            image_path = f"/static/imgs/{filename}"



        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return jsonify({"erro": "Nome e email são obrigatórios"}), 400

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
            "image":image_path
        }

        
        print(request.files)

        UsuarioService.atualizar(id, dados)

        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500

@usuario_bp.route("/usuarios/<id>/senha", methods=["PUT"])
@jwt_required()
def alterar_senha(id):
    try:
        id_logado = get_jwt_identity()
        logado = get_jwt()
        dados = request.get_json()

        if id != id_logado and logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403

       
        senha_atual = dados.get("senha_atual")
        senha_nova = dados.get("senha_nova")
 
        
        # Se o próprio usuário, exige senha atual
        if id == id_logado:
            if not senha_atual:
                return jsonify({"erro": "Senha atual é obrigatória"}), 400
            UsuarioService.alterar_senha(id, senha_atual, senha_nova)
            return jsonify({"mensagem": "Senha alterada com sucesso"}), 200
        else:
            # Admin pode resetar sem senha atual
            UsuarioService.resetar_senha_padrao(id)

            return jsonify({
            "mensagem": "Senha resetada para o padrão (User + últimos 4 dígitos do CPF)"
        }), 200

        
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500

@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):

    try:     
        id_logado = get_jwt_identity()
        logado = get_jwt()

        if id != id_logado and logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        UsuarioService.deletar(id)

        if id == id_logado:
         return jsonify({
            "mensagem": "Conta excluída com sucesso. Você será deslogado."
        }), 200
    
    
        return jsonify({"mensagem": "Usuário removido"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500


@usuario_bp.route("/novo-usuario", methods=["POST"])
@jwt_required()
def novo_usuario():
    try:
        id_logado = get_jwt_identity()
        logado = get_jwt()

        if  logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        

        imagem = request.files.get("image")
        image_path = None

        if imagem and imagem.filename != "":
            os.makedirs("static/imgs", exist_ok=True)
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = os.path.join("static/imgs", filename)
            imagem.save(caminho)
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
        dados["image"] = image_path

        if dados["cpf"]:
            int(dados["cpf"])
            if len(dados["cpf"])!=11 :
             return "CPF inválido. Deve conter 11 dígitos numéricos.", 400
        
        if dados["email"]:
            email = dados["email"]
     
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
            
        if dados["senha"]:
                if len(dados["senha"])<8:
                  return "Senha muito curta. Deve conter no minimo 8 caracteres ", 400
                elif not (set(dados["senha"]) & set("!@#$%^&*()-_=+[{]};:'\",<.>/?\\|")) :
                  return "Senha inválida. Deve conter ao menos um caractere especial (@ ou #).", 400
                elif not (set(dados["senha"]) & set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")):
                    return "Senha inválida. Deve conter ao menos uma letra.", 400
                elif not (set(dados["senha"]) & set("0123456789")):
                    return "Senha inválida. Deve conter ao menos um numero.", 400

            
        resultado = UsuarioService.cadastrar(dados)
        return jsonify({
            "mensagem": "Usuário cadastrado com sucesso",
            "usuario": resultado
        }), 201
        
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500

