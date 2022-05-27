#!/bin/bash

if [ "$1" == "initdb" ]; then
    cd helper 
    python dbCreate.py
    echo "Database created"
    ls
elif [ "$1" == "deletedb" ]; then
    rm db.sqlite
    echo "Database deleted"
    ls
elif [ "$1" == "parsinfo" ]; then
    python knoema.py
    echo "info added!"
    ls
elif [ "$1" == "rebuildbd" ]; then
    rm db.sqlite
    echo "Database deleted"
    ls
    cd helper 
    python dbCreate.py
    echo "Database created"
    ls
else
    echo "initdb - создаст пустую базу данных"
    echo "deletedb - удалит базу данных"
    echo "rebuildbd - пересоберет базу данных"
    echo "parsinfo - спарсит данные"
fi
