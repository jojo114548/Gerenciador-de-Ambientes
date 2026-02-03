from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt
)
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip
from service.ambientes_service import AmbientesService
from service.equipamento_service import EquipamentoService
from repository.eventos_repository import EventosRepository
from repository.historico_equipamento_repository import HistoricoEquipamentoRepository
from repository.historico_repository import HistoricoRepository

# Cria o Blueprint para as rotas do painel administrativo
painelAdm_bp = Blueprint("painelAdm", __name__)


@painelAdm_bp.route('/painelAdm')
@jwt_required()
def painelAdm():
        """
        Rota principal do painel administrativo do sistema.
        
        Funcionalidade:
        - Requer autenticação JWT (usuário deve estar logado)

        """
    

        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()
        # Obtém os dados completos do JWT 
        logado = get_jwt()

        # Verifica permissões de acesso ao painel
        if logado["role"] != "admin":
            # Retorna erro 403 - acesso negado
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Listar dados
        # Busca todos os usuários cadastrados no sistema
        usuarios = UsuarioService.listar()
        # Busca todas as solicitações pendentes de ambientes
        pendentes_ambientes = PendenteService.listar()
        # Busca todas as solicitações pendentes de equipamentos
        pendentes_equipamentos = PendenteServiceEquip.listar()
        # Busca todos os ambientes cadastrados
        ambientes = AmbientesService.listar()
        # Busca todos os equipamentos cadastrados
        equipamentos = EquipamentoService.listar()
        # Busca o histórico completo de reservas de ambientes
        historico = HistoricoRepository.listar_todos()
        # Busca o histórico completo de uso de equipamentos
        historico_equipamento = HistoricoEquipamentoRepository.listar()
        
     
        # Busca todos os eventos cadastrados
        evento = EventosRepository.listar()
        # Para cada evento, verifica se o usuário logado está inscrito
        for event in evento:
            #Verifica se usuario  usuário está inscrito neste evento
            event["inscrito"] = EventosRepository.usuario_ja_inscrito(
                event["id"],
                id_logado
            )
        
        # Renderiza o template do painel administrativo passando todos os dados necessários
        return render_template(
            'painelAdm.html',
            pendentes=pendentes_ambientes,  # Solicitações pendentes de ambientes
            pendentes_equipamentos=pendentes_equipamentos,  # Solicitações pendentes de equipamentos
            id_logado=id_logado,  # ID do usuário logado
            logado=logado,  # Dados completos do JWT 
            usuarios=usuarios,  # Lista de todos os usuários
            ambientes=ambientes,  # Lista de todos os ambientes
            equipamentos=equipamentos,  # Lista de todos os equipamentos
            evento=evento,  # Lista de eventos com status de inscrição
            historico=historico,  # Histórico de reservas de ambientes
            historico_equip=historico_equipamento  # Histórico de uso de equipamentos
        )