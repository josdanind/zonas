#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crea las bases de datos
	CREATE DATABASE $DB_ZONAS;
EOSQL
