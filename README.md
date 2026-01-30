# Gerenciador de Ambientes (Flask + MySQL)

Sistema web para gerenciamento de ambientes, equipamentos, eventos e agendamentos**, com controle de usuários, histórico e notificações. O projeto segue uma arquitetura organizada em Controllers, Services, Repositories e Models, utilizando Flask no backend e PostgreSQL como banco de dados.

## 🚀 Funcionalidades

* 👤 Autenticação e gestão de usuários
* 🏢 Cadastro e gerenciamento de ambientes
* 🧰 Cadastro e gerenciamento de equipamentos
* 📅 Agendamento de ambientes e equipamentos
* 🎉 Gestão de eventos
* 🔔 Sistema de notificações
* 🕓 Histórico de uso (ambientes e equipamentos)
* 🛠️ Painel administrativo

## 🧱 Arquitetura do Projeto

O projeto está organizado em camadas:

```
Gerenciador-de-Ambientes-mysql/
│
├── app.py                  # Arquivo principal da aplicação Flask
├── controller/             # Camada de controle (rotas/endpoints)
├── service/                # Regras de negócio
├── repository/             # Acesso a dados (MySQL)
├── model/                  # Modelos/entidades
├── templates/              # Templates HTML (Jinja2)
│   └── modais/             # Modais reutilizáveis
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
       


## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Flask**
* **Flask-JWT-Extended** (autenticação)
* **PostgreSQL**
* **HTML5 / CSS3 / JavaScript**
* **Jinja2** (templates)






