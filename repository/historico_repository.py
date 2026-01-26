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
        """Lista todo o histórico de agendamentos de ambientes"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                ORDER BY h.historico_date DESC, h.start_time DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historico_id):
        """Busca um registro específico do histórico por ID"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email,
                    u.departamento
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                WHERE h.id = %s
            """, (historico_id,))
            
            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir(dados):
        """Insere um registro no histórico de agendamentos"""
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
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        """Lista histórico de agendamentos de um usuário específico"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    h.id,
                    h.agendamento_id,
                    h.type,
                    h.name,
                    h.historico_date,
                    h.start_time,
                    h.end_time,
                    h.purpose,
                    h.status,
                FROM historico h
                WHERE h.user_id = %s
                ORDER BY h.historico_date DESC, h.start_time DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_tipo(tipo):
        """Lista histórico filtrado por tipo (ambiente ou equipamento)"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                WHERE h.type = %s
                ORDER BY h.historico_date DESC, h.start_time DESC
            """, (tipo,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_status(status):
        """Lista histórico filtrado por status"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                WHERE h.status = %s
                ORDER BY h.historico_date DESC, h.start_time DESC
            """, (status,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_periodo(data_inicio, data_fim):
        """Lista histórico em um período específico"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                WHERE h.historico_date BETWEEN %s AND %s
                ORDER BY h.historico_date DESC, h.start_time DESC
            """, (data_inicio, data_fim))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(id, status):
        """Atualiza o status de um registro do histórico pelo agendamento_id"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico
                SET status = %s
                WHERE agendamento_id = %s
            """, (status, id))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status_por_id(historico_id, status):
        """Atualiza o status de um registro específico do histórico pelo ID do histórico"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico
                SET status = %s
                WHERE id = %s
            """, (status, historico_id))

            if cursor.rowcount == 0:
                raise ValueError("Registro não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cancelar(historico_id, user_id):
        """Cancela um registro do histórico (verifica permissão do usuário)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico
                SET status = 'cancelado'
                WHERE id = %s AND user_id = %s
            """, (historico_id, user_id))

            if cursor.rowcount == 0:
                raise ValueError("Registro não encontrado ou sem permissão")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(historico_id):
        """Remove um registro do histórico"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM historico
                WHERE id = %s
            """, (historico_id,))

            if cursor.rowcount == 0:
                raise ValueError("Registro não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_status(user_id=None):
        """Conta registros do histórico por status"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    status,
                    COUNT(*) as total
                FROM historico
            """
            
            params = []
            if user_id:
                query += " WHERE user_id = %s"
                params.append(user_id)
            
            query += " GROUP BY status"
            
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            
            return {r['status']: r['total'] for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_tipo(user_id=None):
        """Conta registros do histórico por tipo"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    type,
                    COUNT(*) as total
                FROM historico
            """
            
            params = []
            if user_id:
                query += " WHERE user_id = %s"
                params.append(user_id)
            
            query += " GROUP BY type"
            
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            
            return {r['type']: r['total'] for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        """Busca no histórico por nome do ambiente/equipamento, usuário ou finalidade"""
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
                    u.name as usuario_nome,
                    u.email as usuario_email
                FROM historico h
                INNER JOIN users u ON h.user_id = u.id
                WHERE h.name LIKE %s
                   OR u.name LIKE %s
                   OR h.purpose LIKE %s
                ORDER BY h.historico_date DESC, h.start_time DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()