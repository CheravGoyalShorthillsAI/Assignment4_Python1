class LoaderHelper():
    def __init__(self, file_path: str, object):
        self.file_path = file_path
        self.object = object

    def load(self):
        try:
            # Attempt to load the file
            file = self.object(self.file_path)
            return file
        except Exception:
            # Catch any exception related to loading the file and raise the expected error
            raise ValueError("Invalid file.")