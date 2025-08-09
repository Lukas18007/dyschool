# Setup Rápido - Dyschool

Este guia te ajudará a configurar e executar o projeto Dyschool rapidamente.

## 🚀 Setup em 5 minutos

### 1. Pré-requisitos
- Python 3.8+ instalado
- pip instalado

### 2. Clone e Configure
```bash
# Clone o repositório (se aplicável)
# cd dyschool

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 3. Configure o Banco de Dados
```bash
# Crie as migrações
python manage.py makemigrations

# Aplique as migrações
python manage.py migrate

# Carregue dados iniciais (especialidades e temas)
python manage.py load_initial_data

# Crie um superusuário
python manage.py createsuperuser
```

### 4. Execute o Projeto
```bash
# Inicie o servidor
python manage.py runserver
```

### 5. Acesse a Aplicação
- **Site Principal**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 👥 Criando Usuários de Teste

### Aluno de Teste
1. Acesse http://localhost:8000/sign-up/
2. Preencha o formulário:
   - Username: `aluno_teste`
   - Email: `aluno@teste.com`
   - User Type: `Student`
   - Outros campos conforme necessário

### Professor de Teste
1. Acesse http://localhost:8000/sign-up/
2. Preencha o formulário:
   - Username: `professor_teste`
   - Email: `professor@teste.com`
   - User Type: `Teacher`
   - Outros campos conforme necessário
3. Após o cadastro, acesse http://localhost:8000/teacher/profile/
4. Configure especialidades, temas e valores

## 🎯 Testando o Fluxo

### Como Aluno:
1. Faça login como aluno
2. Vá para "Buscar Aulas"
3. Selecione especialidade e tema
4. Encontre professores disponíveis
5. Clique em "Solicitar Aula"
6. Preencha os detalhes da solicitação

### Como Professor:
1. Faça login como professor
2. Configure seu perfil (especialidades, valores)
3. Vá para o Dashboard
4. Veja solicitações de alunos
5. Clique em "Enviar Disponibilidade"
6. Defina data, horário e duração

### Como Aluno (novamente):
1. Vá para o Dashboard do Aluno
2. Veja as disponibilidades enviadas
3. Clique em "Aceitar" em uma disponibilidade
4. Confirme a aula

## 🔧 Comandos Úteis

```bash
# Verificar status das migrações
python manage.py showmigrations

# Resetar banco de dados (CUIDADO!)
python manage.py flush

# Criar novo comando de gerenciamento
python manage.py makemigrations core

# Executar testes
python manage.py test

# Shell do Django
python manage.py shell
```

## 🐛 Solução de Problemas

### Erro de Migração
```bash
# Se houver erro nas migrações
python manage.py migrate --fake-initial
```

### Erro de Arquivos Estáticos
```bash
# Coletar arquivos estáticos
python manage.py collectstatic
```

### Erro de Permissão (Linux/Mac)
```bash
# Dar permissão de execução
chmod +x manage.py
```

### Ambiente Virtual não Ativa
```bash
# Verificar se está ativo
which python  # Linux/Mac
where python  # Windows
```

## 📱 Testando no Mobile

Para testar no celular:
1. Descubra o IP da sua máquina na rede local
2. Execute: `python manage.py runserver 0.0.0.0:8000`
3. Acesse: `http://SEU_IP:8000`

## 🎵 Dados Iniciais

O comando `load_initial_data` cria:
- **8 Especialidades**: Piano, Violão, Canto, Teoria Musical, Bateria, Baixo, Saxofone, Flauta
- **Múltiplos Temas** por especialidade (ex: Técnica Básica, Harmonia, Improvisação)

## 🔐 Segurança

Para produção:
1. Mude `DEBUG = False`
2. Configure `SECRET_KEY` segura
3. Configure `ALLOWED_HOSTS`
4. Use banco PostgreSQL
5. Configure HTTPS

---

**Pronto!** Agora você pode testar todas as funcionalidades do Dyschool! 🎵 