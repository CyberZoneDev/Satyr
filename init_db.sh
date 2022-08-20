#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "bootcamp" --dbname "bootcamp" <<-EOSQL
    CREATE USER satyr_slave WITH PASSWORD 'Sup3R_SatyR_SlAv3_P0sswArb';
    CREATE DATABASE satyr WITH OWNER 'satyr_slave';
EOSQL

psql -v ON_ERROR_STOP=1 --username "satyr_slave" --dbname "satyr" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL