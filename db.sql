CREATE TABLE cp_users_hal9000 (
    id SERIAL PRIMARY KEY,
    user_token TEXT NOT NULL,
    cp_id INT NOT NULL
);

CREATE TABLE fb_pages_hal9000 (
    id SERIAL PRIMARY KEY,
    page_id VARCHAR(255) NOT NULL,
    page_name VARCHAR(255) NOT NULL,
    page_token TEXT NOT NULL
);

CREATE TABLE cp_pages_hal9000 (
    id SERIAL PRIMARY KEY,
    cp_id INT NOT NULL,
    page_id VARCHAR(255) NOT NULL
);


