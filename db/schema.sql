
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
    setting_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_section TEXT    NOT NULL,
    setting_name    TEXT    NOT NULL,
    setting_value   TEXT    NOT NULL,
    UNIQUE ( setting_section, setting_name ) 
);

INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) VALUES (1, 'connection', 'host', 'rsync.mvsrv.be');
INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) VALUES (2, 'connection', 'port', 1503);
INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) VALUES (3, 'application', 'loglevel', 'INFO');
INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) VALUES (4, 'view', 'type', 'text');

-- Table: versions
CREATE TABLE versions ( 
    version_id       INTEGER PRIMARY KEY AUTOINCREMENT
                             UNIQUE,
    version_major    INTEGER NOT NULL,
    version_minor    INTEGER NOT NULL,
    version_revision INTEGER NOT NULL,
    changelog        TEXT,
    UNIQUE ( version_major, version_minor, version_revision ) 
);

INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog]) VALUES (1, 0, 0, 1, null);
INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog]) VALUES (2, 0, 0, 2, 'Added settings table');
INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog]) VALUES (3, 0, 0, 3, 'Added section column to settings table');
INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog]) VALUES (4, 0, 0, 4, 'Added loglevel record in settings table and unique key to versions table');
INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog]) VALUES (5, 0, 0, 5, 'Added view type record in settings table');
