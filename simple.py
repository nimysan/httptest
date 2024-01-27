from markupsafe import escape
import os
from time import time
from html import escape
from locust import stats, HttpUser, between, task, events
from flask import Blueprint, render_template, jsonify, make_response
from xml.dom import minidom
import random




class WebsiteUser(HttpUser):
    host = "http://d2w82h7h2b0a64.cloudfront.net"
    # host =
    wait_time = between(1, 3)
    cache_hits = 0;
    cache_misses = 0;
    m4s_task = "";

    @task
    def mpd(self):
        url = "/TVC4001/index.mpd"
        response = self.client.get(url)
        print("Response status code:", response.status_code)
        if response.status_code == 200:
            try:
                doc = minidom.parseString(response.text)
                self.m4s_task = doc.getElementsByTagName("SegmentTemplate")[0].getAttribute("startNumber")
                print('self.m4s_task ', self.m4s_task)
            except:
                print('Unexpected error occurred.')
                self.m4s_task = ""

        else:
            self.m4s_task = ""

    @task
    def sample_m4s(self):
        random_num = random.randint(1, 10000)
        if len(self.m4s_task) > 0 and random_num == 100:
            url = "/TVC4001/0-" + self.m4s_task + ".m4s"
            print("URL is --->", url)
            response = self.client.get(url)
            print("Response status code:", response.status_code)


stats = {}
path = os.path.dirname(os.path.abspath(__file__))
extend = Blueprint(
    "extend",
    "extend_web_ui",
    static_folder=f"{path}/static/",
    static_url_path="/extend/static/",
    template_folder=f"{path}/templates/",
)


@events.init.add_listener
def locust_init(environment, **kwargs):
    """
    We need somewhere to store the stats.

    On the master node stats will contain the aggregated sum of all content-lengths,
    while on the worker nodes this will be the sum of the content-lengths since the
    last stats report was sent to the master
    """
    if environment.web_ui:
        # this code is only run on the master node (the web_ui instance doesn't exist on workers)
        @extend.route("/content-length")
        def total_content_length():
            """
            Add a route to the Locust web app where we can see the total content-length for each
            endpoint Locust users are hitting. This is also used by the Content Length tab in the
            extended web UI to show the stats. See `updateContentLengthStats()` and
            `renderContentLengthTable()` in extend.js.
            """
            report = {"stats": []}
            if stats:
                stats_tmp = []

                for name, inner_stats in stats.items():
                    ch = inner_stats["cache-hits"]
                    tr = inner_stats["total_requests"]
                    stats_tmp.append(
                        {"name": name, "safe_name": escape(name, quote=False), "chnumber": ch, "crate": tr / ch}
                    )

                    # Truncate the total number of stats and errors displayed since a large number of rows will cause the app
                    # to render extremely slowly.
                    report = {"stats": stats_tmp[:500]}
                return jsonify(report)
            # print(jsonify(stats))
            return jsonify(stats)

        @extend.route("/extend")
        def extend_web_ui():
            """
            Add route to access the extended web UI with our new tab.
            """
            # ensure the template_args are up to date before using them
            environment.web_ui.update_template_args()
            return render_template("extend.html", **environment.web_ui.template_args)

        @extend.route("/content-length/csv")
        def request_content_length_csv():
            """
            Add route to enable downloading of content-length stats as CSV
            """
            response = make_response(content_length_csv())
            file_name = f"cache_hits_{time()}.csv"
            disposition = f"attachment;filename={file_name}"
            response.headers["Content-type"] = "text/csv"
            response.headers["Content-disposition"] = disposition
            return response

        def content_length_csv():
            """Returns the content-length stats as CSV."""
            rows = [
                ",".join(
                    [
                        '"Name"',
                        '"Total Cache-Hits"',
                    ]
                )
            ]

            if stats:
                for url, inner_stats in stats.items():
                    rows.append(f"\"{url}\",{inner_stats['cache-hits']:.2f}")
            return "\n".join(rows)

        # register our new routes and extended UI with the Locust web UI
        environment.web_ui.app.register_blueprint(extend)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, **kwargs):
    """
    Event handler that get triggered on every request
    """
    # print(
    #     f"request name is {name} and response is {response.headers.get('X-Cache')}")

    stats.setdefault(name, {"cache-hits": 0, "total_requests": 0})
    # stats.setdefault(name, {"total_requests": 0})

    if response.headers.get("X-Cache") == "Hit from cloudfront":
        stats[name]["cache-hits"] += 1

    stats[name]["total_requests"] += 1


# stats[name]["content-length"] += 1


@events.reset_stats.add_listener
def on_reset_stats():
    """
    Event handler that get triggered on click of web UI Reset Stats button
    """
    global stats
    stats = {}
