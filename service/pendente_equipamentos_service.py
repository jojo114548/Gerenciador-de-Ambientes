from repository.pendente_equipamento_repository import (
    PendenteEquipamentoRepository
)
from service.historico_equipamento_service import (
    HistoricoEquipamentoService
)
from service.notificacao_service import NotificacaoService


class PendenteServiceEquip:

    @staticmethod
    def criar_pendente(dados):
        if not dados:
            raise Exception("Dados do pendente não informados")

        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")
        
       

        try:
            return PendenteEquipamentoRepository.inserir(dados)
        except Exception as e:
            if "uq_pendente_agendamento" in str(e):
                return None
            raise

    @staticmethod
    def listar():
        return PendenteEquipamentoRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):


        pendente = PendenteEquipamentoRepository.buscar_por_id(pendente_id)
        if not pendente:
            raise ValueError("Pendente não encontrado")

       
        PendenteEquipamentoRepository.atualizar_status(pendente_id, status)
        if status == 'Confirmado':
            # Mover para histórico
            try:
                HistoricoEquipamentoService.criar_historico({
                    "agendamento_id": pendente["agendamento_id"],
                    "equipamento_id": pendente["equipamento_id"],
                    "user_id": pendente["user_id"],
                    "equipamento_nome": pendente["equipamento_nome"],
                    "data_equip": pendente["data"],
                    "hora_inicio": pendente["hora_inicio"],
                    "hora_fim": pendente["hora_fim"],
                    "finalidade": pendente["finalidade"],
                    "status": "Confirmado"
                })
            except Exception as e:
                print(f"Erro ao criar histórico: {e}")

            # Notificar usuário - Aprovação
            try:
                NotificacaoService.criar_notificacao({
                    "user_id": pendente["user_id"],
                    "titulo": "Agendamento Aprovado",
                    "mensagem": f"Seu agendamento do equipamento '{pendente['equipamento_nome']}' foi aprovado para {pendente['data']} às {pendente['hora_inicio']}.",
                    "tipo": "sucesso"
                })
            except Exception as e:
                print(f"Erro ao criar notificação: {e}")
            
        elif status == 'Rejeitado':
            # Mover para histórico com status Rejeitado
            try:
                HistoricoEquipamentoService.criar_historico({
                    "agendamento_id": pendente["agendamento_id"],
                    "equipamento_id": pendente["equipamento_id"],
                    "user_id": pendente["user_id"],
                    "equipamento_nome": pendente["equipamento_nome"],
                    "data_equip": pendente["data"],
                    "hora_inicio": pendente["hora_inicio"],
                    "hora_fim": pendente["hora_fim"],
                    "finalidade": pendente["finalidade"],
                    "status": "Rejeitado"
                })
            except Exception as e:
                print(f"Erro ao criar histórico: {e}")

                
                

            return pendente

