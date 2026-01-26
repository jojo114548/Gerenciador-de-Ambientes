import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class PendenteEquipamentoRepository:

 
    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO pendentes_equipamentos
                    (agendamento_id, user_id, status)
                VALUES (%s, %s, %s)
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["status"]
            ))

            conn.commit()

            return {
                "pendente_id": cursor.lastrowid,
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
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE pendentes_equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, pendente_id))

            # atualiza o agendamento de equipamento
            cursor.execute("""
                UPDATE agendamentos_equipamentos
                SET status = %s
                WHERE id = (
                    SELECT agendamento_id
                    FROM pendentes_equipamentos
                    WHERE id = %s
                )
            """, (status, pendente_id))

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
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id AS pendente_id,
                p.agendamento_id,
                p.user_id,
                p.status,

                ae.equipamento_id,
                ae.data_equip,
                ae.hora_inicio,
                ae.hora_fim,
                ae.finalidade,

                e.name AS equipamento_nome
            FROM pendentes_equipamentos p
            JOIN agendamentos_equipamentos ae 
                ON ae.id = p.agendamento_id
            JOIN equipamentos e 
                ON e.id = ae.equipamento_id
            WHERE p.id = %s
        """, (pendente_id,))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id AS pendente_id,
                p.agendamento_id,
                p.user_id,
                p.status,

                ae.equipamento_id,
                ae.data_equip,
                ae.hora_inicio,
                ae.hora_fim,
                ae.finalidade,

                e.name AS equipamento_nome
            FROM pendentes_equipamentos p
            JOIN agendamentos_equipamentos ae 
                ON ae.id = p.agendamento_id
            JOIN equipamentos e 
                ON e.id = ae.equipamento_id
            ORDER BY ae.data_equip DESC, ae.hora_inicio DESC
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result