#!/bin/bash


CONTAINER_NAME="status-checker_db_1"
PG_USER="${POSTGRES_USER}"
PG_DB="${POSTGRES_DB}"

BACKUP_DIR="/tmp/pg_backup"
mkdir -p $BACKUP_DIR

DATE=$(date +'%Y-%m-%d_%H-%M-%S')
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.sql"

docker exec $CONTAINER_NAME pg_dump -U $PG_USER $PG_DB > $BACKUP_FILE

tar -czf /tmp/backup_${DATE}.tar.gz -C $BACKUP_DIR .

gsutil cp /tmp/backup_${DATE}.tar.gz gs://url-checker-459813-backup-bucket

rm /tmp/backup_${DATE}.tar.gz
rm -rf $BACKUP_DIR
