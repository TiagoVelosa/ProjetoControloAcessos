# ProjetoControloAcessos

A instalação para sistema UNIX é a seguinte:

A instalação do Django requer o Python com a versão 3.8 ou superior instalada no sistema para instalar é necessário utilizar este comando no linux:

$ sudo apt-get update
$ sudo apt-get install python3.8

Para verificar a versão é utilizado este comando:
$ python3 --version

Após a instalação do Python é necessário instalar/configurar a base de dados:

Para o Mysql ou MariaDB é necessário instalar o mysqlclient

É recomendado instalar um virtual environment para instalar o Django para tal é necessário do pip, para instalar o pip são necessários os seguintes comandos:

-python3 -m pip install --user --upgrade pip

-python3 -m pip --version

-pip 21.1.3 from $HOME/.local/lib/python3.9/site-packages (python 3.9)

Depois criar o virtual environment 

-python3 -m pip install --user virtualenv

-python3 -m venv env

Para ativar o virtual environment utiliza-se o comando:

-source env/bin/activate

Para desativar simplesmente escreve-se “deactivate”

Após a criação e ativação do virtual environment podemos instalar o Django com o seguinte comando:

-python -m pip install Django   (ou substituir o python por python3 se houverem múltiplas versões do python instaladas)

-git clone https://github.com/TiagoVelosa/ProjetoControloAcessos

-python -m pip install -e ProjetoControloAcessos/

As configurações da base de dados estão no ficheiro settings.py dentro da pasta projeto.

Para fazer migrações utiliza-se o comando: python manage.py migrate

E para correr o servidor: python manage.py runserver

Provavelmente será necessário instalar a extensão xhtml2pdf:

-python -m pip instal --pre xhtml2pdf


Referências: https://docs.djangoproject.com/en/3.2/intro/install/
https://docs.djangoproject.com/en/3.2/topics/install/#database-installation
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/


