import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, time
import os

def get_connection():
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no .env")
        
        print(f"Tentando conectar ao banco...") # remova em produção
        conn = psycopg2.connect(db_url)
        print("Conexão bem-sucedida!") # remova em produção
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

class AgendamentosRepository:

    @staticmethod
    def inserir(agendamento):
        """
        Insere um novo agendamento.
        agendamento = {
            'ambiente_id': 1,
            'data': date(2026, 2, 15),
            'hora_inicio': time(14, 0),
            'hora_fim': time(16, 0),
            'finalidade': 'Reunião',
            'status': 'pendente'  # opcional, default é 'pendente'
        }
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Validar campos obrigatórios
            campos_obrigatorios = ['ambiente_id', 'data', 'hora_inicio', 'hora_fim']
            for campo in campos_obrigatorios:
                if campo not in agendamento:
                    raise ValueError(f"Campo obrigatório ausente: {campo}")

            # Verificar conflito antes de inserir
            if AgendamentosRepository.existe_conflito(
                agendamento['ambiente_id'],
                agendamento['data'],
                agendamento['hora_inicio'],
                agendamento['hora_fim']
            ):
                raise ValueError("Já existe um agendamento neste horário")

            cursor.execute("""
                INSERT INTO nexus.agendamentos
                (ambiente_id, data, hora_inicio, hora_fim, finalidade, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                agendamento["ambiente_id"],
                agendamento["data"],
                agendamento["hora_inicio"],
                agendamento["hora_fim"],
                agendamento.get("finalidade"),
                agendamento.get("status", "pendente")
            ))

            agendamento_id = cursor.fetchone()[0]
            conn.commit()
            return agendamento_id

        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao inserir agendamento: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe_conflito(ambiente_id, data, hora_inicio, hora_fim, agendamento_id=None):
        """
        Verifica conflito de horário para ambiente.
        Retorna True se existe conflito, False caso contrário.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if agendamento_id:
                # Ao atualizar, ignora o próprio agendamento
                cursor.execute("""
                    SELECT 1
                    FROM nexus.agendamentos
                    WHERE ambiente_id = %s
                      AND data = %s
                      AND status NOT IN ('rejeitado', 'cancelado')
                      AND (
                          (hora_inicio < %s AND hora_fim > %s) OR
                          (hora_inicio < %s AND hora_fim > %s) OR
                          (hora_inicio >= %s AND hora_fim <= %s)
                      )
                      AND id != %s
                    LIMIT 1
                """, (
                    ambiente_id,
                    data,
                    hora_fim, hora_inicio,
                    hora_fim, hora_fim,
                    hora_inicio, hora_fim,
                    agendamento_id
                ))
            else:
                cursor.execute("""
                    SELECT 1
                    FROM nexus.agendamentos
                    WHERE ambiente_id = %s
                      AND data = %s
                      AND status NOT IN ('rejeitado', 'cancelado')
                      AND (
                          (hora_inicio < %s AND hora_fim > %s) OR
                          (hora_inicio < %s AND hora_fim > %s) OR
                          (hora_inicio >= %s AND hora_fim <= %s)
                      )
                    LIMIT 1
                """, (
                    ambiente_id,
                    data,
                    hora_fim, hora_inicio,
                    hora_fim, hora_fim,
                    hora_inicio, hora_fim
                ))

            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        """Lista todos os agendamentos com informações do ambiente"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.ambiente_id,
                    a.data,
                    a.hora_inicio,
                    a.hora_fim,
                    a.finalidade,
                    a.status,
                    a.created_at,
                    a.updated_at,
                    amb.name AS ambiente_nome,
                    amb.type AS ambiente_tipo,
                    amb.localizacao,
                    amb.capacidade
                FROM nexus.agendamentos a
                INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                ORDER BY a.data DESC, a.hora_inicio ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_pendentes():
        """Lista apenas agendamentos pendentes"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.ambiente_id,
                    a.data,
                    a.hora_inicio,
                    a.hora_fim,
                    a.finalidade,
                    a.status,
                    a.created_at,
                    amb.name AS ambiente_nome,
                    amb.type AS ambiente_tipo,
                    amb.localizacao,
                    pa.user_id,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.agendamentos a
                INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                LEFT JOIN nexus.pendentes_ambientes pa ON pa.agendamento_id = a.id
                LEFT JOIN nexus.users u ON pa.user_id = u.id
                WHERE a.status = 'pendente'
                ORDER BY a.created_at ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_confirmados():
        """Lista agendamentos confirmados"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.ambiente_id,
                    a.data,
                    a.hora_inicio,
                    a.hora_fim,
                    a.finalidade,
                    a.status,
                    a.created_at,
                    amb.name AS ambiente_nome,
                    amb.type AS ambiente_tipo,
                    amb.localizacao
                FROM nexus.agendamentos a
                INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                WHERE a.status = 'confirmado'
                  AND a.data >= CURRENT_DATE
                ORDER BY a.data ASC, a.hora_inicio ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(agendamento_id):
        """Busca um agendamento específico por ID"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.ambiente_id,
                    a.data,
                    a.hora_inicio,
                    a.hora_fim,
                    a.finalidade,
                    a.status,
                    a.created_at,
                    a.updated_at,
                    amb.name AS ambiente_nome,
                    amb.type AS ambiente_tipo,
                    amb.localizacao,
                    amb.capacidade,
                    amb.image AS ambiente_image
                FROM nexus.agendamentos a
                INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                WHERE a.id = %s
            """, (agendamento_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_ambiente(ambiente_id, data_inicio=None, data_fim=None):
        """Lista agendamentos de um ambiente específico"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if data_inicio and data_fim:
                cursor.execute("""
                    SELECT 
                        id, ambiente_id, data, hora_inicio, hora_fim,
                        finalidade, status, created_at
                    FROM nexus.agendamentos
                    WHERE ambiente_id = %s
                      AND data BETWEEN %s AND %s
                      AND status NOT IN ('rejeitado', 'cancelado')
                    ORDER BY data, hora_inicio
                """, (ambiente_id, data_inicio, data_fim))
            else:
                cursor.execute("""
                    SELECT 
                        id, ambiente_id, data, hora_inicio, hora_fim,
                        finalidade, status, created_at
                    FROM nexus.agendamentos
                    WHERE ambiente_id = %s
                      AND status NOT IN ('rejeitado', 'cancelado')
                    ORDER BY data, hora_inicio
                """, (ambiente_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_data(data):
        """Lista todos os agendamentos de uma data específica"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.ambiente_id,
                    a.data,
                    a.hora_inicio,
                    a.hora_fim,
                    a.finalidade,
                    a.status,
                    amb.name AS ambiente_nome,
                    amb.type AS ambiente_tipo,
                    amb.localizacao
                FROM nexus.agendamentos a
                INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                WHERE a.data = %s
                  AND a.status NOT IN ('rejeitado', 'cancelado')
                ORDER BY a.hora_inicio
            """, (data,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(agendamento_id, novo_status):
        """
        Atualiza o status de um agendamento.
        Status válidos: 'pendente', 'confirmado', 'rejeitado', 'cancelado'
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Validar status
            status_validos = ['pendente', 'confirmado', 'rejeitado', 'cancelado']
            if novo_status not in status_validos:
                raise ValueError(f"Status inválido. Use: {', '.join(status_validos)}")

            cursor.execute("""
                UPDATE nexus.agendamentos
                SET status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (novo_status, agendamento_id))

            if cursor.rowcount == 0:
                raise ValueError("Agendamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao atualizar status: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar(agendamento_id, agendamento):
        """
        Atualiza um agendamento existente.
        Verifica conflitos antes de atualizar.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Verificar se existe
            cursor.execute("SELECT 1 FROM nexus.agendamentos WHERE id = %s", (agendamento_id,))
            if not cursor.fetchone():
                raise ValueError("Agendamento não encontrado")

            # Verificar conflito se alterou data/horário
            if any(k in agendamento for k in ['data', 'hora_inicio', 'hora_fim', 'ambiente_id']):
                # Buscar dados atuais
                cursor.execute("""
                    SELECT ambiente_id, data, hora_inicio, hora_fim
                    FROM nexus.agendamentos WHERE id = %s
                """, (agendamento_id,))
                atual = cursor.fetchone()

                ambiente_id = agendamento.get('ambiente_id', atual[0])
                data = agendamento.get('data', atual[1])
                hora_inicio = agendamento.get('hora_inicio', atual[2])
                hora_fim = agendamento.get('hora_fim', atual[3])

                if AgendamentosRepository.existe_conflito(
                    ambiente_id, data, hora_inicio, hora_fim, agendamento_id
                ):
                    raise ValueError("Conflito de horário com outro agendamento")

            # Construir query dinamicamente
            campos = []
            valores = []
            
            campos_permitidos = ['ambiente_id', 'data', 'hora_inicio', 'hora_fim', 'finalidade', 'status']
            
            for campo in campos_permitidos:
                if campo in agendamento:
                    campos.append(f"{campo} = %s")
                    valores.append(agendamento[campo])

            if not campos:
                raise ValueError("Nenhum campo para atualizar")

            campos.append("updated_at = CURRENT_TIMESTAMP")
            valores.append(agendamento_id)

            query = f"UPDATE nexus.agendamentos SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(query, valores)

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao atualizar agendamento: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(agendamento_id):
        """Deleta um agendamento (se permitido)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Verificar se pode deletar (exemplo: apenas pendentes)
            cursor.execute("""
                SELECT status FROM nexus.agendamentos WHERE id = %s
            """, (agendamento_id,))
            
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Agendamento não encontrado")

            # Comentar esta validação se quiser permitir deletar qualquer status
            # if resultado[0] not in ['pendente', 'rejeitado']:
            #     raise ValueError("Apenas agendamentos pendentes ou rejeitados podem ser deletados")

            cursor.execute("DELETE FROM nexus.agendamentos WHERE id = %s", (agendamento_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Erro ao deletar agendamento: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def confirmar(agendamento_id):
        """Confirma um agendamento pendente"""
        AgendamentosRepository.atualizar_status(agendamento_id, 'confirmado')

    @staticmethod
    def rejeitar(agendamento_id):
        """Rejeita um agendamento pendente"""
        AgendamentosRepository.atualizar_status(agendamento_id, 'rejeitado')

    @staticmethod
    def cancelar(agendamento_id):
        """Cancela um agendamento"""
        AgendamentosRepository.atualizar_status(agendamento_id, 'cancelado')

    @staticmethod
    def listar_por_periodo(data_inicio, data_fim, status=None):
        """Lista agendamentos em um período"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if status:
                cursor.execute("""
                    SELECT 
                        a.id,
                        a.ambiente_id,
                        a.data,
                        a.hora_inicio,
                        a.hora_fim,
                        a.finalidade,
                        a.status,
                        amb.name AS ambiente_nome,
                        amb.type AS ambiente_tipo
                    FROM nexus.agendamentos a
                    INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                    WHERE a.data BETWEEN %s AND %s
                      AND a.status = %s
                    ORDER BY a.data, a.hora_inicio
                """, (data_inicio, data_fim, status))
            else:
                cursor.execute("""
                    SELECT 
                        a.id,
                        a.ambiente_id,
                        a.data,
                        a.hora_inicio,
                        a.hora_fim,
                        a.finalidade,
                        a.status,
                        amb.name AS ambiente_nome,
                        amb.type AS ambiente_tipo
                    FROM nexus.agendamentos a
                    INNER JOIN nexus.ambientes amb ON a.ambiente_id = amb.id
                    WHERE a.data BETWEEN %s AND %s
                    ORDER BY a.data, a.hora_inicio
                """, (data_inicio, data_fim))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_status(status):
        """Conta agendamentos por status"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM nexus.agendamentos WHERE status = %s
            """, (status,))

            return cursor.fetchone()[0]

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def estatisticas():
        """Retorna estatísticas gerais de agendamentos"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE status = 'pendente') as pendentes,
                    COUNT(*) FILTER (WHERE status = 'confirmado') as confirmados,
                    COUNT(*) FILTER (WHERE status = 'rejeitado') as rejeitados,
                    COUNT(*) FILTER (WHERE status = 'cancelado') as cancelados,
                    COUNT(*) as total
                FROM nexus.agendamentos
            """)

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()