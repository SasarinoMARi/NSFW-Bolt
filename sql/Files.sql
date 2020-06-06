SELECT * FROM files

ALTER TABLE files ADD COLUMN thumbnail text

INSERT INTO Files(name, filename, directory, isFolder, extension) VALUES(
       'Test', 'Test', 'C:\Test', FALSE, NULL)
       
UPDATE files SET isFolder = 0 WHERE isfolder IS FALSE
UPDATE files SET isFolder = 1 WHERE directory LIKE '%漫画%'