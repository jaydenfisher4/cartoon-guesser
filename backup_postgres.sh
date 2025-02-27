#!/bin/bash

HOST="dpg-cv01fbtumphs73cfjvbg-a.ohio-postgres.render.com"       
PORT="5432"                     
USER="cartoon_guesser_db_user"      
DB_NAME="cartoon_guesser_db"    
PASSWORD="eiJzd2jGnDLo54CG8oBQsgdQCWvkpDvy"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backups/cartoon_guesser_backup_$TIMESTAMP.dump"

mkdir -p backups

export PGPASSWORD=$PASSWORD

pg_dump -h "$HOST" -p "$PORT" -U "$USER" -d "$DB_NAME" -F c -f "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup saved to $BACKUP_FILE"
else
    echo "Backup failed!"
    exit 1
fi

unset PGPASSWORD