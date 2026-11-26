#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- 1. criar as tabelas (copiar do main.py)
   -- Tabela de pessoas: a CHAVE PRIMÁRIA é o id
        CREATE TABLE IF NOT EXISTS pessoas (
            id SERIAL PRIMARY KEY,      -- SERIAL = número automático (1, 2, 3...)
            nome TEXT NOT NULL          -- NOT NULL = obrigatório
        );
    -- Tabela de dentes: tem a própria chave primária
    -- e a CHAVE ESTRANGEIRA pessoa_id, que aponta para pessoas(id)
        CREATE TABLE IF NOT EXISTS dentes (
            id SERIAL PRIMARY KEY,
            pessoa_id INTEGER NOT NULL REFERENCES pessoas(id) ON DELETE CASCADE,
            -- ON DELETE CASCADE: se apagar a pessoa, os dentes dela somem junto
            data DATE NOT NULL,
            arcada TEXT NOT NULL CHECK (arcada IN ('cima', 'baixo')),
            -- CHECK: o banco só aceita 'cima' ou 'baixo'
            qual_dente TEXT NOT NULL,
            presente NUMERIC(6,2) DEFAULT 0
            -- NUMERIC(6,2): número com 2 casas decimais (ex.: 5.50 de presente)
        );
    -- 2. criar o usuário da aplicação, com a senha vinda do .env
    CREATE USER ${FADA_APP_USER} WITH PASSWORD '${FADA_APP_PASSWORD}';

    -- 3. dar só as permissões necessárias
    GRANT SELECT, INSERT, UPDATE, DELETE ON PESSOAS, DENTES TO ${FADA_APP_USER};
    GRANT USAGE ON SEQUENCE pessoas_id_seq, dentes_id_seq TO ${FADA_APP_USER};
EOSQL