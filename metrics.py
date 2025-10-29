import json
import requests
from prometheus_client import CollectorRegistry, push_to_gateway, Gauge, Counter

config = json.load(open("config.json"))


class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.total_steps = Counter("uitest_total_steps", "uitest_total_steps", registry=self.registry,
                                   labelnames=["desc_job", "product"])
        self.total_time = Gauge("uitest_total_time", "uitest_total_time", registry=self.registry,
                                labelnames=["desc_job", "product"])
        self.step = Gauge("uitest_step", "uitest_step", registry=self.registry,
                          labelnames=["stepname", "desc_job", "desc_step", "priority", "product", "cluster"])
        self.step_time = Gauge("uitest_step_time", "uitest_step_time", registry=self.registry,
                               labelnames=["stepname", "desc_job", "desc_step", "product"])
        self.cluster = Gauge("cluster", "cluster", registry=self.registry, labelnames=["cluster"])
        self.url = config["pushgateway-url"]
        self.product = config["product"]
        self.push_gateway_job = ""
        self.job_desc = ""
        self.priority = config["priority"]

    def set_job(self, job):
        self.push_gateway_job = job

    def set_job_desc(self, job_desc):
        self.job_desc = job_desc

    def set_priority(self, priority):
        self.priority = priority

    def push(self):
        push_to_gateway(self.url, job=self.push_gateway_job, registry=self.registry)

    def set_metrics(self, step_name, step_desc, total_time, cluster):
        self.step.labels(step_name, self.job_desc, step_desc, self.priority, self.product, cluster).set(1)
        self.cluster.labels(f"cluster {cluster}").set(cluster)
        self.step_time.labels(step_name, self.job_desc, step_desc, self.product).set(total_time)
        self.total_steps.labels(self.job_desc, self.product).inc()

    def set_fail_step_metric(self, step_name, step_desc, total_time, cluster):
        self.step.labels(step_name, self.job_desc, step_desc, self.priority, self.product, cluster).set(0)
        self.step_time.labels(step_name, self.job_desc, step_desc, self.product).set(total_time)
        self.cluster.labels(f"cluster {cluster}").set(cluster)


class MonitoringApiClient:
    def __init__(self):
        self.url = config["monitoring-api-url"]
        self.product = config["product"]
        self.job = ""
        self.desc_job = ""
        self.priority = config["priority"]
        self.last_step = ""
        self.cluster = "1"
        self.is_failed = False
        self.is_failed_timeout = False

    def set_job(self, job):
        self.job = job

    def set_job_desc(self, job_desc):
        self.desc_job = job_desc

    def set_priority(self, priority):
        self.priority = priority

    def set_last_step(self, step):
        self.last_step = step

    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_failed(self, boolean):
        self.is_failed = boolean

    def set_failed_timeout(self, boolean):
        self.is_failed_timeout = boolean

    def send_result(self):
        headers = {'content-type': 'application/json'}
        data = {
            "job": self.job,
            "jobDescription": self.desc_job,
            "product": self.product,
            "lastStep": self.last_step,
            "cluster": self.cluster,
            "priority": self.priority,
            "isFailed": self.is_failed,
            "isFailedByTimeout": self.is_failed_timeout
        }
        requests.post(self.url, json=data, headers=headers)
