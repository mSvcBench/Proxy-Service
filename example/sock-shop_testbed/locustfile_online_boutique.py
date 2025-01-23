from locust import HttpUser, TaskSet, between, constant_throughput
import random

products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z']

keep_alive = False


def index(l):
    if keep_alive:
        l.client.get("/")
    else:
        l.client.get("/", headers={"Connection": "close"}, cookies=None)


def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD']
    if keep_alive:
        l.client.post("/setCurrency",
            {'currency_code': random.choice(currencies)})
    else:
        l.client.post("/setCurrency", {'currency_code': random.choice(currencies)}, headers={"Connection": "close"}, cookies=None)


def browseProduct(l):
    if keep_alive:
        l.client.get("/product/" + random.choice(products))
    else:
        l.client.get("/product/" + random.choice(products), headers={"Connection": "close"}, cookies=None)


def viewCart(l):
    if keep_alive:
        l.client.get("/cart")
    else:
        l.client.get("/cart", headers={"Connection": "close"}, cookies=None)


def addToCart(l):
    product = random.choice(products)
    if keep_alive:
        l.client.get("/product/" + product)
        l.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])})
    else:
        l.client.get("/product/" + product, headers={"Connection": "close"}, cookies=None)
        l.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])}, headers={"Connection": "close"}, cookies=None)


def checkout(l):
    addToCart(l)
    if keep_alive:
        l.client.post("/cart/checkout", {
            'email': 'someone@example.com',
            'street_address': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'country': 'United States',
            'credit_card_number': '4432-8015-6152-0454',
            'credit_card_expiration_month': '1',
            'credit_card_expiration_year': '2039',
            'credit_card_cvv': '672',
        })
    else:
        l.client.post("/cart/checkout", {
            'email': 'someone@example.com',
            'street_address': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'country': 'United States',
            'credit_card_number': '4432-8015-6152-0454',
            'credit_card_expiration_month': '1',
            'credit_card_expiration_year': '2039',
            'credit_card_cvv': '672',
        }, headers={"Connection": "close"}, cookies=None)



class UserBehavior(TaskSet):
    def on_start(self):
        index(self)
        if not keep_alive:
            self.client.cookies.clear()
            self.client.headers.update({"Connection": "close"})

    tasks = {index: 1,
            setCurrency: 1,
            browseProduct: 1,
            addToCart: 1,
            viewCart: 1,
            checkout: 1
            }


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = constant_throughput(1)

