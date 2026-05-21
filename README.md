Guia de inicialização local do projeto pós clonagem:
#Criar a pasta venv:
python -m venv venv

#Instalar todas as bibliotecas do projeto:
#Sempre que utilizarem novas bibliotecas adicionem elas no requirements.txt
.\venv\Scripts\pip install -r requirements.txt

#Rodar o servidor:
.\venv\Scripts\python.exe manage.py runserver
