"""
Script para limpar dados de exemplo do banco de dados
Útil para resetar os dados sem reinicializar toda a estrutura
"""

import psycopg2
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

def clear_all_data(cursor):
    """Remove todos os dados das tabelas mantendo a estrutura"""
    print("🗑️  Removendo todos os dados...")
    
    # Ordem correta para respeitar foreign keys
    tables = [
        'nexus.inscricoes_eventos',
        'nexus.notificacoes',
        'nexus.historico_equipamentos',
        'nexus.historico',
        'nexus.pendentes_equipamentos',
        'nexus.pendentes_ambientes',
        'nexus.agendamentos_equipamentos',
        'nexus.agendamentos',
        'nexus.eventos_equipamentos',
        'nexus.eventos',
        'nexus.equipamentos_especificacoes',
        'nexus.equipamentos',
        'nexus.recursos_ambientes',
        'nexus.ambientes',
        'nexus.users'
    ]
    
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
        print(f"  ✅ {table} limpa")

def clear_specific_tables(cursor, tables_to_clear):
    """Remove dados apenas de tabelas específicas"""
    print(f"🗑️  Removendo dados de tabelas específicas...")
    
    for table in tables_to_clear:
        try:
            cursor.execute(f"TRUNCATE TABLE nexus.{table} CASCADE")
            print(f"  ✅ nexus.{table} limpa")
        except Exception as e:
            print(f"  ❌ Erro ao limpar nexus.{table}: {e}")

def reset_sequences(cursor):
    """Reseta as sequences (auto increment) para começar do 1"""
    print("🔄 Resetando sequences...")
    
    sequences = [
        'nexus.agendamentos_id_seq',
        'nexus.agendamentos_equipamentos_id_seq',
        'nexus.ambientes_id_seq',
        'nexus.equipamentos_especificacoes_id_seq',
        'nexus.equipamentos_id_seq',
        'nexus.eventos_equipamentos_id_seq',
        'nexus.eventos_id_seq',
        'nexus.historico_equipamentos_id_seq',
        'nexus.historico_id_seq',
        'nexus.inscricoes_eventos_id_seq',
        'nexus.notificacoes_id_seq',
        'nexus.pendentes_ambientes_id_seq',
        'nexus.pendentes_equipamentos_id_seq',
        'nexus.recursos_ambientes_id_seq'
    ]
    
    for sequence in sequences:
        try:
            cursor.execute(f"ALTER SEQUENCE {sequence} RESTART WITH 1")
            print(f"  ✅ {sequence} resetada")
        except Exception as e:
            print(f"  ⚠️  {sequence}: {e}")

def show_menu():
    """Mostra menu de opções"""
    print("\n" + "=" * 60)
    print("🧹 LIMPEZA DE DADOS DO BANCO - Sistema Nexus")
    print("=" * 60)
    print("\nEscolha uma opção:")
    print("1. Limpar TODOS os dados (mantém estrutura)")
    print("2. Limpar apenas dados de teste/exemplo")
    print("3. Limpar tabelas específicas")
    print("4. Resetar sequences (auto increment)")
    print("5. Sair")
    print("\n⚠️  ATENÇÃO: Esta operação NÃO pode ser desfeita!")
    return input("\nOpção: ")

def confirm_action(message):
    """Solicita confirmação do usuário"""
    response = input(f"\n⚠️  {message} (digite 'SIM' para confirmar): ")
    return response.upper() == 'SIM'

def clear_database():
    """Função principal"""
    
    conn = None
    cursor = None
    
    try:
        # Conectar ao banco
        conn = get_db_connection()
        cursor = conn.cursor()
        
        while True:
            option = show_menu()
            
            if option == '1':
                if confirm_action("Deseja realmente LIMPAR TODOS OS DADOS?"):
                    clear_all_data(cursor)
                    reset_sequences(cursor)
                    conn.commit()
                    print("\n✅ Todos os dados foram removidos com sucesso!")
                    
                    # Mostrar estatísticas
                    print("\n📊 Verificação:")
                    tables = ['users', 'ambientes', 'equipamentos', 'eventos', 'notificacoes']
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM nexus.{table}")
                        count = cursor.fetchone()[0]
                        print(f"  {table}: {count} registros")
                else:
                    print("❌ Operação cancelada")
            
            elif option == '2':
                if confirm_action("Deseja limpar apenas dados de teste?"):
                    # Limpa tudo exceto estrutura
                    clear_all_data(cursor)
                    conn.commit()
                    print("\n✅ Dados de teste removidos!")
                else:
                    print("❌ Operação cancelada")
            
            elif option == '3':
                print("\nTabelas disponíveis:")
                print("  - users")
                print("  - ambientes")
                print("  - equipamentos")
                print("  - eventos")
                print("  - notificacoes")
                print("  - agendamentos")
                print("  - historico")
                print("  - inscricoes_eventos")
                
                tables_input = input("\nDigite as tabelas separadas por vírgula: ")
                tables = [t.strip() for t in tables_input.split(',')]
                
                if confirm_action(f"Deseja limpar: {', '.join(tables)}?"):
                    clear_specific_tables(cursor, tables)
                    conn.commit()
                    print("\n✅ Tabelas selecionadas foram limpas!")
                else:
                    print("❌ Operação cancelada")
            
            elif option == '4':
                if confirm_action("Deseja resetar as sequences?"):
                    reset_sequences(cursor)
                    conn.commit()
                    print("\n✅ Sequences resetadas!")
                else:
                    print("❌ Operação cancelada")
            
            elif option == '5':
                print("\n👋 Saindo...")
                break
            
            else:
                print("\n❌ Opção inválida!")
            
            input("\nPressione ENTER para continuar...")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n❌ Erro: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 Script de Limpeza do Banco de Dados")
    print("⚠️  CUIDADO: Este script remove dados permanentemente!\n")
    
    if confirm_action("Deseja continuar?"):
        clear_database()
    else:
        print("\n❌ Operação cancelada pelo usuário")