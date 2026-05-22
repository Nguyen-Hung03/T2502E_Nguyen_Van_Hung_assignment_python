CREATE DATABASE IF NOT EXISTS news_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE news_management;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(150) NOT NULL,
    url VARCHAR(500) NOT NULL,
    category_id INT NOT NULL,
    parser_type VARCHAR(50) NOT NULL DEFAULT 'generic',
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_sources_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS articles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source_id INT NOT NULL,
    category_id INT NOT NULL,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000) NOT NULL,
    summary TEXT NULL,
    content LONGTEXT NULL,
    status TINYINT NOT NULL DEFAULT 0 COMMENT '0: chi co link, 1: da lay noi dung',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_articles_url UNIQUE (url),
    CONSTRAINT fk_articles_source
        FOREIGN KEY (source_id) REFERENCES sources(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_articles_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_articles_status_created (status, created_at)
);

INSERT INTO categories (category_name)
VALUES
    ('Cong nghe'),
    ('Kinh doanh'),
    ('The thao'),
    ('Giai tri'),
    ('The gioi')
ON DUPLICATE KEY UPDATE category_name = VALUES(category_name);
