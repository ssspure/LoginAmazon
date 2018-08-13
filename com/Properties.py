
class Properties:

    def __init__(self, filename, sep = "=", comment = "#"):
        self.filename = filename
        self.sep = sep
        self.comment = comment
        self.datas = {}

        self.resolveFile()

    def resolveFile(self):
        try:
            f = open(self.filename, "r", encoding='utf-8')
            lines = f.readlines()

            for line in lines:
                if not line.startswith("#") and line.find("=")>0:
                    key = line.strip().split("=")[0].strip()
                    val = line.strip().split("=")[1].strip()
                    self.datas[key] = val
        except FileNotFoundError as e:
            print("The File is Not Exists:" + self.filename)
            exit(1)
        finally:
            f.close()

    def get(self, key):
        return self.datas.get(key)