powershell -File c:\temp\salt_upgrade\upgrade_call_oop.ps1 "TVT" "192.168.29.30" "upgrade" "30" "$true"


# Get Sql Server
https://stackoverflow.com/questions/7587077/how-do-i-check-for-the-sql-server-version-using-powershell

# DOC
https://learn.microsoft.com/pt-br/sql/t-sql/functions/serverproperty-transact-sql?view=sql-server-ver16



# Fazer uma lista
- Maquina
- Nome do banco 
- Versão


# Executar Script
python3 get_soft.py -b -s TM

# Olhar caminho
/srv/jenkins/jenkins_home/workspace/saltstack/salt_softs

# Truncate Mysql
```
CREATE TABLE `machines` (
  `id` int NOT NULL,
  `name` text,
  `grains_item` text,
  `pkg_list_pkgs` text,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `machines`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `machines`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;
```

# Create connection
***DATABASE_SI***
```
GS_MYSQL_USER=python
GS_MYSQL_PASSWORD=123.senha
GS_MYSQL_HOST=192.168.29.30
GS_MYSQL_PORT=3306
GS_MYSQL_DATABASE=dbs_machines
```

***export DATABASE_SI***
```
export DATABASE_SI="GS_MYSQL_USER=python
GS_MYSQL_PASSWORD=123.senha
GS_MYSQL_HOST=192.168.29.30
GS_MYSQL_PORT=3306
GS_MYSQL_DATABASE=dbs_machines"
```

***Update Syndic***
```
python3.9 mysql_addon.py softs_TM.json
```
