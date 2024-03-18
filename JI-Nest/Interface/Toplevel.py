#!/usr/bin/env python3
import os
import toml
import json
import time
import textwrap
import subprocess
import Serp as sp
import Findwork as fw
from uuid import uuid4
from redis import Redis
import customtkinter as ctk
from datetime import timedelta


Config_specs = os.path.normpath(
    f"{os.path.expanduser('~')}/portfolio_projects/Jobs_and_Internships-Nest/config.toml")


class TopLevelWindow(ctk.CTkToplevel):
    """ Class that creates the top level windows for the app"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.geometry("400x300")
        self.resizable(False, False)

        # Configure grid rows and columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top level window frame
        self.details = ResultsFrame(self)
        self.details.grid(row=0, column=0, sticky="nsew")

    def display_instructions(self):
        """ Function that displays the instructions for using the app """
        app_name, app_usage = get_config()
        self.title("App Usage")
        instructions = ctk.CTkLabel(self, text=app_usage)
        instructions.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def pull_details(self, Query):
        """ Function that displays the details of the search result """
        self.title("Saved Details")
        if Query and isinstance(Query, dict):
            num, detail = Query.get("no_details"), Query.get("details")

            if detail == "Jobs":
                nm = int(num)
                db = 2
                details = details_pull(db, nm)
                self.details.populate_pulled_details(details)
            elif detail == "Internships":
                nm = int(num)
                db = 3
                details = details_pull(db, nm)
                self.details.populate_pulled_details(details)
        else:
            pass

        # details = ctk.CTkLabel(self, text="Pulled Details")
        # details.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def display_details(self, detail, engine, job_id):
        """ Function that displays the details of the search result """
        self.title("Details")
        if engine == "Findwork":
            results = fw.job_details(detail, job_id)
            self.details.populate_details(results)
        elif engine == "Serp":
            results = sp.job_details(detail, job_id)
            self.details.populate_details(results)
        else:
            pass
        # details = ctk.CTkLabel(self, text="Details")
        # details.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def error_input_details(self):
        """ Function that displays an error message when the user selects
            both remote and country """
        self.title("Error")
        self.geometry("300x100")
        error_message = ctk.CTkLabel(self, text="Please select either remote"
                                     " or country, not both")
        error_message.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def error_missing_input(self):
        """ Function that displays an error message when the user does not
            enter any input """
        self.title("Error")
        self.geometry("300x100")
        error_message = ctk.CTkLabel(self, text="Please enter a search input")
        error_message.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def error_missing_query(self):
        """ Function that displays an error message when the user does not
            enter any input """
        self.title("Error")
        self.geometry("300x100")
        error = """You have to enter the number of details to pull as well
                as the Description of the details to pull"""
        error_message = ctk.CTkLabel(self, text=textwrap.fill(error, width=30),
                                     text_color="red", height=5)
        error_message.grid(row=0, column=0, padx=(10, 30), pady=10,
                           sticky="ew", columnspan=2)


class PullFrame(ctk.CTkFrame):
    """ class that populates pulled details """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Frame configs
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # # Populate the frame with the pulled details
        # self.populate_details(result)

    def populate_details(self, result):
        """ Function that populates the pop up window """
        if result and isinstance(result, tuple) and len(result) == 2:
            val = result[1]
            det_dict = json.loads(val)
            for idx, (k, v) in enumerate(det_dict.items()):
                wrapped_k, wrapped_v = textwrap.fill(k, width=20), \
                    textwrap.fill(v, width=30)
                detail_label = ctk.CTkLabel(self,
                                            text=f"{wrapped_k}: ")
                detail_label.grid(row=idx, column=0,  padx=(10, 0),
                                  pady=10, sticky="w")

                if k == "Application url":
                    detail_button = ctk.CTkButton(self, text="Apply",
                                                  command=lambda
                                                  url=v: open_url(url))
                    detail_button.grid(row=idx, column=0, padx=(115, 10),
                                       pady=10, sticky="w")
                else:
                    detail_value = ctk.CTkLabel(self, text=wrapped_v)
                    detail_value.grid(row=idx, column=0, padx=(115, 10),
                                      pady=10, sticky="w")


class ResultsFrame(ctk.CTkScrollableFrame):
    """ Class that creates a scrollable frame for the pop up window """
    def __init__(self, master, **kwargs):
        """ Function that initializes the results frame """
        super().__init__(master, **kwargs)

        # Result details
        self.results = {}

        # Frame configs
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def populate_details(self, results):
        """" Function that populates the pop up window """
        if results and isinstance(results, dict):
            self.results = results
            for index, (k, v) in enumerate(results.items()):
                wrapped_k, wrapped_v = textwrap.fill(k, width=20), \
                    textwrap.fill(v, width=30)
                detail_label = ctk.CTkLabel(self,
                                            text=f"{wrapped_k}: ")
                detail_label.grid(row=index, column=0,  padx=(10, 0), pady=10,
                                  sticky="w")

                if k == "Application url":
                    detail_button = ctk.CTkButton(self, text="Apply",
                                                  command=lambda
                                                  url=v: open_url(url))
                    detail_button.grid(row=index, column=0, padx=(115, 10),
                                       pady=10, sticky="w")
                else:
                    detail_value = ctk.CTkLabel(self, text=wrapped_v)
                    detail_value.grid(row=index, column=0, padx=(115, 10),
                                      pady=10, sticky="w")

            save_button = ctk.CTkButton(self, text="Save",
                                        command=self.save_details,
                                        corner_radius=10, width=90)
            save_button.grid(row=len(results), column=0, padx=(250, 0),
                             pady=10, sticky="w")

        else:
            pass

    def populate_pulled_details(self, pulled_details):
        """ Function that populates the frame with pulled details """
        if pulled_details and isinstance(pulled_details, list):
            for index, detail in enumerate(pulled_details):
                pull_frame = PullFrame(self)
                pull_frame.grid(row=index, column=0, padx=10,
                                pady=10, sticky="nsew")
                pull_frame.populate_details(detail)

    def save_details(self):
        """ Function that saves the details of the search result """
        job_details = self.results
        job = json.dumps(job_details)
        rs = Redis(host="localhost", port=6340, db=2, decode_responses=True)

        if not rs.exists("insertion_order"):
            rs.zadd("insertion_order", {"SortedSet": time.time()})

        for key in rs.scan_iter():
            if rs.type(key) == 'string':
                existing_job = rs.get(key)

                if existing_job == job:
                    time_rem = rs.ttl(key)
                    rs.delete(key)
                    rs.setex(key, time_rem, job)
                    rs.zadd("insertion_order", {key: time.time()})
                    return

        job_sid = f"Job:{str(uuid4())}"
        rs.setex(job_sid, timedelta(weeks=5), job)
        rs.zadd("insertion_order", {job_sid: time.time()})


def details_pull(db, n):
    """ Function that pulls details from Redis based on the db and
        retrieves the last n items """
    rs = Redis(host="localhost", port=6340, db=db, decode_responses=True)

    # Retrieve the keys of the last n items from the sorted set
    last_n_keys = rs.zrevrange("insertion_order", 0, n - 1)

    # Fetch the values corresponding to the keys
    last_n_values = []
    for key in last_n_keys:
        value = rs.get(key)
        last_n_values.append((key, value))

    return last_n_values


def open_url(url):
    """ Function that opens the application url """
    chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
    subprocess.run([chrome_path, url], check=True)


def get_config():
    """ Function that gets the configuration details for the app """
    try:
        configs = toml.load(Config_specs)
        app_name = configs['project']['name']
        app_usage = configs['App_Usage']['Instructions']
        return app_name, app_usage
    except FileNotFoundError:
        print(f"Configuration file {Config_specs} not found")
        return None, None
    except toml.TomlDecodeError as e:
        print(f"Error decoding {Config_specs}: {e}")
        return None, None
