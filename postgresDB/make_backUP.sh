#!/bin/bash

# Запускаем PostgreSQL в фоновом режиме
/usr/local/bin/docker-entrypoint.sh postgres &

echo "Dropping public schema..."
psql -U postgres -d PET_SHOP <<-EOSQL
    DROP SCHEMA public CASCADE;
EOSQL

# Ждем пока PostgreSQL станет доступен
until pg_isready -h localhost -U postgres; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Восстанавливаем базу данных
echo "Restoring database from backup..."
pg_restore -U postgres -d PET_SHOP BAckUp.sql

# Оставляем контейнер работающим
wait
