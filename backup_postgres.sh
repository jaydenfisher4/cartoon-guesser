#!/bin/bash

# Configuration (replace these with your Render PostgreSQL details)
HOST="dpg-cv01fbtumphs73cfjvbg-a.ohio-postgres.render.com"        # e.g., pg-render-host.region.render.com
PORT="5432"                       # Usually 5432
USER="cartoon_guesser_db_user"       # e.g., myuser
DB_NAME="cartoon_guesser_db"     # e.g., mydb
PASSWORD="eiJzd2jGnDLo54CG8oBQsgdQCWvkpDvy"    # e.g., mypassword

# Output file name with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backups/cartoon_guesser_backup_$TIMESTAMP.dump"

# Create backups directory if it doesn’t exist
mkdir -p backups

# Export PGPASSWORD to avoid prompt
export PGPASSWORD=$PASSWORD

# Run pg_dump to create the backup
pg_dump -h "$HOST" -p "$PORT" -U "$USER" -d "$DB_NAME" -F c -f "$BACKUP_FILE"

# Check if the command succeeded
if [ $? -eq 0 ]; then
    echo "Backup saved to $BACKUP_FILE"
else
    echo "Backup failed!"
    exit 1
fi

# Unset PGPASSWORD for security
unset PGPASSWORD