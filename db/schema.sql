
-- Table: backup_groups
CREATE TABLE backup_groups ( 
    backup_group_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_group_name        TEXT    UNIQUE,
    backup_group_description TEXT    NOT NULL,
    backup_group_destination TEXT    NOT NULL 
);


-- Table: backups
CREATE TABLE backups ( 
    backup_id          INTEGER PRIMARY KEY,
    backup_group_id    INTEGER NOT NULL
                               REFERENCES backup_groups ( backup_group_id ) ON DELETE RESTRICT
                                                                            ON UPDATE CASCADE,
    backup_name        TEXT    NOT NULL
                               UNIQUE,
    backup_source      TEXT    NOT NULL,
    backup_destination TEXT,
    backup_description TEXT    NOT NULL 
);


-- Table: backup_history
CREATE TABLE backup_history ( 
    backup_history_id        INTEGER  PRIMARY KEY
                                      NOT NULL,
    back_up_id               INT      NOT NULL
                                      REFERENCES backups ( backup_id ) ON DELETE CASCADE
                                                                       ON UPDATE CASCADE,
    backup_history_timestamp DATETIME NOT NULL,
    backup_history_log       TEXT 
);


-- Table: settings
CREATE TABLE settings ( 
    setting_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name  TEXT    NOT NULL,
    setting_value TEXT    NOT NULL 
);


-- Table: versions
CREATE TABLE versions ( 
    version_id       INTEGER PRIMARY KEY AUTOINCREMENT
                             UNIQUE,
    version_major    INTEGER NOT NULL,
    version_minor    INTEGER NOT NULL,
    version_revision INTEGER NOT NULL,
    changelog        TEXT 
);

INSERT INTO [versions] ([version_major], [version_minor], [version_revision], [changelog]) VALUES (0, 0, 1, null);
INSERT INTO versions (version_major,version_minor,version_revision,changelog) 
VALUES (0,0,2,'Added settings table');