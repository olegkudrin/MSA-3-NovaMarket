from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://192.168.49.2:30080"

    @task
    def index(self):
        self.client.get("/")
