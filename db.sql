CREATE TABLE cp_users (
    id SERIAL PRIMARY KEY,
    user_token TEXT NOT NULL,
    cp_id INT NOT NULL
);

CREATE TABLE fb_pages (
    id SERIAL PRIMARY KEY,
    page_id VARCHAR(255) NOT NULL,
    page_name VARCHAR(255) NOT NULL,
    page_token TEXT NOT NULL
);

CREATE TABLE cp_pages (
    id SERIAL PRIMARY KEY,
    cp_id INT NOT NULL,
    page_id VARCHAR(255) NOT NULL
);


