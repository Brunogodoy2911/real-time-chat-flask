# Real-Time Chat (Flask + Socket.IO)

Uma aplicação de chat em tempo real desenvolvida com **Flask** e
**Socket.IO**, apresentando uma interface moderna estilo **WhatsApp
(Dark Mode)**, autenticação segura e persistência de mensagens.

------------------------------------------------------------------------

## 📋 Resumo

Este projeto é uma aplicação de chat *full-stack* que permite aos
utilizadores registarem-se, fazerem login e trocarem mensagens
instantaneamente.\
O backend gere a autenticação e o armazenamento de mensagens utilizando
**SQLAlchemy**, enquanto o frontend comunica via **WebSockets** para
atualizações em tempo real.

------------------------------------------------------------------------

## ✨ Funcionalidades

-   🔄 **Mensagens em Tempo Real:** Comunicação instantânea usando
    Flask-SocketIO.\
-   🔐 **Autenticação de Utilizadores:** Login seguro com bcrypt e
    Flask-Login.\
-   🖼️ **Upload de Avatar:** Envio de foto de perfil no registo ou
    atualização posterior.\
-   💬 **Histórico de Mensagens:** Todas as mensagens são gravadas em
    SQLite.\
-   🎨 **Interface Responsiva:** Tema Dark moderno estilo WhatsApp, com
    bolhas de envio/receção.

------------------------------------------------------------------------

## 🚀 Tecnologias Utilizadas

Com base no ficheiro `requirements.txt`:

-   Python 3\
-   Flask\
-   Flask-SocketIO\
-   Flask-SQLAlchemy\
-   Flask-Login\
-   Bcrypt

------------------------------------------------------------------------

## 🔌 Endpoints da API

  ----------------------------------------------------------------------------------
  Método   Endpoint              Descrição                                    Auth
  -------- --------------------- -------------------------------------------- ------
  POST     `/api/login`          Autentica o utilizador (JSON: username,      Não
                                 password).                                   

  POST     `/api/user`           Regista um novo utilizador (FormData +       Não
                                 avatar).                                     

  POST     `/api/send_message`   Envia uma nova mensagem e guarda na base de  Sim
                                 dados.                                       

  GET      `/api/messages`       Retorna o histórico completo de mensagens.   Sim

  POST     `/api/upload_photo`   Atualiza a foto de perfil do utilizador.     Sim

  GET      `/logout`             Encerra a sessão do utilizador.              Sim
  ----------------------------------------------------------------------------------

------------------------------------------------------------------------

## 📸 Imagens do Interface (Frontend)

Adicione aqui as capturas de ecrã da sua aplicação:

1.  **Ecrã de Login**\
    Interface minimalista com tema escuro.\
2.  **Ecrã de Registo**\
    Formulário com pré-visualização do avatar.\
3.  **Sala de Chat Principal**\
    Mensagens trocadas em tempo real com estilo moderno.

------------------------------------------------------------------------

## 🛠️ Como Executar

### 1. Clonar o repositório

``` bash
git clone <seu-repositorio>
cd seu-projeto
```

### 2. Instalar dependências

``` bash
pip install -r requirements.txt
```

### 3. Executar a aplicação

``` bash
python app.py
```

### 4. Aceder no navegador

    http://127.0.0.1:5000

------------------------------------------------------------------------

## 📄 Licença

Este projeto é de uso livre para estudo e modificação.
