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

painelAdm_bp = Blueprint("painelAdm", __name__)


@painelAdm_bp.route('/painelAdm')
@jwt_required()
def painelAdm():
    

        id_logado = get_jwt_identity()
        logado = get_jwt()

        if id != id_logado and logado["role"] != "admin":
         return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Listar dados
        usuarios = UsuarioService.listar()
        pendentes_ambientes = PendenteService.listar()
        pendentes_equipamentos = PendenteServiceEquip.listar()
        ambientes = AmbientesService.listar()
        equipamentos = EquipamentoService.listar()
        historico = HistoricoRepository.listar_todos()
        historico_equipamento = HistoricoEquipamentoRepository.listar()
        
        # Listar eventos com verificação de inscrição
        evento = EventosRepository.listar()
        for event in evento:
            event["inscrito"] = EventosRepository.usuario_ja_inscrito(
                event["id"],
                id_logado
            )
        
        return render_template(
            'painelAdm.html',
            pendentes=pendentes_ambientes,
            pendentes_equipamentos=pendentes_equipamentos,
            id_logado=id_logado,
            logado=logado,
            usuarios=usuarios,
            ambientes=ambientes,
            equipamentos=equipamentos,
            evento=evento,
            historico=historico,
            historico_equip=historico_equipamento
        )
    
   