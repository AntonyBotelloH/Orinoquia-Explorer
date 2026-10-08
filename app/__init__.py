import pymysql

# Permitir que Django use PyMySQL como adaptador de MySQLdb en servidores cPanel/Passenger
pymysql.install_as_MySQLdb()
