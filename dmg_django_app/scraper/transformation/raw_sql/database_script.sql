ALTER TABLE dmg_django_supermarket
    CHANGE COLUMN supermarket_id id INT AUTO_INCREMENT,
    CHANGE COLUMN supermarket_name name VARCHAR(50) NOT NULL,
    PRIMARY KEY(id);