#!/usr/bin/env python3
""" Module that queries the serp api and return the data """
import json
import asyncio
import aiohttp
from os import getenv
from dotenv import load_dotenv
from typing import Union, Callable, List


def url_params(search_query: dict) -> dict:
    """ Function that formats the url params"""
    if search_query:
        load_dotenv()
        params = {}
        search = search_query.get("user_input")
        params["engine"] = "google_jobs"
        params["api_key"] = getenv("Serp")
        if "remote" in search_query:
            params["ltype"] = 1
            params["q"] = search
        elif "location" in search_query:
            params["q"] = search
            params["location"] = search_query.get("location")
        else:
            params["q"] = search
        return params
    return {}


async def fetch(session: aiohttp.ClientSession, search_query: dict) -> Union[dict[str, str], str]:
    """ Function that fetches the data from the api """
    url = "https://serpapi.com/search"
    params = url_params(search_query)
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        return f"Error: {response.status}"


async def save_data(session: aiohttp.ClientSession, search_query: dict) -> None:
    """ Function that saves the data """
    with open("data.json", "w") as file:
        data = await fetch(session, search_query)
        json.dump(data, file, indent=4)


async def main(search_query: dict) -> None:
    """ Function that runs the main program """
    async with aiohttp.ClientSession() as session:
        return await save_data(session, search_query)


def populate() -> List[dict[str, str]]:
    """ Function that populates the data """
    with open("data.json", "r") as file:
        data = json.load(file)
        jobs = data.get("jobs_results")

        unique_res = set(frozenset({
           "role": job.get("title"),
           "job_id": job.get("job_id")
        }.items()) for job in jobs)

        results = [dict(item) for item in unique_res]
        return results


def job_details(detail: str, job_id: str) -> dict[str, str]:
    """ Function that returns job details """
    with open("data.json", "r") as file:
        data = json.load(file)
        jobs = data.get("jobs_results")
        for job in jobs:
            for key, value in job.items():
                if str(value) == job_id:
                    return {
                        "Company": job.get("company_name"),
                        "Role": job.get("title"),
                        "Remote": "Yes" if job["location"] == " Anywhere "
                        else "No",
                        "Location": job["location"] if job["location"] !=
                        " Anywhere " else "Anywhere",
                        "Date posted": job.get("detected_extensions", "null")
                        .get("posted_at", "null"),
                        "Schedule": job.get("detected_extensions", "null")
                        .get("schedule_type", "null")
                    }
        return {f"{detail}": "No details found"}
