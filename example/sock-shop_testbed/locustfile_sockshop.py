import base64

from locust import FastHttpUser, HttpUser, TaskSet, task, constant_throughput, between
import locust as lc
from random import randint, choice
import itertools, time

user_id_counter = itertools.count()
main_host = "http://160.80.223.224:30309"
# main_host = "http://192.168.10.90:30309"

class RegTasks(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = next(user_id_counter)+100
    @task
    def reg(self):
        self.client.get("/")
        username = f"u{self.user_id}"
        password = "password"
        info = {"username":f"{username}","password":f"{password}","email":"","firstName":"", "lastName":""}
        response = self.client.post("/register", json=info)
        info = {"number": "1","street": "1","city": "1","postcode": "1","country": "1"}
        response = self.client.post("/addresses", json=info)
        self.client.get("/card")
        info = {"longNum": "12345", "expires": "1", "ccv": "1"}
        response = self.client.post("/cards", json=info)


class WebTasks(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assign a unique user ID
        self.user_id = next(user_id_counter)+100

    @task
    def load(self):
        username = f"u{self.user_id}"
        password = "password"
        headers={"Authorization": "Basic " + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")}
        self.client.get("/")
        self.client.get("/login", headers=headers)

        self.client.get("/category.html")
        catalogue = self.client.get("/catalogue").json()
        while True:
            category_item = choice(catalogue)
            item_id = category_item["id"]
            if item_id != "03fef6ac-1896-4ce8-bd69-b798f85c6e0b":
                break
        self.client.get("/detail.html?id={}".format(item_id))
        catalogue = self.client.get("/catalogue").json()
        while True:
            category_item = choice(catalogue)
            item_id = category_item["id"]
            if item_id != "03fef6ac-1896-4ce8-bd69-b798f85c6e0b":
                break
        self.client.get("/detail.html?id={}".format(item_id))
        catalogue = self.client.get("/catalogue").json()
        while True:
            category_item = choice(catalogue)
            item_id = category_item["id"]
            if item_id != "03fef6ac-1896-4ce8-bd69-b798f85c6e0b":
                break
        self.client.get("/detail.html?id={}".format(item_id))

        self.client.get("/basket.html")

        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.post("/orders")

        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.post("/orders")

        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.post("/orders")

        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.post("/orders")

        self.client.get("/",headers={'Connection':'close'},cookies=None)
        # python random sleep
        # time.sleep(randint(1, 5)/1000)

class Web(HttpUser):
    # tasks = [RegTasks]
    tasks = [WebTasks]
    host = main_host
    n_ops = 23
    # wait_time = between(10000,10000)
    # wait_time = constant_throughput(2.5/n_ops)
    wait_time = constant_throughput(5.0/n_ops)
    # wait_time = constant_throughput(1.66/n_ops)

#     # wait_time = constant_throughput(12.0/n_ops)

# class siteUser(FastHttpUser):
    # network_timeout = 15.0
    # connection_timeout = 15.0
    # tasks = [WebTasks]
    # host = main_host
    # n_ops = 23

    # wait_time = constant_throughput(5.0/n_ops)
