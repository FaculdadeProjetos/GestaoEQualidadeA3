# Sistema de Gestão e Qualidade A3

Sistema de gestão de usuários e controle de irrigação desenvolvido com Flask e MySQL.

## 🏗️ Estrutura do Projeto

```
GestaoEQualidadeA3/
├── app/
│   ├── __init__.py              # Application factory
│   ├── core/
│   │   └── extensions.py        # Flask extensions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── irrigation_controller.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py           # Authentication routes
│   │   └── forms.py            # Authentication forms
│   ├── users/
│   │   ├── __init__.py
│   │   └── routes.py           # User management routes
│   ├── irrigation/
│   │   ├── __init__.py
│   │   └── routes.py           # Irrigation control routes
│   └── templates/              # Jinja2 templates
├── config.py                   # Configuration settings
├── wsgi.py                     # WSGI entry point
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Docker image definition
├── init.sql                    # Database initialization
├── wait-for-db.sh             # Database wait script
└── env.example                # Environment variables example
```

## 🚀 Configuração e Execução

### Pré-requisitos

- Docker e Docker Compose
- Python 3.10+ (para desenvolvimento local)

### Configuração de Ambiente

1. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp env.example .env
```

2. Edite o arquivo `.env` com suas configurações:
```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DB_HOST=db
DB_PORT=3306
DB_NAME=user_management
DB_USER=user
DB_PASSWORD=password

# MySQL Root Password (for Docker)
MYSQL_ROOT_PASSWORD=root_password
```

### Execução com Docker

1. **Desenvolvimento:**
```bash
docker-compose up --build
```

2. **Produção:**
```bash
docker-compose -f docker-compose.yml up --build
```

A aplicação estará disponível em `http://localhost:5000`

### Execução Local (Desenvolvimento)

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente no arquivo `.env`

3. Execute a aplicação:
```bash
flask run --debug
```

## 🗄️ Banco de Dados

O sistema utiliza MySQL 8.0 com as seguintes tabelas:

- **users**: Gerenciamento de usuários
- **irrigation_controllers**: Controle de sistemas de irrigação

### Acesso ao Banco

- **Host**: localhost
- **Porta**: 3307 (mapeada do container)
- **Usuário**: user
- **Senha**: password (configurável via .env)
- **Database**: user_management

## 🔧 Funcionalidades

### Autenticação
- Login/Logout de usuários
- Registro de novos usuários
- Gerenciamento de sessões

### Gestão de Usuários
- Dashboard do usuário
- Perfil e configurações
- Listagem de usuários

### Controle de Irrigação
- Monitoramento de níveis de umidade
- Controle de sistemas de irrigação
- Histórico de irrigações

## 🏛️ Arquitetura

O projeto segue uma arquitetura modular baseada em:

- **Application Factory Pattern**: Criação flexível da aplicação Flask
- **Blueprint Pattern**: Organização modular das rotas
- **Repository Pattern**: Separação de modelos de dados
- **Configuration Management**: Gestão centralizada de configurações

### Princípios Aplicados

- **Clean Code**: Código limpo e bem documentado
- **Separation of Concerns**: Separação clara de responsabilidades
- **DRY (Don't Repeat Yourself)**: Reutilização de código
- **SOLID Principles**: Princípios de design orientado a objetos

## 🔒 Segurança

- Senhas hasheadas com Werkzeug
- Proteção CSRF com Flask-WTF
- Validação de formulários
- Gerenciamento seguro de sessões

## 🐳 Docker

### Multi-stage Build
O Dockerfile utiliza multi-stage builds para:
- **Development**: Hot reload e debugging
- **Production**: Imagem otimizada com Gunicorn

### Health Checks
- Verificação de saúde do banco MySQL
- Dependências entre serviços

## 📝 Desenvolvimento

### Estrutura de Código

- **Models**: `app/models/` - Definição de modelos de dados
- **Views**: `app/*/routes.py` - Lógica de rotas e views
- **Forms**: `app/*/forms.py` - Formulários e validações
- **Templates**: `app/templates/` - Templates Jinja2
- **Extensions**: `app/core/extensions.py` - Extensões Flask

### Boas Práticas

- Documentação em português para facilitar manutenção
- Type hints quando aplicável
- Testes unitários (em desenvolvimento)
- Logging estruturado
- Tratamento de erros

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 