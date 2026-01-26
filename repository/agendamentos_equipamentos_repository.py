import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )



class AgendamentoEquipamentoRepository:

    @staticmethod
    def inserir(agendamento: dict):
        """
        Insere um novo agendamento de equipamento
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agendamentos_equipamentos
            (equipamento_id, user_id, data_equip, hora_inicio, hora_fim, finalidade, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            agendamento["equipamento_id"],
            agendamento["user_id"],
            agendamento["data_equip"],
            agendamento["hora_inicio"],
            agendamento["hora_fim"],
            agendamento["finalidade"],
            agendamento.get("status", "pendente")
        ))

        conn.commit()
        agendamento_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return agendamento_id

    @staticmethod
    def existe_conflito(equipamento_id, data_equip, hora_inicio, hora_fim,agendamento_id=None):
        """
        Verifica conflito de horário para equipamento
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM agendamentos_equipamentos
            WHERE equipamento_id = %s
            AND data_equip = %s
            AND status != 'rejeitado'
            AND %s < hora_fim
            AND %s > hora_inicio
            LIMIT 1
        """, (
            equipamento_id,
            data_equip,
            hora_inicio,
            hora_fim
        ))

        conflito = cursor.fetchone()

        cursor.close()
        conn.close()

        return conflito is not None

    @staticmethod
    def listar_por_equipamento(equipamento_id):
        """
        Lista todos os agendamentos de um equipamento
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM agendamentos_equipamentos
            WHERE equipamento_id = %s
            ORDER BY data_equip, hora_inicio
        """, (equipamento_id,))

        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        return resultados

    @staticmethod
    def listar_por_usuario(user_id):
        """
        Lista todos os agendamentos feitos por um usuário
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM agendamentos_equipamentos
            WHERE user_id = %s
            ORDER BY data_equip DESC, hora_inicio
        """, (user_id,))

        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        return resultados

    @staticmethod
    def atualizar_status(agendamento_id, status):
        """
        Atualiza o status do agendamento (pendente, aprovado, cancelado)
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE agendamentos_equipamentos
            SET status = %s
            WHERE id = %s
        """, (status, agendamento_id))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def deletar(agendamento_id):
        """
        Remove o agendamento (uso administrativo)
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM agendamentos_equipamentos
            WHERE id = %s
        """, (agendamento_id,))

        conn.commit()
        cursor.close()
        conn.close()
