import mysql.connector
import os
import sys
import time
import json
import re

class MySQLAddOn:

    def __init__(self):
        """
            General configurations
        """
        self.fullpath = os.path.abspath(os.path.dirname(__file__))
        multi_env = os.getenv('DATABASE_SI', False)
        '''
        GS_MYSQL_PASSWORD=
        GS_MYSQL_PORT=3306
        GS_MYSQL_USER=python
        GS_MYSQL_HOST=192.168.29.30
        GS_MYSQL_DATABASE=dbs_machines
        '''
        # Multi-line params
        self.conn_dict = {}
        if bool(multi_env):
            TRANSLATE_MAP = {
                'user': 'GS_MYSQL_USER',
                'password': 'GS_MYSQL_PASSWORD',
                'host': 'GS_MYSQL_HOST',
                'port': 'GS_MYSQL_PORT',
                'database': 'GS_MYSQL_DATABASE',
            }

            for f_data in multi_env.splitlines():
                f_data = f_data.split('=')
                # dados para conexao do banco
                for map_data in TRANSLATE_MAP.items():
                    if len(f_data) == 2 and f_data[0] in map_data[1]:
                        self.conn_dict.update({map_data[0]: f_data[1]})

            try:
                self.conn = mysql.connector.connect(**self.conn_dict)
                self.conn.autocommit = True
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print('ERROR: ', err)


    def separate_data(self, pkgs, kernel):
        bancos = []
        base_win = ['SQL Server \d+ Database.*', 'postgresql.*', 'mysql-server.*', \
        'mariadb.*', 'percona.*']

        base_lnx = ['percona-server-server.*', 'mongodb-server.*', 'postgresql.*', \
        'mysql-server.*', 'mariadb-server.*']

        if kernel == 'Windows':
            for pkg in pkgs.items():
                for regex in base_win:
                    r = re.compile('^'+regex+'$', re.IGNORECASE)
                    rlist = list(filter(r.match, pkg))
                    for banco in rlist:
                        if list(pkg) not in bancos and len(list(pkg)) == 2:
                            bancos.append({list(pkg)[0] : list(pkg)[1]})

        elif kernel == 'Linux':
            for pkg in pkgs.items():
                for regex in base_lnx:
                    r = re.compile('^'+regex+'$', re.IGNORECASE)
                    rlist = list(filter(r.match, pkg))
                    for banco in rlist:
                        if list(pkg) not in bancos and len(list(pkg)) == 2:
                            bancos.append({list(pkg)[0] : list(pkg)[1]})

        return bancos


    def insert_machine(self, machine_name, grains_item, pkg_list_pkgs):
        cursor = self.conn.cursor()
        # Já exite?
        select_query = "SELECT COUNT(*) FROM machines WHERE name = %s"
        cursor.execute(select_query, (machine_name,))
        count = cursor.fetchone()[0]

        if count > 0:
            # UPDATE
            update_query = "UPDATE machines SET grains_item = %s, pkg_list_pkgs = %s WHERE name = %s"
            cursor.execute(update_query, (grains_item, pkg_list_pkgs, machine_name))
            # print(f"UPDATE: {machine_name}")
        else:
            # INSERT
            insert_query = "INSERT INTO machines (name, grains_item, pkg_list_pkgs) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (machine_name, grains_item, pkg_list_pkgs))
            # print(f"INSERT: {machine_name}")


    def parse_data(self):
        """
            Load json data and insert into database
        """
        json_file = sys.argv[1]

        count = 1
        def parse_banco(bancos):
            res = [f"{key}={value}" for item in bancos for key, value in item.items()]
            lmp = "; ".join(res)

            return lmp

        try:
            # Parse Patches
            jdata = json.loads(open(json_file, 'r').read().replace('\n','').replace('}{','},{'))
            # print('J_DATA ', jdata)

            # Inserir/atualizar no banco de dados
            machines = jdata['data']
            for machine_name, machine_data in machines.items():
                ret = machine_data['ret']
                grains_item = str(ret.get('grains.item', {}))
                pkg_list_pkgs = str(ret.get('pkg.list_pkgs', {}))
                bancos = self.separate_data(ret['pkg.list_pkgs'], ret['grains.item']['kernel'])

                if bool(bancos):
                    flavors_db = parse_banco(bancos)
                    grains = machine_data['ret']['grains.item']
                    info_machine = f"{grains.get('host', '')}; {grains.get('osfinger', '')}"
                    # Run the insert
                    self.insert_machine(machine_name, info_machine, flavors_db)

            print('\n', '{} Finish...'.format(json_file), '\n')

        except Exception as err:
            print('Final Error: {}'.format(str(err)))
            pass


# Run mysql
MySQLAddOn().parse_data()
MySQLAddOn().conn.close()
