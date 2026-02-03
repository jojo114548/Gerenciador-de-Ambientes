from repository.pendente_equipamento_repository import (
    PendenteEquipamentoRepository
)
from service.historico_equipamento_service import (
    HistoricoEquipamentoService
)

from repository.agendamentos_equipamentos_repository import AgendamentoEquipamentoRepository


class PendenteServiceEquip:

    @staticmethod
    def criar_pendente(dados):
        """
        Cria um novo registro de pendente de equipamento.

        - Valida se os dados foram informados
        - Garante que o usuário esteja associado
        - Insere o pendente no banco
        - Trata duplicidade por constraint única
        """
        # Validação básica de existência dos dados
        if not dados:
            raise Exception("Dados do pendente não informados")
        
         # Garante que o pendente tenha um usuário associado
        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")
        
        try:
             # Insere o pendente no banco de dados
            return PendenteEquipamentoRepository.inserir(dados)
        
        except Exception as e:
            # Trata violação de constraint única (pendente duplicado)
            if "uq_pendente_agendamento" in str(e):
                return None
            # Repropaga qualquer outro erro
            raise

    @staticmethod
    def listar():
        """
        Retorna todos os pendentes de equipamentos cadastrados.
        """
        return PendenteEquipamentoRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):
        """
        Atualiza o status de um pendente de equipamento.

        Fluxo completo:
        - Busca o pendente pelo ID
        - Valida existência
        - Verifica se já existe histórico para o agendamento
        - Atualiza o status do pendente
        - Cria histórico (somente para status finais e se ainda não existir)
        - Envia notificações ao usuário
        - Retorna os dados atualizados
        """
       
         # Busca o pendente pelo ID
        pendente = PendenteEquipamentoRepository.buscar_por_id(pendente_id)

         # Valida se o pendente existe
        if not pendente:
            raise ValueError("Pendente não encontrado")

         # Verifica se existe conflito de horário para equipamento
        conflito = AgendamentoEquipamentoRepository.existe_conflito(
        equipamento_id=pendente["equipamento_id"],
        data=pendente["data"],
        hora_inicio=pendente["hora_inicio"],
        hora_fim=pendente["hora_fim"],
        agendamento_id=pendente["agendamento_id"]  
    )
        
         # Caso exista conflito, bloqueia a atualização
        if conflito:
            raise ValueError(
                "Conflito de horário: o ambiente já está reservado nesse período."
            )
        

         #  Atualiza status do pendente (sempre)
        PendenteEquipamentoRepository.atualizar_status(pendente_id, status)

        # Cria histórico     
        HistoricoEquipamentoService.criar_historico({
                    "agendamento_id": pendente["agendamento_id"],
                    "equipamento_id": pendente["equipamento_id"],
                    "user_id": pendente["user_id"],
                    "equipamento_nome": pendente["equipamento_nome"],
                    "data_equip": pendente["data"],
                    "hora_inicio": pendente["hora_inicio"],
                    "hora_fim": pendente["hora_fim"],
                    "finalidade": pendente["finalidade"],
                    "status": status
                })
        # Retorna o pendente com o status atualizado
        return {
            **pendente,
            "status": status
        }
