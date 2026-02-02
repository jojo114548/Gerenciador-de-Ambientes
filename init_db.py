"""
Script de inicialização do banco de dados PostgreSQL
Baseado no dump fornecido - Database: nexus
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_db_connection():
    """Estabelece conexão com o PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'postgres')
    )

def create_schema_and_types(cursor):
    """Cria o schema e tipos customizados"""
    
    # Criar schema
    cursor.execute("CREATE SCHEMA IF NOT EXISTS nexus;")
    
    # Criar tipos ENUM
    types_sql = [
        """
        DO $$ BEGIN
            CREATE TYPE nexus.role_usuario AS ENUM ('admin', 'user');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_agendamento AS ENUM ('pendente', 'confirmado', 'rejeitado', 'cancelado');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_agendamento_eq AS ENUM ('pendente', 'Confirmado', 'Rejeitado');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_ambiente AS ENUM ('Disponivel', 'ocupado', 'manutencao');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_equipamento AS ENUM ('Disponivel', 'ocupado');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_historico AS ENUM ('Confirmado', 'Rejeitado', 'Concluido', 'Cancelado');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_historico_eq AS ENUM ('Confirmado', 'Rejeitado', 'Concluido', 'Cancelado');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.status_usuario AS ENUM ('ativo', 'inativo');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.tipo_ambiente AS ENUM ('sala', 'laboratorio', 'auditorio', 'estudio');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.tipo_evento AS ENUM ('workshop', 'hackathon', 'palestra', 'outro');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """,
        """
        DO $$ BEGIN
            CREATE TYPE nexus.tipo_notificacao AS ENUM ('info', 'aviso', 'sucesso');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """
    ]
    
    for type_sql in types_sql:
        cursor.execute(type_sql)

def create_tables(cursor):
    """Cria todas as tabelas do banco de dados"""
    
    tables_sql = [
        # Tabela users
        """
        CREATE TABLE IF NOT EXISTS nexus.users (
            id UUID PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            cpf VARCHAR(14) NOT NULL,
            rg VARCHAR(20),
            data_nascimento DATE,
            telefone VARCHAR(20),
            endereco VARCHAR(255),
            departamento VARCHAR(100),
            funcao VARCHAR(100),
            role nexus.role_usuario DEFAULT 'user' NOT NULL,
            image VARCHAR(255),
            status nexus.status_usuario DEFAULT 'ativo' NOT NULL,
            senha VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela ambientes
        """
        CREATE TABLE IF NOT EXISTS nexus.ambientes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            type nexus.tipo_ambiente NOT NULL,
            capacidade INTEGER NOT NULL,
            status nexus.status_ambiente DEFAULT 'Disponivel',
            descricao TEXT,
            localizacao VARCHAR(50),
            area VARCHAR(20),
            image VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela agendamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.agendamentos (
            id SERIAL PRIMARY KEY,
            ambiente_id INTEGER NOT NULL REFERENCES nexus.ambientes(id) ON DELETE CASCADE,
            data DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            finalidade TEXT,
            status nexus.status_agendamento DEFAULT 'pendente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela equipamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.equipamentos (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            status nexus.status_equipamento DEFAULT 'Disponivel',
            descricao TEXT,
            marca VARCHAR(50),
            modelo VARCHAR(100),
            condicao VARCHAR(30),
            image VARCHAR(255),
            quantidade_disponivel INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela equipamentos_especificacoes
        """
        CREATE TABLE IF NOT EXISTS nexus.equipamentos_especificacoes (
            id SERIAL PRIMARY KEY,
            equipamento_id INTEGER NOT NULL REFERENCES nexus.equipamentos(id) ON DELETE CASCADE,
            especificacao VARCHAR(255) NOT NULL
        );
        """,
        
        # Tabela eventos
        """
        CREATE TABLE IF NOT EXISTS nexus.eventos (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(150) NOT NULL,
            data_evento DATE NOT NULL,
            hora_evento TIME NOT NULL,
            localizacao VARCHAR(150) NOT NULL,
            descricao TEXT,
            participantes INTEGER DEFAULT 0,
            capacidade INTEGER NOT NULL,
            instrutor VARCHAR(100),
            tipo nexus.tipo_evento NOT NULL,
            image VARCHAR(255),
            ambiente_id INTEGER REFERENCES nexus.ambientes(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela eventos_equipamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.eventos_equipamentos (
            id SERIAL PRIMARY KEY,
            evento_id INTEGER REFERENCES nexus.eventos(id) ON DELETE CASCADE,
            equipamento_id INTEGER REFERENCES nexus.equipamentos(id),
            quantidade INTEGER DEFAULT 1,
            UNIQUE(evento_id, equipamento_id)
        );
        """,
        
        # Tabela notificacoes
        """
        CREATE TABLE IF NOT EXISTS nexus.notificacoes (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES nexus.users(id) ON DELETE CASCADE,
            titulo VARCHAR(100) NOT NULL,
            mensagem VARCHAR(255) NOT NULL,
            tipo nexus.tipo_notificacao DEFAULT 'info',
            lida BOOLEAN DEFAULT FALSE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela historico
        """
        CREATE TABLE IF NOT EXISTS nexus.historico (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES nexus.users(id) ON DELETE CASCADE,
            agendamento_id INTEGER NOT NULL REFERENCES nexus.agendamentos(id) ON DELETE CASCADE,
            type VARCHAR(20),
            name VARCHAR(100),
            historico_date DATE,
            start_time TIME,
            end_time TIME,
            purpose TEXT,
            status nexus.status_historico NOT NULL
        );
        """,
        
        # Tabela pendentes_ambientes
        """
        CREATE TABLE IF NOT EXISTS nexus.pendentes_ambientes (
            id SERIAL PRIMARY KEY,
            agendamento_id INTEGER NOT NULL UNIQUE REFERENCES nexus.agendamentos(id) ON DELETE CASCADE,
            user_id UUID NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela agendamentos_equipamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.agendamentos_equipamentos (
            id SERIAL PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES nexus.users(id) ON DELETE CASCADE,
            equipamento_id INTEGER NOT NULL REFERENCES nexus.equipamentos(id) ON DELETE CASCADE,
            data DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            finalidade VARCHAR(255),
            status VARCHAR(20) DEFAULT 'Pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela historico_equipamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.historico_equipamentos (
            id SERIAL PRIMARY KEY,
            agendamento_id INTEGER NOT NULL REFERENCES nexus.agendamentos_equipamentos(id) ON DELETE CASCADE,
            equipamento_id INTEGER NOT NULL REFERENCES nexus.equipamentos(id) ON DELETE CASCADE,
            user_id UUID NOT NULL,
            equipamento_nome VARCHAR(255) NOT NULL,
            data_equip DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            finalidade VARCHAR(255) NOT NULL,
            status nexus.status_historico NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela pendentes_equipamentos
        """
        CREATE TABLE IF NOT EXISTS nexus.pendentes_equipamentos (
            id SERIAL PRIMARY KEY,
            agendamento_id INTEGER NOT NULL UNIQUE REFERENCES nexus.agendamentos_equipamentos(id) ON DELETE CASCADE,
            user_id UUID NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela inscricoes_eventos
        """
        CREATE TABLE IF NOT EXISTS nexus.inscricoes_eventos (
            id SERIAL PRIMARY KEY,
            evento_id INTEGER NOT NULL REFERENCES nexus.eventos(id) ON DELETE CASCADE,
            user_id UUID NOT NULL REFERENCES nexus.users(id) ON DELETE CASCADE,
            status VARCHAR(20) DEFAULT 'Inscrito',
            data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(evento_id, user_id)
        );
        """,
        
        # Tabela recursos_ambientes
        """
        CREATE TABLE IF NOT EXISTS nexus.recursos_ambientes (
            id SERIAL PRIMARY KEY,
            recursos_id INTEGER NOT NULL REFERENCES nexus.ambientes(id) ON DELETE CASCADE,
            recursos VARCHAR(255) NOT NULL
        );
        """
    ]
    
    for table_sql in tables_sql:
        cursor.execute(table_sql)

def create_indexes(cursor):
    """Cria índices para otimização de queries"""
    
    indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_agendamento_data ON nexus.agendamentos(data);",
        "CREATE INDEX IF NOT EXISTS idx_agendamento_status ON nexus.agendamentos(status);",
        "CREATE INDEX IF NOT EXISTS idx_historico_user ON nexus.historico(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_historico_agendamento ON nexus.historico(agendamento_id);"
    ]
    
    for index_sql in indexes_sql:
        cursor.execute(index_sql)

def create_functions_and_triggers(cursor):
    """Cria funções e triggers"""
    
    # Função para criar histórico de equipamentos
    cursor.execute("""
        CREATE OR REPLACE FUNCTION nexus.fn_criar_historico_equipamento()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Inserir no histórico apenas quando status for Confirmado, Rejeitado ou Cancelado
            IF NEW.status IN ('Confirmado', 'Rejeitado', 'Cancelado') AND 
               (OLD.status IS NULL OR OLD.status != NEW.status) THEN
                
                INSERT INTO nexus.historico_equipamentos (
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
                SELECT 
                    ae.id,
                    ae.equipamento_id,
                    ae.user_id,
                    e.name,
                    ae.data,
                    ae.hora_inicio,
                    ae.hora_fim,
                    ae.finalidade,
                    NEW.status::nexus.status_historico
                FROM nexus.agendamentos_equipamentos ae
                JOIN nexus.equipamentos e ON ae.equipamento_id = e.id
                WHERE ae.id = NEW.agendamento_id;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Trigger para histórico de equipamentos
    cursor.execute("""
        DROP TRIGGER IF EXISTS trg_historico_equipamento ON nexus.pendentes_equipamentos;
        
        CREATE TRIGGER trg_historico_equipamento
        AFTER UPDATE ON nexus.pendentes_equipamentos
        FOR EACH ROW
        EXECUTE FUNCTION nexus.fn_criar_historico_equipamento();
    """)

def init_database():
    """Função principal para inicializar o banco de dados"""
    
    conn = None
    cursor = None
    
    try:
        # Conectar ao banco
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("🔄 Iniciando configuração do banco de dados...")
        
        # Criar schema e tipos
        print("📝 Criando schema e tipos customizados...")
        create_schema_and_types(cursor)
        
        # Criar tabelas
        print("📊 Criando tabelas...")
        create_tables(cursor)
        
        # Criar índices
        print("🔍 Criando índices...")
        create_indexes(cursor)
        
        # Criar funções e triggers
        print("⚙️  Criando funções e triggers...")
        create_functions_and_triggers(cursor)
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("ℹ️  Schema: nexus")
        print("ℹ️  Todas as tabelas, tipos, índices e triggers foram criados.")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()