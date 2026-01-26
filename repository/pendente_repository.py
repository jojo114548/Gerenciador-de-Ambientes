import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class PendenteRepository:

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO pendentes_ambientes
                    (agendamento_id, user_id, status)
                VALUES (%s, %s, %s)
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["status"]
            ))

            conn.commit()

            return {
                "id": cursor.lastrowid,
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
    def buscar_por_id(pendente_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id AS pendente_id,
                p.status,
                p.user_id,

                a.id AS agendamento_id,
                a.ambiente_id,
                a.data,
                a.hora_inicio,
                a.hora_fim,
                a.finalidade,

                amb.name AS ambiente_nome
            FROM pendentes_ambientes p
            JOIN agendamentos a ON a.id = p.agendamento_id
            JOIN ambientes amb ON amb.id = a.ambiente_id
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

    amb.id AS ambiente_id,
    amb.name AS ambiente_nome,

    a.data,
    a.hora_inicio,
    a.hora_fim,
    a.finalidade
FROM pendentes_ambientes p
JOIN agendamentos a ON a.id = p.agendamento_id
JOIN ambientes amb ON amb.id = a.ambiente_id
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def atualizar_status(pendente_id, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pendentes_ambientes
            SET status = %s
            WHERE id = %s
        """, (status, pendente_id))

        conn.commit()
        cursor.close()
        conn.close()