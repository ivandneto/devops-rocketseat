# ============ ESTÁGIO 1: builder ============
# Imagem base: Python 3.14 sobre Alpine (Linux mínimo).
# "AS builder" dá um nome a este estágio, para o segundo poder copiar coisas dele.
FROM python:3.14-alpine AS builder

# Pasta de trabalho dentro da imagem (como um "cd"; se não existir, é criada).
WORKDIR /app

# Copia SÓ a lista de bibliotecas primeiro.
# Assim, a camada do pip fica no cache: se você mudar só o código,
# o Docker não reinstala tudo no próximo build.
COPY requirements.txt /app/requirements.txt

# Instala as bibliotecas da lista (fastapi, uvicorn, psycopg).
# --no-cache-dir: o pip não guarda os arquivos baixados (imagem menor).
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o resto do projeto (o main.py) para /app.
COPY . /app


# ============ ESTÁGIO 2: execução ============
FROM python:3.14-alpine


COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages

COPY --from=builder /app/main.py /app/main.py

WORKDIR /app

RUN adduser -D appuser
USER appuser

EXPOSE 8000 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]