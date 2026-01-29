import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class HistoricoEquipamentoRepository:

    @staticmethod
    def inserir(dados: dict):
        """Insere um registro no histórico de equipamentos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO historico_equipamentos (
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        """Lista todo o histórico de equipamentos"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.equipamento_id,
                    he.user_id,
                    he.equipamento_nome,
                    he.data_equip,
                    he.hora_inicio,
                    he.hora_fim,
                    he.finalidade,
                    he.status,
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico_equipamentos he
                INNER JOIN users u ON he.user_id = u.id
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """)
            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historicoEquip_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT *
                FROM historico_equipamentos
                WHERE id = %s
            """, (historicoEquip_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def atualizar_status_por_id(historicoEquip_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE historico_equipamentos
            SET status = %s
            WHERE id = %s
        """, (status, historicoEquip_id))
        conn.commit()

    
    @staticmethod
    def marcar_concluidos():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico_equipamentos
                SET status = 'Concluído'
                WHERE status = 'Confirmado'
                AND TIMESTAMP(data_equip, hora_fim) < NOW()
            """)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()