import psycopg2
import matplotlib.pyplot as plt
import configuration as config


class InformationHandler:
    def __init__(self):
        config_data = config.Configuration().output()
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(config_data[0],
                                                                                           config_data[1],
                                                                                           config_data[2],
                                                                                           config_data[3]))
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
        return dictionary

    def popularity(self, dictionary):
        print("Im here!")
        return sorted(dictionary, key=lambda i: len(dictionary[i]), reverse=True)[5:10]

    def histogram(self, sort, dictionary):
        label_salary = []
        final_salary = []
        bins = range(0, 10000, 1000)
        plt.style.use('seaborn-white')
        for i in sort:
            final_salary.append([z["salary"] for z in dictionary[i]])
            label_salary.append(i)
        plt.hist(final_salary, bins, alpha=0.2, label=label_salary)
        plt.xlabel("Salary")
        plt.ylabel("Number of Jobs")
        plt.title("Upwork Jobs")
        plt.legend(loc='upper right')
        plt.show()


if __name__ == "__main__":
    InformationHandler()