#!/bin/bash
PROGNAME=$(basename $0)
echo 'Install BIBBOX SYS-ACTIVITIES Microservice'
echo '-  Create data folder for redis and orientDB'

mkdir -p data/redis/data

if  [[ ! -f data/orientdb/config ]]; then
        echo '-- Copy orientDB config file'
        cp config/orientdb-server-config.xml  data/orientdb/config
        cp config/security.json  data/orientdb/config
        echo '-- Copy orientDB default DB'
        cp -R config/orientdbdatabases/*  data/orientdb/databases/
fi
echo '-- redis    db0pw  = bibbox4ever'
echo '-  Finished'
echo 'run docker-compose up -d'