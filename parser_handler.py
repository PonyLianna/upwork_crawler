import psycopg2
import matplotlib.pyplot as plt

class InformationHandler:
    def __init__(self):
        login_data = ['', '', '', '']
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(login_data[0],
                                                                                           login_data[1],
                                                                                           login_data[2],
                                                                                           login_data[3]))
        cursor = conn.cursor()
        cursor.execute("SELECT id, salary, tags FROM jobs")

        dictionary = self.dictionary(cursor)
        sort = self.popularity(dictionary)
        self.histogram(sort, dictionary)

    def dictionary(self, cursor):
        dictionary = {}
        for id, salary, tags in cursor:
            for tag in tags.split(" "):
                if tag in dictionary:
                    dictionary[tag].append({"id": id, "salary": int(salary.replace(",", '').replace("$", ''))})
                else:
                    dictionary[tag] = [{"id": id, "salary": int(salary.replace(",", '').replace("$", ''))}]
        return(dictionary)

    def popularity(self, dictionary):
        print("Im here!")
        return sorted(dictionary, key=lambda i: len(dictionary[i]), reverse=True)[5:10]

    def histogram(self, sort, dictionary):
        bins = range(0, 5000, 100)
        plt.style.use('seaborn-white')
        for i in sort:
            salary = []
            for z in dictionary[i]:
                salary.append(z["salary"])
            plt.hist(salary, bins, alpha=0.2, label=i)
        plt.xlabel("Salary")
        plt.ylabel("Number of Jobs")
        plt.title("Upwork Jobs")
        plt.legend(loc='upper right')
        plt.show()

InformationHandler()