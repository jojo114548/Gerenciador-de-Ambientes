import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class AgendamentosRepository:

    @staticmethod
    def inserir(agendamento):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO agendamentos
                (ambiente_id, data, hora_inicio, hora_fim, finalidade, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                agendamento["ambiente_id"],
                agendamento["data"],
                agendamento["hora_inicio"],
                agendamento["hora_fim"],
                agendamento["finalidade"],
                agendamento["status"]
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe_conflito(ambiente_id, data, hora_inicio, hora_fim, agendamento_id=None):
        """Verifica conflito de horário para ambiente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 1
                FROM agendamentos
                WHERE ambiente_id = %s
                  AND data = %s
                  AND status != 'rejeitado'
                  AND (%s < hora_fim AND %s > hora_inicio)
                  AND (%s IS NULL OR id != %s)
            """, (
                ambiente_id,
                data,
                hora_inicio,
                hora_fim,
                agendamento_id,
                agendamento_id
            ))

            return cursor.fetchone() is not None

        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    a.*,
                    amb.name as ambiente_nome,
                    amb.type as ambiente_tipo,
                    amb.localizacao,
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM agendamentos a
                INNER JOIN ambientes amb ON a.ambiente_id = amb.id
                INNER JOIN users u ON a.user_id = u.id
                WHERE a.status = 'pendente'
                ORDER BY a.created_at ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()
