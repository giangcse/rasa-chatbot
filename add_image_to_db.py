import pymongo
import json
while True:
    link = str(input("Link: "))
    url = pymongo.MongoClient("mongodb://127.0.0.1/")
    mydb = url['Zalo']
    img_col = mydb['zoa_images']
    # if link is not "":
    #     if "https://i.imgur.com/" in link:
    #         _is_exists = img_col.count_documents({"url": link})
    #         if _is_exists == 0:
    #             count = img_col.count_documents({})
    #             img_col.insert_one({"id": count, "url":link})
    #             print("Image", link, "has been added into database.")
    #         else:
    #             print("Image is exists")
    #     else:
    #         print("URL does not imgur")
    # else:
    #     print("This is not URL")
    import random

    max_id = img_col.count_documents({})
    rand_id = random.randint(0, int(max_id))
    print(img_col.find_one({"id": rand_id})['url'])