import os
import cv2
import json

# upload image to correct location in database
def upload(name, image, num):
    """
        :type name: str
              image: List[List[List[int]]] (numpy array)
              num: int
        :rtype: N/A
    """
    file_path = "db/imgs/" + name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = name + "-" + str(num) + ".jpg"
    destination = file_path + "/" + file_name
    cv2.imwrite(destination, image)
    return

# adds a new person to people.json
def add_person(index, name, label):
    """
        :type index: int
              name: str
              laebl: str
        :rtype: N/A
    """
    if index == 0:
        people_json = {}
        people_json["num_people"] = 1
        people_json["people"] = {}
    else:
        with open("db/people.json", "r") as f:
            people_json = json.load(f)
        people_json["num_people"] = people_json["num_people"] + 1
    people_json["people"][name] = label
    with open("db/people.json", "w") as f:
        json.dump(people_json, f, indent=4)
    return

