#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "XXX" --dbname "XXX" <<-EOSQL
    CREATE USER XXX WITH PASSWORD 'XXX';
    CREATE DATABASE XXX OWNER 'XXX';
EOSQL

psql -v ON_ERROR_STOP=1 --username "XXX" --dbname "XXX" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
