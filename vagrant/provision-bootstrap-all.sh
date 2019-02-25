# on ajoute un utilisateur
adduser dev

# mise à jour des paquets installés
yum update -y

# installation EPEL ( Extra Packages for Enterprise Linux )
yum install epel-release -y

# dépôt pour installer python 3.6 + installation
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum install -y \
    python36u \
    python36u-pip \
    python36u-devel

# dépôt pour installer postgresql 10 + installation
yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
yum install -y \
    postgresql10 \
    postgresql10-server \
    postgresql10-devel \
    postgresql10-contrib \
    gcc-c++ \
    policycoreutils-python

# initialisation du serveur de base de donnée postgresql
/usr/pgsql-10/bin/postgresql-10-setup initdb
systemctl enable postgresql-10
systemctl start postgresql-10
# création de l'utilisateur de base de données, et de la base de données en développement
su - postgres -c "createuser --createdb --no-superuser --createrole --no-password vagrant"
su - vagrant -c "createdb -O vagrant botOxem_dev"
