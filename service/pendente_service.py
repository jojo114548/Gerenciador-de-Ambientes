from repository.pendente_repository import PendenteRepository
from service.historico_service import HistoricoService
from repository.agendamentos_repository import AgendamentosRepository

class PendenteService:

 
    @staticmethod
    def criar_pendente(dados):

        """
        Cria um novo registro de pendente.

        - Valida se os dados foram informados
        - Garante que exista um usuário associado
        - Tenta inserir o pendente no banco
        - Trata erro de chave única (pendente duplicado)
        """

        # Validação básica dos dados
        if not dados:
            raise Exception("Dados do pendente não informados")
        
        
        # Garante que o usuário esteja associado ao pendente
        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")
        
      

        try:
            # Insere o pendente no banco de dados
            return PendenteRepository.inserir(dados)
        
        except Exception as e:
              # Trata violação de constraint única (pendente já existente)
            if "uq_pendente_agendamento" in str(e):
                return None
            # Repropaga qualquer outro erro
            raise

    @staticmethod
    def listar():
        """
        Retorna todos os registros de pendentes cadastrados.
        """
        return PendenteRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):         
        """
        Atualiza o status de um pendente.

        Fluxo:
        - Busca o pendente pelo ID
        - Valida existência
        - Verifica conflito de horário no ambiente
        - Atualiza o status
        - Registra histórico do ambiente
        - Retorna os dados atualizados
        """

         # Busca o pendente no banco
        pendente = PendenteRepository.buscar_por_id(pendente_id)
        
        # Valida se o pendente existe
        if not pendente:
            raise Exception("Pendente não encontrado")
        
        # Verifica se existe conflito de horário para o ambiente
        conflito = AgendamentosRepository.existe_conflito(
            ambiente_id=pendente["ambiente_id"],
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

        # Atualiza o status do pendente
        PendenteRepository.atualizar_status(pendente_id, status)

        # cria histórico
        HistoricoService.criar_historico({
            "agendamento_id": pendente["agendamento_id"],
            "user_id": pendente["user_id"],
            "type": "Ambientes",
            "name": pendente["ambiente_nome"],
            "historico_date": pendente["data"],
            "start_time": pendente["hora_inicio"],
            "end_time": pendente["hora_fim"],
            "purpose": pendente["finalidade"],
            "status": status
        })

        # Retorna o pendente com o status atualizado
        return {
            **pendente,
            "status": status
        }