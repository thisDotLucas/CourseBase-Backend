
from firebase import firebase
import dataHandling


def main():
    data_map = dataHandling.run()
    fill_database(data_map)


def fill_database(data_map):
    db = firebase.FirebaseApplication("https://*****************.firebaseio.com/", None)
    db.delete("/courses", None)

    for key in data_map.keys():
        data = data_map[key]
        insert = {"name": key, "url": data["url"], "timestamps": data["timestamps"], "period": data["period"]}
        result = db.post("/courses", insert)
        print(result)


if __name__ == "__main__":
    main()
