-- Table: public.orders

-- DROP TABLE IF EXISTS public.orders;

CREATE TABLE IF NOT EXISTS public.orders
(
    "order_id" bigint,
    "customer_id" bigint,
    "order_date " text COLLATE pg_catalog."default",
    amount double precision
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.orders
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.customers
(
    "customer_id" bigint,
    "customer_name            " text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers
    OWNER to postgres;

COPY orders FROM '/docker-entrypoint-initdb.d/orders.csv' CSV HEADER;

COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' CSV HEADER;




