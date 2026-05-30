from locust import HttpUser, task, between

class TaskeyUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/login",
            data={
                "email": "alaa.badawy404@gmail.com",
                "password": "3360639"
            },
            allow_redirects=True
        )

        print("LOGIN STATUS:", response.status_code)
        print("COOKIES:", self.client.cookies.get_dict())

    @task(3)
    def get_tasks(self):
        self.client.get("/profile/upcoming", allow_redirects=True)

    @task(1)
    def create_task(self):
        self.client.post("/profile/create", data={
            "task_name": "Load Test Task",
            "title": "Testing",
            "task_description": "Testing load",
            "priority": "low",
            "due_date": "2026-06-01",
            "group_name": "test"
        }, allow_redirects=True)