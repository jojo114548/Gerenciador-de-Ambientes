from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.ambientes_service import AmbientesService
import uuid,os
from werkzeug.utils import secure_filename
from service.equipamento_service import EquipamentoService

equipamento_bp = Blueprint("equipamento", __name__)


@equipamento_bp.route('/equipamentos')
@jwt_required()
def equipamentos():
    try:
        logado = get_jwt()
        id_logado = get_jwt_identity()

        usuarios = UsuarioService.listar()
        equipamentos = EquipamentoService.listar()


        return render_template('equipamentos.html',
        equipamentos=equipamentos,
        id_logado=id_logado,
        logado=logado,
        usuarios=usuarios)
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
    

@equipamento_bp.route('/equipamento', methods=['POST'])
@jwt_required()
def cadastrar_equipamento():

    try:
        logado = get_jwt()
       

        if logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
         
        imagem = request.files.get("image")
        image_path = request.form.get("image_atual")

        if imagem:
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = f"static/imgs/{filename}"
            imagem.save(caminho)
            image_path = f"/{caminho}"

        dados = {
            
            "name": request.form.get("name"),
            "categoria": request.form.get("categoria"),
            "status": request.form.get("status") or "Disponivel",
            "descricao": request.form.get("descricao"),
            "marca": request.form.get("marca"),
            "modelo": request.form.get("modelo"),
            "condicao": request.form.get("condicao"),
            "quantidade_disponivel": int(request.form.get("quantidade_disponivel")),
            "image": image_path,
            "especificacoes": request.form.getlist("especificacoes[]")
        }

        EquipamentoService.inserir_equipamento(dados)
        return jsonify({"mensagem": "Equipamento cadastrado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
    

@equipamento_bp.route('/editar-equipamento/<id>', methods=['POST'])
@jwt_required()
def editar_equipamento(id):
    try:
         
        logado = get_jwt()
       
        if logado["role"] != "admin":
          return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        imagem = request.files.get("image")
        image_path = request.form.get("image_atual")

        if imagem and imagem.filename:
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = f"static/imgs/{filename}"
            imagem.save(caminho)
            image_path = f"/{caminho}"

        qtd = request.form.get("quantidade_disponivel")
        if qtd is None or qtd == "":
            return jsonify({"erro": "Quantidade disponível é obrigatória"}), 400

        quantidade = int(qtd)

        status = request.form.get("status")
        if quantidade <= 0:
            status = "ocupado"
        elif not status:
            status = "disponivel"

        dados = {
            "id": id,
            "name": request.form.get("name"),
            "categoria": request.form.get("categoria"),
            "status": status,
            "descricao": request.form.get("descricao"),
            "marca": request.form.get("marca"),
            "modelo": request.form.get("modelo"),
            "condicao": request.form.get("condicao"),
            "quantidade_disponivel": quantidade,
            "image": image_path,
            "especificacoes": request.form.getlist("especificacoes[]")
        }

        EquipamentoService.atualizar_equipamento(dados)
        return jsonify({"mensagem": "Equipamento atualizado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500

@equipamento_bp.route("/equipamentos/<id>", methods=["DELETE"])
@jwt_required()
def deletar_equipamento(id):
        try:
            logado = get_jwt()
       
            if logado["role"] != "admin":
              return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
            EquipamentoService.deletar_equipamento(id)
            return jsonify({'mensagem': 'Equipamento excluído com sucesso'}), 200
        except ValueError as e:
          return jsonify({"erro": str(e)}), 400
        except Exception as e:
          print(e)
          return jsonify({"erro": "Erro ao alterar senha"}), 500

@equipamento_bp.route("/novo-equipamento", methods=["GET", "POST"])
@jwt_required()
def novo_equipamento():
    try:
        # 🔹 GET apenas exibe a página
        if request.method == "GET":
            return render_template("novo_equipamento.html")

        # 🔹 POST → cria equipamento
        imagem = request.files.get("image")
        image_path = None

        if imagem and imagem.filename:
            os.makedirs("static/imgs", exist_ok=True)

            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = os.path.join("static/imgs", filename)

            imagem.save(caminho)
            image_path = f"/static/imgs/{filename}"

        dados = {
            "name": request.form.get("name"),
            "categoria": request.form.get("categoria"),
            "status": request.form.get("status") or "Disponivel",
            "descricao": request.form.get("descricao"),
            "marca": request.form.get("marca"),
            "modelo": request.form.get("modelo"),
            "condicao": request.form.get("condicao"),
            "quantidade_disponivel": int(request.form.get("quantidade", 0)),
            "image": image_path,
            "especificacoes": request.form.getlist("especificacoes[]")
        }

        # 🔒 Validação mínima
        if not dados["name"] or not dados["categoria"]:
            return "Nome e categoria são obrigatórios", 400

        EquipamentoService.inserir_equipamento(dados)
        
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"erro": "Erro ao alterar senha"}), 500

