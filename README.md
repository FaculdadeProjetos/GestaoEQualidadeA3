# 🌱 Sistema de Gestão de Usuários e Controle de Irrigação

Este projeto é um sistema web desenvolvido com **Flask**, **MySQL** e **Docker**, destinado à **gestão de usuários** e **controle automatizado de irrigação**, com arquitetura modular e boas práticas de desenvolvimento.

## 📦 Tecnologias Utilizadas

- **Backend:** Python 3.10+, Flask
- **Banco de Dados:** MySQL 8.0
- **Ambiente:** Docker, Docker Compose
- **Padrões:** Factory Pattern, Repository Pattern, Blueprints
- **Segurança:** CSRF, senhas hash (Werkzeug), sessões seguras

## 🏗️ Estrutura do Projeto

```
GestaoEQualidadeA3/
├── app/
│   ├── auth/                # Autenticação
│   ├── irrigation/          # Controle de irrigação
│   ├── users/               # Gerenciamento de usuários
│   ├── models/              # Modelos de dados
│   ├── templates/           # Jinja2 templates
│   └── core/                # Extensões e configurações Flask
├── config.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── init.sql
└── env.example
```

## 🚀 Como Executar

### ✅ Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.10+ (para execução local)

### 🔧 Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/FaculdadeProjetos/GestaoEQualidadeA3.git
   cd GestaoEQualidadeA3
   ```

2. Copie e configure o arquivo `.env`:
   ```bash
   cp env.example .env
   ```

3. Execute com Docker:
   ```bash
   docker-compose up --build
   ```

Ou, para execução local:

```bash
pip install -r requirements.txt
flask run --debug
```

## 🗄️ Banco de Dados

- Host: `localhost`
- Porta: `3307`
- Usuário: `user`
- Senha: `password` (configurável no `.env`)
- Banco: `user_management`

**Tabelas:**
- `users`: usuários do sistema
- `irrigation_controllers`: dados de controle de irrigação

## ⚙️ Funcionalidades

### 👤 Gestão de Usuários
- Registro, login e logout
- Sessões autenticadas
- Visualização e edição de perfil

### 💧 Controle de Irrigação
- Monitoramento de umidade
- Histórico de irrigações
- Ativação manual e automática de irrigação

## 🧱 Arquitetura & Boas Práticas

- **Factory Pattern**: criação modular da aplicação
- **Repository Pattern**: isolamento da lógica de dados
- **BluePrints**: rotas organizadas por domínio
- **Clean Code**: código limpo e comentado
- **Principais Princípios**: SOLID, DRY, SoC

## 🔐 Segurança

- Senhas hash com `Werkzeug`
- Proteção contra CSRF com `Flask-WTF`
- Validação de formulários
- Sessões seguras

## 🐳 Docker

- Multi-stage builds:
  - Dev: hot reload e debug
  - Prod: otimizado com Gunicorn
- Health checks e dependência de serviços (MySQL)

## 🧪 Testes e Manutenção

- Suporte a **type hints**
- Testes unitários (em progresso)
- Logging estruturado
- Tratamento de erros centralizado
- Documentação técnica em português

## 🤝 Contribuindo

1. Faça um fork
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a **licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais informações.