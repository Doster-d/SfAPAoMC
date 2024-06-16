CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(320) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(1024) NOT NULL
);

CREATE TABLE access_tokens (
    token VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);