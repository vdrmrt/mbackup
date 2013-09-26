ALTER TABLE settings RENAME TO settings_old;

-- Table: settings
CREATE TABLE settings ( 
    setting_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_section TEXT    NOT NULL,
    setting_name    TEXT    NOT NULL,
    setting_value   TEXT,
    UNIQUE ( setting_section, setting_name ) 
);

INSERT INTO [settings] ([setting_section], [setting_name], [setting_value])
SELECT [setting_section], [setting_name], [setting_value] FROM settings_old;

DROP TABLE settings_old;

INSERT INTO [versions] ([version_major], [version_minor], [version_revision], [changelog]) 
VALUES ( 0, 0, 6, 'Changed not null constraint on setting_value and added user and key settings');