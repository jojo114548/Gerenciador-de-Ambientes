from repository.ambientes_repository import AmbientesRepository
from service.notificacao_service import NotificacaoService
from model.ambientes import Ambiente


class AmbientesService:
    
    @staticmethod
    def listar():
   
      ambientes = AmbientesRepository.listar()

      for ambiente in ambientes:
            if ambiente["recursos"]:
                ambiente["recursos"] = ambiente["recursos"].split(" | ")
            else:
                ambiente["recursos"] = []

      return ambientes
    @staticmethod
    def inserir_ambiente(dados):
        
        ambiente = Ambiente(**dados)

        # INSERE O AMBIENTE E RECEBE O ID REAL
        ambiente_id = AmbientesRepository.inserir_ambiente(ambiente)

        # recursos vindos do form
        recursos = dados.get("recursos", [])

        # insere os recursos com o ID correto
        if recursos:
            AmbientesRepository.inserir_recursos(
                ambiente_id,
                recursos
            )
        
        

    @staticmethod
    def deletar_ambiente(ambiente_id):
        AmbientesRepository.deletar_ambiente(ambiente_id)
        
        

  

    @staticmethod
    def atualizar_ambiente(dados):
        ambiente = Ambiente(**dados)
        AmbientesRepository.atualizar_ambiente(ambiente)
        
        