# Alibaba Scraper

Sistema que automatiza o processo de coleta de dados de produtos e fornecedores na plataforma Alibaba, com foco na busca e organização de cotações de fornecedores internacionais.

A solução combina uma **extensão personalizada do Google Chrome**, um **backend em Python com Flask**, um **banco de dados relacional** e uma **interface web** para visualização e exportação dos dados coletados.

---

## Instalação e Uso da Extensão do Google Chrome

A extensão utilizada neste projeto é uma **extensão personalizada do Google Chrome**, carregada em modo desenvolvedor.  
Ela é responsável por coletar automaticamente os dados de produtos e fornecedores diretamente do site do Alibaba.

⚠️ **Importante:**  
Antes de utilizar a extensão, é **obrigatório** criar uma **Request for Quotation** na aplicação web local desenvolvida com Flask.  
Todas as *quotations* coletadas pela extensão **devem estar associadas a uma request for quotation ativa**.

---

### Instalação

#### Acesse a pasta do projeto
Entre no diretório principal onde o código foi clonado.

```bash
cd python-aliababa-product-capture-tool
```

#### Crie o ambiente virtual 
Isso isola as dependências do projeto para não interferir no seu sistema.

```bash
python -m venv venv
```

#### Ative o ambiente virtual:

- No Linux/Mac

```bash
source venv/bin/activate
```

- No Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

#### Instale as dependências
Baixa e instala todos os pacotes necessários (como Flask e SQLAlchemy).

```bash
pip install -r requirements.txt
```

#### Inicialize o Banco de Dados

Dependendo do seu objetivo no projeto, escolha uma das opções abaixo para preparar o banco de dados:

##### Uso da App ou Desenvolvimento da Extensão
Se você pretende capturar dados reais usando a extensão do Chrome ou quer testar a aplicação do zero, crie um banco de dados vazio:

```bash
flask start_db
```
> Use esta opção se você for instalar a extensão para capturar produtos diretamente do Alibaba.

##### Desenvolvimento Backend (Sem Extensão)
Se você quer contribuir para o código da aplicação (Python/Flask) sem precisar instalar a extensão ou capturar dados manualmente, utilize o comando de seeding:

```bash
flask start_and_seed_db
```
> O banco de dados será criado e preenchido automaticamente com dados fictícios (sportive shoes, smartwatches, etc.), permitindo que você veja as funcionalidades da aplicação imediatamente.
imento:


#### Execute a aplicação
Inicia o servidor de desenvolvimento do Flask.

```bash
flask run
```

A aplicação web ficará disponível localmente (por padrão em `http://localhost:5000`).

---

### Criar uma Request for Quotation
> Caso tenha inicializado o banco de dados com o comando `start_and_seed_db` e pretenda contribuir apenas com o desenvolvimento do sistema, esta seção é opcional. 

1. Acesse a aplicação web local no navegador.
2. Na tela principal, crie uma nova **Request for Quotation**, informando:
   - Um título
   - A quantidade desejada
3. Após criada, a request será automaticamente marcada como **ativa**.

📌 Apenas **uma request for quotation ativa** pode receber novas quotations.  
A extensão sempre associará os dados coletados à request ativa no momento do scraping.

---

### Instalar a extensão do Google Chrome
> Caso tenha inicializado o banco de dados com o comando `start_and_seed_db` e pretenda contribuir apenas com o desenvolvimento do sistema, esta seção é opcional. 


1. Abra o Google Chrome.
2. Acesse:
   ```
   chrome://extensions
   ```
3. Ative o **Modo do desenvolvedor** no canto superior direito.
4. Clique em **“Carregar sem compactação”** (*Load unpacked*).
5. Selecione a pasta **`product-scraper`** localizada na raiz do projeto.

Após esses passos, a extensão estará instalada e pronta para uso.

---

### Utilizar a extensão para coletar dados
> Caso tenha inicializado o banco de dados com o comando `start_and_seed_db` e pretenda contribuir apenas com o desenvolvimento do sistema, esta seção é opcional. 


1. Certifique-se de que:
   - O servidor Flask esteja em execução.
   - Exista uma **request for quotation ativa** na aplicação web local.

2. Acesse o site do **Alibaba** e navegue até a **página de um produto específico**  
   (não utilize páginas de listagem ou resultados de busca).

3. Com a página do produto aberta, utilize a **extensão do Google Chrome**, conforme demonstrado no vídeo explicativo do projeto.

https://github.com/user-attachments/assets/ee6fb04f-e7f6-42ea-a42d-6c351ec54549


## Visão Geral da Solução

O sistema é composto por várias partes que trabalham de forma integrada:

- Extensão do Google Chrome para coleta automática de dados diretamente das páginas de produtos do Alibaba.
- Servidor web local em Python (Flask) responsável por receber, processar e persistir os dados.
- Banco de dados relacional (SQLite) para armazenar requests for quotation e quotations.
- Comunicação em tempo real com Socket.IO para sincronização automática da interface.
- Exportação de dados para CSV para geração de relatórios.

---

## Estrutura do Projeto

```
├── app.py
├── csv
├── migrations
│   └── 0001_alter_table_names.sql
├── product-scraper
│   ├── content.js
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── README.md
├── repository.py
├── requirements.txt
├── schema.py
├── sheets.py
├── templates
│   ├── quotation_edit.html
│   ├── quotation_list.html
│   └── request_for_quotation_list.html
├── utils.py
└── fake.py
```

---

## product-scraper

Diretório que contém os arquivos da **extensão personalizada do Google Chrome** responsável pelo scraping.

O arquivo mais importante é o **`content.js`**, onde:
- Os dados do produto e do fornecedor são extraídos diretamente do DOM da página do Alibaba.
- As informações coletadas são enviadas para o servidor Flask local através de uma requisição HTTP (`/webhook`).

---

## app.py

Arquivo principal da aplicação backend.

Responsabilidades principais:

- Inicializa o servidor Flask.
- Configura CORS para permitir requisições apenas do domínio do Alibaba.
- Define o endpoint `/webhook`, responsável por:
  - Receber os dados enviados pela extensão.
  - Persistir as cotações no banco de dados.
  - Emitir eventos via Socket.IO para atualizar a interface em tempo real.
- Define endpoints para:
  - Criar e listar **requests for quotation**.
  - Listar **quotations** associadas a uma request.
  - Gerar arquivos CSV com as cotações.
- Define um comando customizado do Flask para inicializar o banco de dados.

---

## templates

Contém os templates HTML que compõem o frontend da aplicação.

- **request_for_quotation_list.html**  
  Permite criar e ativar uma *request for quotation*.  
  Lista todas as requests cadastradas, exibindo a quantidade de quotations associadas a cada uma.

- **quotation_list.html**  
  Exibe todas as *quotations* relacionadas a uma *request for quotation* específica.  
  Esses dados são extraídos diretamente do site do Alibaba.

- **quotation_edit.html**  
  Exibe todas as propriedades de uma *quotation*, permitindo a edição de algumas delas.

---

## schema.py

Define o esquema do banco de dados utilizando **SQLAlchemy Core**.

Este módulo atua como a camada de definição das tabelas e da estrutura do banco, fazendo a ponte entre o banco de dados relacional e a aplicação Python.

---

## repository.py

Contém a classe **`SQLAlchemyRepository`**, responsável por **todas as interações com o banco de dados**.

- Toda comunicação com o banco deve ser feita exclusivamente através desta classe.
- Centraliza a lógica de persistência, consultas e atualizações.

---

## sheets.py

Responsável pela exportação dos dados.

Atualmente:
- Exporta as cotações para o formato **CSV**.
- Os arquivos gerados são salvos no diretório `csv/`.

---

## utils.py

Módulo de utilidades auxiliares.

- **slugify**  
  Gera strings seguras para nomes de arquivos e URLs.

- **copy_buyer_script_to_clipboard**  
  Copia automaticamente um script com informações do comprador para a área de transferência.

---

## Requisitos

- Python 3.10+
- Google Chrome
- Git (opcional)

---

## Variáveis de Ambiente

```
BUYER_NAME
BUYER_ADDRESS
```

---

## Observações Finais

Projeto desenvolvido a partir da combinação entre estudo acadêmico e aprendizado autodidata.
