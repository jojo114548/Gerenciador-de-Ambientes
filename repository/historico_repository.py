import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class HistoricoRepository:

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    h.id,
                    h.agendamento_id,
                    h.user_id,
                    h.type,
                    h.name,
                    h.historico_date,
                    h.start_time,
                    h.end_time,
                    h.purpose,
                    h.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                ORDER BY h.historico_date DESC, h.start_time DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO historico (
                    agendamento_id,
                    user_id,
                    type,
                    name,
                    historico_date,
                    start_time,
                    end_time,
                    purpose,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["type"],
                dados["name"],
                dados["historico_date"],
                dados["start_time"],
                dados["end_time"],
                dados.get("purpose"),
                dados["status"]
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historico_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT *
                FROM historico
                WHERE id = %s
            """, (historico_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status_por_id(historico_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico
                SET status = %s
                WHERE id = %s
            """, (status, historico_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    

    @staticmethod
    def marcar_concluidos():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico
                SET status = 'Concluído'
                WHERE status = 'Confirmado'
                AND TIMESTAMP(historico_date, end_time) < NOW()
            """)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()