# 🚀 Nexus

Sistema web completo para gerenciamento de ambientes, equipamentos, eventos e agendamentos, desenvolvido com foco em boas práticas de arquitetura, organização de código e regras de negócio bem definidas.

Este projeto foi desenvolvido com Flask + PostgreSQL, adotando separação clara de responsabilidades (Controller, Service, Repository e Model),.


## 🎯 Objetivo do Projeto

* Evitar conflitos de agendamento
* Centralizar informações de uso
* Manter histórico e rastreabilidade
* Facilitar a gestão administrativa



## ✨ Principais Funcionalidades

### 👤 Usuários & Segurança

* Cadastro e autenticação de usuários
* Controle de acesso via JWT
* Separação de permissões (usuário / administrador)

### 🏢 Ambientes

* Cadastro, edição e exclusão de ambientes
* Visualização de disponibilidade
* Histórico de utilização

### 🧰 Equipamentos

* Gerenciamento completo de equipamentos
* Associação de equipamentos a ambientes
* Controle de uso e histórico

### 📅 Agendamentos

* Agendamento de ambientes e equipamentos
* Validação de conflitos de horários


### 🎉 Eventos

* Criação e gerenciamento de eventos
* Associação com ambientes e recursos

### 🔔 Notificações

* Sistema de notificações internas
* Alertas relacionados a eventos e agendamentos



## 🧱 Arquitetura e Organização

O projeto segue uma arquitetura em camadas, facilitando manutenção, testes e evolução.

```
Gerenciador-de-Ambientes-mysql/
│
├── app.py                  # Ponto de entrada da aplicação
├── controller/             # Rotas e controllers (HTTP)
├── service/                # Regras de negócio
├── repository/             # Acesso ao banco de dados (MySQL)
├── model/                  # Modelos e entidades
├── templates/              # Templates HTML (Jinja2)
│   └── modais/             # Componentes reutilizáveis
├── static/                 # CSS, JS e assets
  






