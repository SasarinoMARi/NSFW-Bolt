class nFile:
    name = None
    fileName = None
    directory = None
    isFolder = None
    extension = None
    thumbnail = None

    @staticmethod 
    def createWithRow(row):
        instance = nFile()
        instance.name = row['name']
        instance.fileName = row['filename']
        instance.directory = row['directory']
        instance.isFolder = row['isFolder']
        instance.extension = row['extension']
        instance.thumbnail = row['thumbnail']
        return instance