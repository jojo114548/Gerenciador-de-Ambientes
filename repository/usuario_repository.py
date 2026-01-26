import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class UsuarioRepository:

    @staticmethod
    def listar():
        """Lista todos os usuários"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, created_at
                FROM users
                ORDER BY name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(user_id):
        """Busca um usuário específico por ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, created_at, updated_at
                FROM users
                WHERE id = %s
            """, (user_id,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        """Busca um usuário por email (com senha para autenticação)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * 
                FROM users 
                WHERE email = %s
            """, (email,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca um usuário por CPF"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, created_at
                FROM users
                WHERE cpf = %s
            """, (cpf,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def adicionar(users):
        """Adiciona um novo usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, senha
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                users.id,
                users.name,
                users.email,
                users.cpf,
                users.rg,
                users.data_nascimento,
                users.telefone,
                users.endereco,
                users.departamento,
                users.funcao,
                users.role,
                users.image,
                users.status,
                users.senha
            ))

            conn.commit()
            return users.id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar(id, dados):
        """Atualiza dados de um usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET name = %s,
                    email = %s,
                    cpf = %s,
                    rg = %s,
                    data_nascimento = %s,
                    telefone = %s,
                    endereco = %s,
                    departamento = %s,
                    funcao = %s,
                    role = %s,
                    image = %s,
                    status = %s
                WHERE id = %s
            """, (
                dados["name"],
                dados["email"],
                dados["cpf"],
                dados.get("rg"),
                dados.get("data_nascimento"),
                dados.get("telefone"),
                dados.get("endereco"),
                dados.get("departamento"),
                dados.get("funcao"),
                dados["role"],
                dados.get("image"),
                dados["status"],
                id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Usuário não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_senha(usuario_id, senha):
        """Atualiza a senha de um usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET senha = %s
                WHERE id = %s
            """, (senha, usuario_id))

            if cursor.rowcount == 0:
                raise ValueError("Usuário não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(usuario_id, status):
        """Atualiza o status de um usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET status = %s
                WHERE id = %s
            """, (status, usuario_id))

            if cursor.rowcount == 0:
                raise ValueError("Usuário não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(usuario_id):
        """Remove um usuário (CASCADE deleta dependências automaticamente)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM users WHERE id = %s
            """, (usuario_id,))

            if cursor.rowcount == 0:
                raise ValueError("Usuário não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        """Busca usuários por nome, email ou CPF"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, telefone,
                    departamento, funcao, role, status, image
                FROM users
                WHERE name LIKE %s
                   OR email LIKE %s
                   OR cpf LIKE %s
                ORDER BY name
                LIMIT 20
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_role(role):
        """Lista usuários filtrados por role (admin ou user)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, telefone,
                    departamento, funcao, role, status, image, created_at
                FROM users
                WHERE role = %s
                ORDER BY name
            """, (role,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_status(status):
        """Lista usuários filtrados por status (ativo ou inativo)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, telefone,
                    departamento, funcao, role, status, image, created_at
                FROM users
                WHERE status = %s
                ORDER BY name
            """, (status,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_departamento(departamento):
        """Lista usuários filtrados por departamento"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, telefone,
                    departamento, funcao, role, status, image
                FROM users
                WHERE departamento = %s
                ORDER BY name
            """, (departamento,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def email_existe(email, excluir_id=None):
        """Verifica se email já está cadastrado"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT 1 FROM users WHERE email = %s"
            params = [email]
            
            if excluir_id:
                query += " AND id != %s"
                params.append(excluir_id)
            
            query += " LIMIT 1"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cpf_existe(cpf, excluir_id=None):
        """Verifica se CPF já está cadastrado"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT 1 FROM users WHERE cpf = %s"
            params = [cpf]
            
            if excluir_id:
                query += " AND id != %s"
                params.append(excluir_id)
            
            query += " LIMIT 1"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_role():
        """Conta usuários por role"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    role,
                    COUNT(*) as total
                FROM users
                GROUP BY role
            """)

            resultados = cursor.fetchall()
            return {r['role']: r['total'] for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_status():
        """Conta usuários por status"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    status,
                    COUNT(*) as total
                FROM users
                GROUP BY status
            """)

            resultados = cursor.fetchall()
            return {r['status']: r['total'] for r in resultados}

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_admins():
        """Lista apenas usuários administradores"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, telefone, departamento, 
                    funcao, status, image, created_at
                FROM users
                WHERE role = 'admin'
                ORDER BY name
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_ativos():
        """Lista apenas usuários ativos"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, telefone,
                    departamento, funcao, role, image
                FROM users
                WHERE status = 'ativo'
                ORDER BY name
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()