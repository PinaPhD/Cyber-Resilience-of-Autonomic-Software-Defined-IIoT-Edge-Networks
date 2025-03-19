---
### MySQL Knowledge Base Installation Guide

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation

```

To Verify that MySQL is properly installed and running: `sudo systemctl status mysql`
To Login: `sudo mysql -u <user_id> -p` and then enter the <user_id> password when prompted.

To allow another VM to interact with this DB remotely:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
	bind-address = 0.0.0.0
	mysqlx-bind-address = 0.0.0.0
```

Restart the MySQL server for changes to take effect: `sudo systemctl restart mysql`

Create other users and assign privileges:

```bash
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;

CREATE USER 'pina254'@'%' IDENTIFIED BY '8998';
GRANT ALL PRIVILEGES ON *.* TO 'pina254'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
EXIT;

```