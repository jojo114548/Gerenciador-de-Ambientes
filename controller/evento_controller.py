from flask import Blueprint, render_template, request, jsonify
from service.usuario_service import UsuarioService
from repository.eventos_repository import EventosRepository
from repository.recursosEventos_repository import RecursosRepository
from service.eventos_service import EventosService
from flask_jwt_extended import ( get_jwt_identity, jwt_required,get_jwt
)
from datetime import timedelta
import uuid
import os
from werkzeug.utils import secure_filename
from service.notificacao_service import NotificacaoService


# Cria o Blueprint para as rotas de eventos
eventos_bp = Blueprint("eventos", __name__)



@eventos_bp.route('/eventos')
@jwt_required()
def eventos():
     """
    Rota para exibir a página de listagem de eventos.
    
     """
     
     # Obtém os dados completos do JWT 
     logado = get_jwt()
     # Obtém o ID do usuário logado a partir do token JWT
     id_logado = get_jwt_identity()
     # Busca todos os eventos cadastrados no banco de dados
     evento=EventosRepository.listar()
     # Para cada evento, verifica se o usuário logado está inscrito
     for event in evento:
        
        event["inscrito"] = EventosRepository.usuario_ja_inscrito(
            event["id"],
            id_logado
        )
    

     # Busca todos os usuários cadastrados no sistema
     usuarios = UsuarioService.listar()
     # Busca todos os ambientes disponíveis para eventos
     ambientes = RecursosRepository.listar_ambientes()
     # Busca todos os equipamentos disponíveis para eventos
     equipamentos = RecursosRepository.listar_equipamentos()
    
     # Renderiza o template de eventos passando todos os dados necessários
     return render_template(
        "eventos.html",
        evento=evento,  # Lista de eventos com status de inscrição
        id_logado=id_logado,  # ID do usuário logado
        logado=logado,  # Dados completos do JWT (incluindo role)
        usuarios=usuarios,  # Lista de todos os usuários
        ambientes=ambientes,  # Lista de ambientes disponíveis
        equipamentos=equipamentos  # Lista de equipamentos disponíveis
    )

@eventos_bp.route("/eventos", methods=["POST"])
@jwt_required()
def criar_evento():
    """
    Rota para criar um novo evento no sistema.
    
    """
    
    # Obtém o ID do usuário logado a partir do token JWT
    id_logado = get_jwt_identity()

    try:
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()

        # Processa imagem
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Inicializa caminho da imagem como None (caso não seja enviada)
        image_path = None

        # Se uma imagem foi enviada e tem nome de arquivo válido
        if imagem and imagem.filename:
            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho onde a imagem será salva
            caminho = f"static/imgs/{filename}"
            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/{caminho}"

        # Monta o dicionário com todos os dados do novo evento
        dados = {
        "titulo": request.form.get("titulo"),  # Título do evento
        "data_evento": request.form.get("data_evento"),  # Data do evento
        "hora_evento": request.form.get("hora_evento"),  # Hora do evento
        "ambiente_id": request.form.get("ambiente_id"),  # ← AQUI - ID do ambiente onde ocorrerá
        "localizacao": request.form.get("localizacao"),  # Localização do evento
        "descricao": request.form.get("descricao"),  # Descrição do evento
        "participantes": request.form.get("participantes", 0),  # Número inicial de participantes
        "capacidade": request.form.get("capacidade"),  # Capacidade máxima do evento
        "instrutor": request.form.get("instrutor"),  # Nome do instrutor/responsável
        "tipo": request.form.get("tipo"),  # Tipo do evento (workshop, palestra, etc)
        "image": image_path  # Caminho da imagem do evento
    }

        
        # Processa equipamentos
        # Obtém lista de IDs dos equipamentos selecionados
        equipamentos_ids = request.form.getlist("equipamentos[]")
        # Obtém lista de quantidades correspondentes a cada equipamento
        quantidades = request.form.getlist("quantidades[]")
        
        # Inicializa lista para armazenar equipamentos processados
        equipamentos = []
        # Se houver equipamentos selecionados
        if equipamentos_ids:
            # Para cada ID de equipamento na lista
            for i, equip_id in enumerate(equipamentos_ids):
                if equip_id:  # Ignora vazios - verifica se o ID não é string vazia
                    # Adiciona equipamento com ID e quantidade à lista
                    equipamentos.append({
                        "equipamento_id": int(equip_id),  # Converte ID para inteiro
                        "quantidade": int(quantidades[i]) if i < len(quantidades) else 1  # Quantidade ou 1 como padrão
                    })
        
        # Cria o evento
        # Chama o serviço para criar o evento com os dados e equipamentos
        evento_id = EventosService.criar(dados, equipamentos)


        # Envia notificação ao usuário informando que o evento foi criado
        NotificacaoService.criar_notificacao(
            user_id=id_logado,  # ID do criador do evento
            titulo="O evento foi criado",  # Título da notificação
            mensagem=f"O evento foi  '{dados['titulo']}' criado",  # Mensagem com nome do evento
            tipo="aviso"  # Tipo da notificação
    )
        # Retorna mensagem de sucesso com ID do evento criado e status 201 (Created)
        return jsonify({
                "mensagem": "Evento criado com sucesso",
                "evento_id": evento_id
            }), 201

    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar evento: {str(e)}"}), 500
    


@eventos_bp.route("/eventos/<id>", methods=["DELETE"])
@jwt_required()
def deletar_evento(id):
    """
    Rota para excluir um evento do sistema.
    
    """
  
    try:
        # Obtém os dados completos do JWT
        logado = get_jwt()
       

        # Verifica se o usuário tem permissão de administrador
        if  logado["role"] != "admin":
            # Retorna erro 403  se não for admin
            return jsonify({"erro": "Você não tem permissão para editar este usuário."}), 403
        
        # Remove o evento do banco de dados pelo ID
        EventosService.remover(id)
        
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Evento excluído"}), 200

    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar "}), 500
   

@eventos_bp.route("/eventos/<evento_id>/inscrever", methods=["POST"])
@jwt_required()
def inscrever_evento(evento_id):
    """
    Rota para inscrever o usuário logado em um evento.
    
    """
    # Obtém o ID do usuário logado a partir do token JWT
    id_logado = get_jwt_identity()

    try:
        # Chama o serviço para realizar a inscrição do usuário no evento
        EventosService.inscrever(evento_id, id_logado)
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Inscrição realizada"}), 200
    # Tratamento de erros de validação (ValueError) - ex: evento lotado, já inscrito
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@eventos_bp.route("/eventos/<evento_id>/detalhes", methods=["GET"])
@jwt_required()
def detalhes_evento(evento_id):
    """
    Rota para buscar detalhes completos de um evento específico.
    
    """
    try:
        
        # Busca os detalhes completos do evento pelo ID (incluindo equipamentos)
        evento = EventosService.buscar_detalhes(evento_id)
        # Se o evento não for encontrado
        if not evento:
            # Retorna erro 404 (Not Found)
            return jsonify({"erro": "Evento não encontrado"}), 404
        
        # Retorna os dados do evento em formato JSON com status 200 (OK)
        return jsonify(evento), 200
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500