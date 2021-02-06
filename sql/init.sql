CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE price
(
    uuid uuid DEFAULT uuid_generate_v4(),
    pair VARCHAR NOT NULL,
    curr INT NOT NULL,
    lowest INT NOT NULL,
    highest INT NOT NULL,
    datetime CURRENT_DATE NOT NULL,
    PRIMARY KEY(uuid)
);