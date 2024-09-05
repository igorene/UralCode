CREATE TABLE IF NOT EXISTS corp(
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
mail text NOT NULL,
phone text NOT NULL,
region text NOT NULL,
city text NOT NULL,
description text NOT NULL,
category text NOT NULL,
specialization text NOT NULL
);