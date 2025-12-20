-- Adminer 5.4.1 PostgreSQL 17.6 dump

DROP TABLE IF EXISTS "posts";
DROP SEQUENCE IF EXISTS posts_id_seq;
CREATE SEQUENCE posts_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."posts" (
    "id" integer DEFAULT nextval('posts_id_seq') NOT NULL,
    "title" character varying(40) NOT NULL,
    "content" text,
    "filename" character varying(40),
    CONSTRAINT "posts_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


DROP TABLE IF EXISTS "users";
CREATE TABLE "public"."users" (
    "id" character varying(10) NOT NULL,
    "pwd" character varying(10) NOT NULL,
    "name" character varying(10) NOT NULL
)
WITH (oids = false);

INSERT INTO "users" ("id", "pwd", "name") VALUES
('user',	'pass',	'使用者'),
('admin',	'pass',	'系統管理員');

-- 2025-12-20 14:53:13 UTC
