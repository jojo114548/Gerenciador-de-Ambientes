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


class PendenteEquipamentoRepository:

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                INSERT INTO nexus.pendentes_equipamentos
                    (agendamento_id, user_id, status)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["status"]
            ))

            pendente_id = cursor.fetchone()["id"]
            conn.commit()

            return {
                "pendente_id": pendente_id,
                "agendamento_id": dados["agendamento_id"],
                "user_id": dados["user_id"],
                "status": dados["status"]
            }

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(pendente_id, status):
        """
        ✅ CORRIGIDO: Agora atualiza corretamente pelo agendamento_id
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 1. Busca o agendamento_id do pendente
            cursor.execute("""
                SELECT agendamento_id 
                FROM nexus.pendentes_equipamentos
                WHERE id = %s
            """, (pendente_id,))
            
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Pendente {pendente_id} não encontrado")
            
            agendamento_id = result[0]

            # 2. Atualiza o status do pendente
            cursor.execute("""
                UPDATE nexus.pendentes_equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, pendente_id))

            # 3. Atualiza o status do agendamento de equipamento
            cursor.execute("""
                UPDATE nexus.agendamentos_equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, agendamento_id))  # ✅ CORRIGIDO: Usa agendamento_id

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(pendente_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT
                    p.id AS pendente_id,
                    p.agendamento_id,
                    p.user_id,
                    p.status,

                    ae.equipamento_id,
                    ae.data,
                    ae.hora_inicio,
                    ae.hora_fim,
                    ae.finalidade,

                    e.name AS equipamento_nome,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.pendentes_equipamentos p
                JOIN nexus.agendamentos_equipamentos ae 
                    ON ae.id = p.agendamento_id
                JOIN nexus.equipamentos e 
                    ON e.id = ae.equipamento_id
                JOIN nexus.users u
                    ON u.id = p.user_id
                WHERE p.id = %s
            """, (pendente_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT
                    p.id AS pendente_id,
                    p.agendamento_id,
                    p.user_id,
                    p.status,
                    p.created_at,

                    ae.equipamento_id,
                    ae.data,
                    ae.hora_inicio,
                    ae.hora_fim,
                    ae.finalidade,

                    e.name AS equipamento_nome,
                    e.categoria,
                    e.marca,
                    e.modelo,
                    
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.pendentes_equipamentos p
                JOIN nexus.agendamentos_equipamentos ae 
                    ON ae.id = p.agendamento_id
                JOIN nexus.equipamentos e 
                    ON e.id = ae.equipamento_id
                JOIN nexus.users u
                    ON u.id = p.user_id
                WHERE p.status = 'pendente'  -- ✅ Só mostra pendentes ativos
                ORDER BY ae.data DESC, ae.hora_inicio DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        """Lista pendentes de um usuário específico"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT
                    p.id AS pendente_id,
                    p.agendamento_id,
                    p.status,
                    p.created_at,

                    ae.data,
                    ae.hora_inicio,
                    ae.hora_fim,
                    ae.finalidade,

                    e.name AS equipamento_nome,
                    e.categoria
                FROM nexus.pendentes_equipamentos p
                JOIN nexus.agendamentos_equipamentos ae 
                    ON ae.id = p.agendamento_id
                JOIN nexus.equipamentos e 
                    ON e.id = ae.equipamento_id
                WHERE p.user_id = %s
                ORDER BY ae.data DESC, ae.hora_inicio DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(pendente_id):
        """Remove um pendente (cascata para agendamento)"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM nexus.pendentes_equipamentos
                WHERE id = %s
            """, (pendente_id,))

            if cursor.rowcount == 0:
                raise ValueError("Pendente não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()