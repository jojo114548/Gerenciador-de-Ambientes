
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from service.usuario_service import UsuarioService

from flask_jwt_extended import (jwt_required)

from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip


# Cria um Blueprint chamado "pendente" para organizar rotas relacionadas a pendências
pendente_bp = Blueprint("pendente", __name__)



@pendente_bp.route('/pendentes/<int:pendente_id>/status', methods=['POST'])
@jwt_required() 
def atualizar_status_pendente(pendente_id):
    """
    Atualiza o status de uma solicitação pendente de AMBIENTE.
    
    """
    try:
        # Obtém os dados JSON enviados no corpo da requisição
        dados = request.get_json()
        
        # Extrai o novo status do JSON
        # Possíveis valores: "aprovado", "rejeitado", "pendente", etc.
        status = dados.get("status")

        # Chama o serviço para atualizar o status da pendência no banco de dados
        PendenteService.atualizar_status(pendente_id, status)

        # Retorna resposta de sucesso com status HTTP 200
        return jsonify({"mensagem": "Status atualizado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        return jsonify({"erro": str(e)}), 500



@pendente_bp.route('/pendentes-equipamentos/<int:pendente_id>/status', methods=['PUT'])
@jwt_required()  
def atualizar_status_pendente_equipamento(pendente_id):
    """
    Atualiza o status de uma solicitação pendente de EQUIPAMENTO.
    
    """
    try:
        # Obtém os dados JSON enviados no corpo da requisição
        dados = request.get_json()
        
        # Extrai o novo status do JSON
        # Possíveis valores: "aprovado", "rejeitado", "pendente", etc.
        status = dados.get("status")

        # Chama o serviço específico para atualizar o status da pendência de EQUIPAMENTO
        PendenteServiceEquip.atualizar_status(pendente_id, status)

        # Retorna resposta de sucesso com status HTTP 200
        return jsonify({"mensagem": "Status do equipamento atualizado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500