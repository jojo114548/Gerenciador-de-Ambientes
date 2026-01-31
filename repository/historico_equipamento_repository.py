import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="jojo4548",
        dbname="Nexus",
        port=5432,
        options="-c search_path=nexus"
    )


class HistoricoEquipamentoRepository:

    @staticmethod
    def inserir(dados: dict):
        """
        ✅ CORRIGIDO: Insere registro no histórico de equipamentos
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            print(f"\n=== INSERIR HISTÓRICO EQUIPAMENTO ===")
            print(f"Dados recebidos: {dados}")
            
            # ✅ Verificar se todos os campos estão presentes
            campos_obrigatorios = [
                "agendamento_id", "equipamento_id", "user_id",
                "equipamento_nome", "data_equip", "hora_inicio",
                "hora_fim", "finalidade", "status"
            ]
            
            for campo in campos_obrigatorios:
                if campo not in dados:
                    raise ValueError(f"Campo obrigatório ausente: {campo}")
                if dados[campo] is None:
                    raise ValueError(f"Campo {campo} não pode ser NULL")
            
            # Executar INSERT
            cursor.execute("""
               -- Inserir histórico dos agendamentos já confirmados
INSERT INTO nexus.historico_equipamentos (
    agendamento_id,
    equipamento_id,
    user_id,
    equipamento_nome,
    data_equip,
    hora_inicio,
    hora_fim,
    finalidade,
    status
)
SELECT 
    ae.id,
    ae.equipamento_id,
    ae.user_id,
    e.name,
    ae.data,
    ae.hora_inicio,
    ae.hora_fim,
    ae.finalidade,
    pe.status::nexus.status_historico
FROM nexus.pendentes_equipamentos pe
JOIN nexus.agendamentos_equipamentos ae ON pe.agendamento_id = ae.id
JOIN nexus.equipamentos e ON ae.equipamento_id = e.id
WHERE pe.status IN ('Confirmado', 'Rejeitado', 'Cancelado')
  AND NOT EXISTS (
      SELECT 1 
      FROM nexus.historico_equipamentos he 
      WHERE he.agendamento_id = pe.agendamento_id
  );
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                dados["agendamento_id"],
                dados["equipamento_id"],
                dados["user_id"],
                dados["equipamento_nome"],
                dados["data_equip"],
                dados["hora_inicio"],
                dados["hora_fim"],
                dados["finalidade"],
                dados["status"]
            ))

            historico_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"✅ Histórico inserido com sucesso! ID: {historico_id}")
            print(f"=== FIM INSERIR HISTÓRICO ===\n")
            
            return historico_id

        except psycopg2.Error as e:
            conn.rollback()
            print(f"❌ ERRO PostgreSQL ao inserir histórico:")
            print(f"   Código: {e.pgcode}")
            print(f"   Mensagem: {e.pgerror}")
            raise
            
        except Exception as e:
            conn.rollback()
            print(f"❌ ERRO ao inserir histórico: {e}")
            import traceback
            traceback.print_exc()
            raise
            
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        """Lista todo o histórico"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    u.name AS usuario_nome,
                    u.email AS usuario_email,
                    u.departamento,
                    e.categoria AS equipamento_categoria,
                    e.marca AS equipamento_marca,
                    e.modelo AS equipamento_modelo
                FROM nexus.historico_equipamentos he
                INNER JOIN nexus.users u ON he.user_id = u.id
                LEFT JOIN nexus.equipamentos e ON he.equipamento_id = e.id
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historicoEquip_id):
        """Busca histórico por ID"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    u.name AS usuario_nome,
                    u.email AS usuario_email,
                    u.departamento,
                    e.categoria AS equipamento_categoria,
                    e.marca AS equipamento_marca,
                    e.modelo AS equipamento_modelo
                FROM nexus.historico_equipamentos he
                INNER JOIN nexus.users u ON he.user_id = u.id
                LEFT JOIN nexus.equipamentos e ON he.equipamento_id = e.id
                WHERE he.id = %s
            """, (historicoEquip_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        """Lista histórico de um usuário"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    e.categoria,
                    e.marca,
                    e.modelo
                FROM nexus.historico_equipamentos he
                LEFT JOIN nexus.equipamentos e ON e.id = he.equipamento_id
                WHERE he.user_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_equipamento(equipamento_id):
        """Lista histórico de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico_equipamentos he
                INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.equipamento_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (equipamento_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def marcar_concluidos():
        """Marca agendamentos concluídos automaticamente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico_equipamentos
                SET status = 'Concluido'
                WHERE status = 'Confirmado'
                  AND (
                        data_equip < CURRENT_DATE
                        OR (
                            data_equip = CURRENT_DATE
                            AND hora_fim < CURRENT_TIME
                        )
                  )
            """)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()