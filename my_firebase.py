
from firebase import firebase
import dataHandling


def main():
    data_map = dataHandling.run()
    fill_database(data_map)


def fill_database(data_map):
    db = firebase.FirebaseApplication("https://course-base-a4b41.firebaseio.com/", None)
    for i in range(0, 4):  # Empties database.
        db.delete("/period" + str(i + 1), None)

    for key in data_map.keys():  # Insert into database
        data = data_map[key]
        insert = {"name": key, "url": data["url"], "timestamps": data["timestamps"], "period": data["period"]}
        result = db.post("/period" + str(data["period"]), insert)
        print(result)


if __name__ == "__main__":
    main()
