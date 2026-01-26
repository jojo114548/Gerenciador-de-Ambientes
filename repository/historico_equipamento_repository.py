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
    def buscar_por_id(historico_id):
        """Busca um registro específico do histórico por ID"""
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
                    u.email as usuario_email,
                    u.departamento,
                    e.categoria as equipamento_categoria,
                    e.marca as equipamento_marca,
                    e.modelo as equipamento_modelo
                FROM historico_equipamentos he
                INNER JOIN users u ON he.user_id = u.id
                LEFT JOIN equipamentos e ON he.equipamento_id = e.id
                WHERE he.id = %s
            """, (historico_id,))
            
            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        """Lista histórico de equipamentos de um usuário específico"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.equipamento_id,
                    he.equipamento_nome,
                    he.data_equip,
                    he.hora_inicio,
                    he.hora_fim,
                    he.finalidade,
                    he.status,
                    e.categoria as equipamento_categoria,
                    e.image as equipamento_image
                FROM historico_equipamentos he
                LEFT JOIN equipamentos e ON he.equipamento_id = e.id
                WHERE he.user_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_equipamento(equipamento_id):
        """Lista histórico de um equipamento específico"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
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
                WHERE he.equipamento_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (equipamento_id,))

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
                WHERE he.status = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
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
                WHERE he.data_equip BETWEEN %s AND %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
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
                UPDATE historico_equipamentos
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
                UPDATE historico_equipamentos
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
    def cancelar(historico_equipamentos_id, user_id):
        """Cancela um registro do histórico (verifica permissão do usuário)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE historico_equipamentos
                SET status = 'cancelado'
                WHERE id = %s AND user_id = %s
            """, (historico_equipamentos_id, user_id))

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
                DELETE FROM historico_equipamentos
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
    def contar_por_status(equipamento_id=None):
        """Conta registros do histórico por status"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    status,
                    COUNT(*) as total
                FROM historico_equipamentos
            """
            
            params = []
            if equipamento_id:
                query += " WHERE equipamento_id = %s"
                params.append(equipamento_id)
            
            query += " GROUP BY status"
            
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            
            return {r['status']: r['total'] for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        """Busca no histórico por nome de equipamento, usuário ou finalidade"""
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
                WHERE he.equipamento_nome LIKE %s
                   OR u.name LIKE %s
                   OR he.finalidade LIKE %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()