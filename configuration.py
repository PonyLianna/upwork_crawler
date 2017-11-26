import json


class Configuration:
    def __init__(self, file="cfg/data.cfg"):
        self.file = file

    def output(self):
        with open(self.file, "r") as config:
            data = json.load(config)
        name = list(data.keys())[0]
        alph = list(data.values())[0]
        print(alph["dbname"], name, alph["host"],  alph["password"])
        return alph["dbname"], name, alph["host"],  alph["password"]

    def update(self):
        data = self.read()
        with open(self.file, "w") as config:
            data["admin"] = ""
            json.dump(data, config)
        print("Updated")

    def read(self):
        try:
            with open(self.file, "r") as config:
                data = json.load(config)
            print("Reading data")
            return data
        except json.decoder.JSONDecodeError:
            print("Your config is empty\nIt's sad.")
            return {}

    def create(self, user, dbname, host, password):
        data = self.read()
        with open(self.file, "w") as config:
            data[user] = {"dbname": dbname, "host": host, "password": password}
            json.dump(data, config)
        print("Created\nUser: {0}\ndbname: {1}\nhost: {2}\nPassword: {3}".format(user, dbname, host, password))


if __name__ == "__main__":
    conf = Configuration()
    conf.output()

