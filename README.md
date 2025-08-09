# Dyschool - Plataforma de Aulas de Música

Dyschool é uma plataforma web desenvolvida em Django que conecta alunos com professores de música para aulas avulsas. O sistema permite que alunos busquem professores especializados e agendem aulas personalizadas.

## 🎵 Funcionalidades

### Para Alunos
- **Busca de Professores**: Encontre professores por especialidade, tema de aula e valor
- **Solicitação de Aulas**: Envie solicitações detalhadas para professores
- **Acompanhamento**: Visualize disponibilidades enviadas pelos professores
- **Agendamento**: Aceite horários disponíveis e confirme aulas

### Para Professores
- **Perfil Completo**: Cadastre especialidades, temas de aula e valores
- **Solicitações**: Receba e visualize solicitações de alunos
- **Disponibilidade**: Envie horários disponíveis para alunos
- **Dashboard**: Gerencie aulas confirmadas e histórico

### Para Administradores
- **Gerenciamento de Especialidades**: Adicione novas especialidades musicais
- **Gerenciamento de Temas**: Configure temas de aula por especialidade
- **Usuários**: Gerencie alunos e professores
- **Relatórios**: Acompanhe o uso da plataforma

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2+
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)
- **Autenticação**: Django Auth System
- **Upload de Arquivos**: Pillow

## 📋 Pré-requisitos

- Python 3.8+
- pip
- virtualenv (recomendado)

## 🚀 Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd dyschool
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Carregue dados iniciais**
   ```bash
   python manage.py load_initial_data
   ```

6. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

7. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

8. **Acesse a aplicação**
   - Site: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 📁 Estrutura do Projeto

```
dyschool/
├── core/                    # Aplicação principal
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Views da aplicação
│   ├── forms.py            # Formulários
│   ├── admin.py            # Configuração do admin
│   ├── urls.py             # URLs da aplicação
│   └── templates/          # Templates HTML
│       └── core/
│           ├── base.html
│           ├── home.html
│           ├── sign_in.html
│           ├── sign_up.html
│           ├── teacher_profile.html
│           ├── teacher_dashboard.html
│           ├── student_dashboard.html
│           ├── lesson_search.html
│           ├── lesson_request.html
│           └── submit_availability.html
├── dyschool/               # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                 # Arquivos estáticos
│   └── css/
│       └── style.css
├── media/                  # Uploads de usuários
├── manage.py
├── requirements.txt
└── README.md
```

## 🗄️ Modelos de Dados

### User (Usuário)
- Extensão do modelo de usuário do Django
- Tipos: Student (Aluno) ou Teacher (Professor)
- Campos adicionais: telefone, foto, bio, data de nascimento, endereço

### Specialization (Especialidade)
- Especialidades musicais (ex: Piano, Violão, Canto)
- Relacionamento com temas de aula

### LessonTopic (Tema de Aula)
- Temas específicos dentro de uma especialidade
- Ex: "Técnica Básica", "Harmonia", "Improvisação"

### TeacherProfile (Perfil do Professor)
- Informações específicas do professor
- Especialidades, temas, valor por hora, experiência

### LessonRequest (Solicitação de Aula)
- Solicitações de alunos para professores
- Tema, duração, valor máximo, observações

### TeacherAvailability (Disponibilidade)
- Horários disponíveis enviados por professores
- Data, horário, duração

### LessonBooking (Agendamento)
- Aulas confirmadas entre aluno e professor
- Status: confirmado, concluído, cancelado

## 🔄 Fluxo de Uso

### Para Alunos:
1. Cadastre-se como aluno
2. Busque professores por especialidade/tema
3. Envie solicitação de aula
4. Aguarde disponibilidades dos professores
5. Aceite um horário disponível
6. Confirme a aula

### Para Professores:
1. Cadastre-se como professor
2. Configure perfil com especialidades e valores
3. Receba solicitações de alunos
4. Envie disponibilidades
5. Aguarde aceite do aluno
6. Confirme a aula

## 🎨 Interface

A interface foi desenvolvida com foco na usabilidade e design moderno:

- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Tema Roxo**: Cores principais em tons de roxo
- **Componentes Modernos**: Cards, botões e formulários estilizados
- **Navegação Intuitiva**: Menu de navegação claro e organizado

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Carregar dados iniciais
python manage.py load_initial_data

# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 📝 Configurações

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_URL=/media/
STATIC_URL=/static/
```

### Configurações do Django
As principais configurações estão em `dyschool/settings.py`:

- **AUTH_USER_MODEL**: 'core.User'
- **MEDIA_URL/MEDIA_ROOT**: Para uploads de arquivos
- **STATIC_URL/STATIC_ROOT**: Para arquivos estáticos

## 🚀 Deploy

### Para Produção:
1. Configure `DEBUG=False`
2. Use um banco de dados PostgreSQL
3. Configure `ALLOWED_HOSTS`
4. Configure arquivos estáticos
5. Use um servidor WSGI como Gunicorn

### Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn dyschool.wsgi:application
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento inicial* - [SeuGitHub](https://github.com/seugithub)

## 🙏 Agradecimentos

- Django Documentation
- Comunidade Django Brasil
- Professores e alunos que testaram a plataforma

## 📞 Suporte

Para suporte, envie um email para suporte@dyschool.com ou abra uma issue no GitHub.

---

**Dyschool** - Conectando alunos e professores de música desde 2024 🎵 