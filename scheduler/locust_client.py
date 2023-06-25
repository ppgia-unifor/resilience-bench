import gevent
from locust import HttpUser, task, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
from models import Workload

setup_logging("INFO", None)


class MyUser(HttpUser):
    host = "https://docs.locust.io"

    @task
    def t(self):
        self.client.get("/")


class Locust():

    def __init__(self):
        # setup Environment and Runner
        self._env = Environment(user_classes=[MyUser], events=events)
        self._runner = self._env.create_local_runner()

    def start(self, workload: Workload):
        # start a WebUI instance
        web_ui = self._env.create_web_ui("127.0.0.1", 8089)

        # execute init event handlers (only really needed if you have registered any)
        self._env.events.init.fire(environment=self._env, runner=self._runner, web_ui=web_ui)

        # start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(self._env.stats))

        # start a greenlet that save current stats to history
        gevent.spawn(stats_history, self._env.runner)

        # start the test
        self._runner.start(workload.users, spawn_rate=10)

        # in 60 seconds stop the runner
        gevent.spawn_later(workload.duration, lambda: self._runner.quit())

        # wait for the greenlets
        self._runner.greenlet.join()

        # stop the web server for good measures
        web_ui.stop()