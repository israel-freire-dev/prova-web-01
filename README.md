# 🏢 GestorPro

Sistema de gestão empresarial desenvolvido em **Django**, voltado para o controle de **Clientes**, **Produtos**, **Fornecedores** e **Ordens de Compra** com controle de estoque baseado em entrega.

---

## 📋 Funcionalidades

### Módulos do Sistema

- **Clientes** — Cadastro completo com CPF, endereço, contato e observações
- **Produtos** — Gestão de catálogo com controle de estoque e vínculo com fornecedor
- **Fornecedores** — Cadastro de fornecedores com CNPJ e dados de contato
- **Ordens de Compra** — Fluxo completo de compras com controle de status e entrega

### Fluxo de Ordens de Compra

```
RASCUNHO → CONFIRMADA → ENTREGUE → (CANCELADA com estorno)
                ↓                         
            CANCELADA (sem alterar estoque)
```

- **Rascunho**: Criação e edição da ordem com seleção de fornecedor e produtos
- **Confirmada**: Ordem aprovada, aguardando entrega (estoque não é alterado)
- **Entregue**: Produtos recebidos — **estoque atualizado automaticamente**
- **Cancelada**: Se cancelada após entrega, o estoque é estornado

### Outros Recursos

- 🔐 **Autenticação** — Login, cadastro de usuário e proteção de rotas
- 📊 **Dashboard** — Painel com métricas em tempo real e alertas de estoque baixo
- 🔄 **API REST** — Endpoints públicos completos (CRUD) para todos os módulos
- 📖 **Swagger** — Documentação interativa das APIs

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| **Python** | 3.14 | Linguagem principal |
| **Django** | 6.0.2 | Framework web |
| **Django REST Framework** | 3.16 | APIs REST |
| **drf-spectacular** | 0.29 | Documentação Swagger/OpenAPI |
| **SQLite** | — | Banco de dados (desenvolvimento) |
| **Tailwind CSS** | CDN | Estilização da interface |

---

## 📖 Documentação da API

Com o servidor rodando, acesse:

| URL | Descrição |
|---|---|
| `/api/docs/` | **Swagger UI** — Interface interativa para testar as APIs |
| `/api/redoc/` | **ReDoc** — Documentação visual alternativa |
| `/api/schema/` | **OpenAPI Schema** — Schema em YAML |

### Endpoints disponíveis

Os endpoints são agrupados por módulo no Swagger:

- **Clientes**: `GET/POST/PUT/DELETE` em `/public/clientes/`
- **Produtos**: `GET/POST/PUT/DELETE` em `/public/produtos/`
- **Fornecedores**: `GET/POST/PUT/DELETE` em `/public/fornecedores/`
- **Ordens de Compra**: `GET` listagem, `POST` confirmar/cancelar/confirmar-entrega em `/public/compras/`

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/israel-freire-dev/prova-web-01.git
cd prova-web-01

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações do banco de dados
python manage.py migrate

# 5. Crie um superusuário (opcional, para acessar o admin)
python manage.py createsuperuser

# 6. Inicie o servidor de desenvolvimento
python manage.py runserver
```

### Acessos

| URL | Descrição |
|---|---|
| `http://127.0.0.1:8000/` | Página principal (requer login) |
| `http://127.0.0.1:8000/login/` | Tela de login |
| `http://127.0.0.1:8000/cadastro/` | Cadastro de novo usuário |
| `http://127.0.0.1:8000/admin/` | Painel administrativo Django |
| `http://127.0.0.1:8000/api/docs/` | Documentação Swagger |

---

## 📁 Estrutura do Projeto

```
prova-web-01/
├── core/             # Configurações, URLs principais, views de auth
├── clientes/         # App de gestão de clientes
├── produtos/         # App de gestão de produtos
├── fornecedores/     # App de gestão de fornecedores
├── compras/          # App de ordens de compra e controle de estoque
├── templates/        # Templates HTML (Tailwind CSS)
│   ├── componentes/  # Componentes reutilizáveis (sidebar)
│   ├── core/         # Login, cadastro, dashboard
│   ├── clientes/     # Templates de clientes
│   ├── produtos/     # Templates de produtos
│   ├── fornecedores/ # Templates de fornecedores
│   └── compras/      # Templates de ordens de compra
├── manage.py
└── db.sqlite3
```
