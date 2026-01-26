from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip


config_bp = Blueprint("config", __name__)


@config_bp.route('/config')
@jwt_required()
def config():
      
    logado = get_jwt()
    id_logado = get_jwt_identity()
    usuarios = UsuarioService.listar()
    pendentes_ambientes= PendenteService.listar()
    pendentes_equipamentos=PendenteServiceEquip.listar()
    return render_template('config.html', pendentes=pendentes_ambientes,pendentes_equipamentos=pendentes_equipamentos,id_logado=id_logado,logado=logado,usuarios=usuarios)