from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from repository.eventos_repository import EventosRepository
from repository.recursosEventos_repository import RecursosRepository
from service.eventos_service import EventosService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from datetime import timedelta
import uuid
import os
from werkzeug.utils import secure_filename
from service.notificacao_service import NotificacaoService


eventos_bp = Blueprint("eventos", __name__)



@eventos_bp.route('/eventos')
@jwt_required()
def eventos():
     
    
    
     logado = get_jwt()
     id_logado = get_jwt_identity()
     evento=EventosRepository.listar()
     for event in evento:
        event["inscrito"] = EventosRepository.usuario_ja_inscrito(
            event["id"],
            id_logado
        )
    

     usuarios = UsuarioService.listar()
     ambientes = RecursosRepository.listar_ambientes()
     equipamentos = RecursosRepository.listar_equipamentos()
    
     return render_template(
        "eventos.html",
        evento=evento,
        id_logado=id_logado,
        logado=logado,
        usuarios=usuarios,
        ambientes=ambientes,
        equipamentos=equipamentos
    )

@eventos_bp.route("/eventos", methods=["POST"])
@jwt_required()
def criar_evento():
    
    id_logado = get_jwt_identity()

    try:
        id_logado = get_jwt_identity()

        # Processa imagem
        imagem = request.files.get("image")
        image_path = None

        if imagem and imagem.filename:
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            caminho = f"static/imgs/{filename}"
            imagem.save(caminho)
            image_path = f"/{caminho}"

        dados = {
        "titulo": request.form.get("titulo"),
        "data_evento": request.form.get("data_evento"),
        "hora_evento": request.form.get("hora_evento"),
        "ambiente_id": request.form.get("ambiente_id"),  # ← AQUI
        "localizacao": request.form.get("localizacao"),
        "descricao": request.form.get("descricao"),
        "participantes": request.form.get("participantes", 0),
        "capacidade": request.form.get("capacidade"),
        "instrutor": request.form.get("instrutor"),
        "tipo": request.form.get("tipo"),
        "image": image_path
    }

        
        # Processa equipamentos
        equipamentos_ids = request.form.getlist("equipamentos[]")
        quantidades = request.form.getlist("quantidades[]")
        
        equipamentos = []
        if equipamentos_ids:
            for i, equip_id in enumerate(equipamentos_ids):
                if equip_id:  # Ignora vazios
                    equipamentos.append({
                        "equipamento_id": int(equip_id),
                        "quantidade": int(quantidades[i]) if i < len(quantidades) else 1
                    })
                    # Cria o evento
        evento_id = EventosService.criar(dados, equipamentos)


        NotificacaoService.criar_notificacao(
            user_id=id_logado,
            titulo="O evento foi criado",
            mensagem=f"O evento foi  '{dados['titulo']}' criado",
            tipo="aviso"
    )
        return jsonify({
                "mensagem": "Evento criado com sucesso",
                "evento_id": evento_id
            }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar evento: {str(e)}"}), 500
    

@eventos_bp.route("/eventos/<id>", methods=["PUT"])
@jwt_required()
def atualizar_evento(id):
    try:
        logado = get_jwt()
       

        if  logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para editar este usuário."}), 403
        
        dados = request.get_json()
        equipamentos = dados.pop("equipamentos", None)

        
        EventosService.atualizar(id, dados,equipamentos)
        return jsonify({"mensagem": "Evento atualizado com sucesso"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
    

@eventos_bp.route("/eventos/<id>", methods=["DELETE"])
@jwt_required()
def deletar_evento(id):

    
    try:
        logado = get_jwt()
       

        if  logado["role"] != "admin":
            return jsonify({"erro": "Você não tem permissão para editar este usuário."}), 403
        
        EventosService.remover(id)
        
        return jsonify({"mensagem": "Evento excluído"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
   

@eventos_bp.route("/eventos/<evento_id>/inscrever", methods=["POST"])
@jwt_required()
def inscrever_evento(evento_id):
    id_logado = get_jwt_identity()

    try:
        EventosService.inscrever(evento_id, id_logado)
        return jsonify({"mensagem": "Inscrição realizada"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@eventos_bp.route("/eventos/<evento_id>/detalhes", methods=["GET"])
@jwt_required()
def detalhes_evento(evento_id):
    """Retorna detalhes completos do evento incluindo equipamentos"""
    try:
        
        evento = EventosService.buscar_detalhes(evento_id)
        if not evento:
            return jsonify({"erro": "Evento não encontrado"}), 404
        
        return jsonify(evento), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


