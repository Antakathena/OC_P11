import time
from locust import (
    HttpUser,
    task,
    between,
    constant,
    SequentialTaskSet
)


class MyReqRes(SequentialTaskSet):
    """SequentialTaskSet allows to decide the order in the execution of tests"""
    @task
    def index(self):
        res = self.client.get("http://127.0.0.1:5000/")
        print("Get index status is ", res.status_code)

    @task
    def show_points_board(self):
        res = self.client.get("http://127.0.0.1:5000/show-points-board")
        print("Get show_points_board status is ", res.status_code)

    @task
    def show_summary(self):
        data = {'email': 'john@simplylift.co'}
        res = self.client.post("http://127.0.0.1:5000/show-summary", data=data)
        print("Post show_summary status is ", res.status_code)

    @task
    def book(self):
        res = self.client.get("http://127.0.0.1:5000/book/<competition>/<club>")
        print("Get book status is ", res.status_code)

    @task
    def purchase_places(self):
        data = {'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '2'}
        res = self.client.post("http://127.0.0.1:5000/purchase-places", data=data)
        print("Post purchase_places status is ", res.status_code)

    @task
    def logout(self):
        res = self.client.get("http://127.0.0.1:5000/logout")
        print("Get logout status is ", res.status_code)


class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "http://example.com"

    tasks = [MyReqRes]

