#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h localhost -U admin; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing pg_dump"
pg_dump -U admin -W -d PET_SHOP > Backup.sql
