import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class EquipamentoRepository:

    @staticmethod
    def listar():
        """Lista todos os equipamentos com suas especificações"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    e.created_at,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.condicao, e.quantidade_disponivel, 
                         e.image, e.created_at
                ORDER BY e.name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(equipamento_id):
        """Busca um equipamento específico por ID com suas especificações"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    e.created_at,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                WHERE e.id = %s
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.condicao, e.quantidade_disponivel, 
                         e.image, e.created_at
            """, (equipamento_id,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_equipamento(dados):
        """Insere um novo equipamento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO equipamentos
                (name, categoria, status, descricao, marca, modelo, condicao, quantidade_disponivel, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["name"],
                dados["categoria"],
                dados.get("status", "Disponivel"),
                dados.get("descricao"),
                dados.get("marca"),
                dados.get("modelo"),
                dados.get("condicao"),
                dados.get("quantidade_disponivel", 1),
                dados.get("image")
            ))

            equipamento_id = cursor.lastrowid
            conn.commit()
            return equipamento_id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_especificacoes(equipamento_id, especificacoes):
        """Insere especificações para um equipamento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            for especificacao in especificacoes:
                if especificacao.strip():
                    cursor.execute("""
                        INSERT INTO equipamentos_especificacoes
                        (equipamento_id, especificacao)
                        VALUES (%s, %s)
                    """, (equipamento_id, especificacao.strip()))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_equipamento(equipamento):
        """Atualiza dados de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE equipamentos
                SET name = %s,
                    categoria = %s,
                    status = %s,
                    descricao = %s,
                    marca = %s,
                    modelo = %s,
                    condicao = %s,
                    quantidade_disponivel = %s,
                    image = %s
                WHERE id = %s
            """, (
                equipamento.name,
                equipamento.categoria,
                equipamento.status,
                equipamento.descricao,
                equipamento.marca,
                equipamento.modelo,
                equipamento.condicao,
                equipamento.quantidade_disponivel,
                equipamento.image,
                equipamento.id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            # Remove especificações antigas
            cursor.execute("""
                DELETE FROM equipamentos_especificacoes
                WHERE equipamento_id = %s
            """, (equipamento.id,))

            # Insere novas especificações
            for especificacao in equipamento.especificacoes:
                if especificacao.strip():
                    cursor.execute("""
                        INSERT INTO equipamentos_especificacoes
                        (equipamento_id, especificacao)
                        VALUES (%s, %s)
                    """, (equipamento.id, especificacao.strip()))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_especificacoes(equipamento_id, especificacoes):
        """Atualiza as especificações de um equipamento (remove antigas e insere novas)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Remove especificações antigas
            cursor.execute("""
                DELETE FROM equipamentos_especificacoes
                WHERE equipamento_id = %s
            """, (equipamento_id,))

            # Insere novas especificações
            for especificacao in especificacoes:
                if especificacao.strip():
                    cursor.execute("""
                        INSERT INTO equipamentos_especificacoes
                        (equipamento_id, especificacao)
                        VALUES (%s, %s)
                    """, (equipamento_id, especificacao.strip()))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(equipamento_id, status):
        """Atualiza apenas o status de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, equipamento_id))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_quantidade(equipamento_id, quantidade_disponivel):
        """Atualiza a quantidade disponível de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE equipamentos
                SET quantidade_disponivel = %s
                WHERE id = %s
            """, (quantidade_disponivel, equipamento_id))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar_equipamento(equipamento_id):
        """Remove um equipamento (CASCADE remove especificações automaticamente)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM equipamentos WHERE id = %s
            """, (equipamento_id,))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        """Busca equipamentos por nome, categoria ou descrição"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id, 
                    e.name, 
                    e.categoria, 
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.quantidade_disponivel,
                    e.image,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                WHERE e.name LIKE %s 
                   OR e.categoria LIKE %s
                   OR e.descricao LIKE %s
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.quantidade_disponivel, e.image
                ORDER BY e.name
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_status(status):
        """Lista equipamentos filtrados por status"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                WHERE e.status = %s
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.condicao, e.quantidade_disponivel, e.image
                ORDER BY e.name
            """, (status,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_categoria(categoria):
        """Lista equipamentos filtrados por categoria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                WHERE e.categoria = %s
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.condicao, e.quantidade_disponivel, e.image
                ORDER BY e.name
            """, (categoria,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_disponiveis():
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    GROUP_CONCAT(es.especificacao SEPARATOR ' | ') AS especificacoes
                FROM equipamentos e
                LEFT JOIN equipamentos_especificacoes es ON e.id = es.equipamento_id
                WHERE e.status = 'Disponivel' AND e.quantidade_disponivel > 0
                GROUP BY e.id, e.name, e.categoria, e.status, e.descricao, 
                         e.marca, e.modelo, e.condicao, e.quantidade_disponivel, e.image
                ORDER BY e.name
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_status():
        """Conta quantos equipamentos existem por status"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    status,
                    COUNT(*) as total,
                    SUM(quantidade_disponivel) as quantidade_total
                FROM equipamentos
                GROUP BY status
            """)

            resultados = cursor.fetchall()
            return {r['status']: {'total': r['total'], 'quantidade': r['quantidade_total']} for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_categoria():
        """Conta quantos equipamentos existem por categoria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    categoria,
                    COUNT(*) as total,
                    SUM(quantidade_disponivel) as quantidade_total
                FROM equipamentos
                GROUP BY categoria
                ORDER BY categoria
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()