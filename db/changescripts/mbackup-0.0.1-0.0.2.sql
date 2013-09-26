CREATE TABLE settings ( 
    setting_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name  TEXT    NOT NULL,
    setting_value TEXT    NOT NULL 
);

INSERT INTO versions (version_major,version_minor,version_revision,changelog) 
VALUES (0,0,2,'Added settings table');