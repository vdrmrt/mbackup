ALTER TABLE versions RENAME TO versions_old;

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

INSERT INTO [versions] ([version_major], [version_minor], [version_revision], [changelog])
SELECT [version_major], [version_minor], [version_revision], [changelog] FROM versions_old;

DROP TABLE versions_old;

INSERT INTO [versions] ([version_id], [version_major], [version_minor], [version_revision], [changelog])
VALUES (4, 0, 0, 4, 'Added loglevel record in settings table and unique key to versions table');