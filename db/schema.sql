
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


-- Table: versions
CREATE TABLE versions ( 
    version_release_number VARCHAR PRIMARY KEY,
    changelog              TEXT 
);

INSERT INTO [versions] ([version_release_number], [changelog]) VALUES ('0.0.1', 'First version');

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

