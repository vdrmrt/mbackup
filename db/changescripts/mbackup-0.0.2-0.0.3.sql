BEGIN;

ALTER TABLE settings RENAME TO settings_old;

-- Table: settings
CREATE TABLE settings ( 
    setting_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_section TEXT    NOT NULL,
    setting_name    TEXT    NOT NULL,
    setting_value   TEXT    NOT NULL,
    UNIQUE ( setting_section, setting_name ) 
);

INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) 
SELECT [setting_id], 'connection', [setting_name], [setting_value] FROM settings_old WHERE [setting_name] = 'host';
INSERT INTO [settings] ([setting_id], [setting_section], [setting_name], [setting_value]) 
SELECT [setting_id], 'connection', [setting_name], [setting_value] FROM settings_old WHERE [setting_name] = 'port';

DROP TABLE settings_old;

INSERT INTO [versions] ([version_major], [version_minor], [version_revision], [changelog]) VALUES (0, 0, 3, 'Added section column to settings table');