#!/usr/bin/env python3
""" Module that queries the findwork api and return the data """
import json
import asyncio
import aiohttp
from os import getenv
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime as dt
from typing import Union, Callable, List


def url_formatter(func: Callable) -> Union[Callable, str]:
    """ Function that formats the url """
    @wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv()
        headers = {}
        headers["Authorization"] = getenv("Findwork")
        params = func(*args, **kwargs)
        return headers, params
    return wrapper


@url_formatter
def url_params(search_query: dict) -> dict:
    """ Function that formats the url params"""
    params = {}
    search = search_query.get("user_input")
    if "remote" in search_query:
        params["remote"] = "true"
        params["search"] = search
        params["sort_by"] = "relevance"
    elif "location" in search_query:
        params["search"] = search
        params["location"] = search_query.get("location")
        params["sort_by"] = "relevance"
    else:
        params["search"] = search
        params["sort_by"] = "relevance"
    return params


async def fetch(search_query: dict) -> Union[dict[str, str], str]:
    """ Function that fetches the data from the api """
    url = "https://findwork.dev/api/jobs/"
    headers, params = await asyncio.to_thread(url_params, search_query)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params,
                               headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return f"Error: {response.status}"


async def save_data(search_query: dict) -> None:
    """ Function that saves the data """
    with open("data.json", "w") as file:
        data = await fetch(search_query)
        json.dump(data, file, indent=4)


async def main(search_query: dict) -> None:
    """ Function that runs the main program """
    return await save_data(search_query)


def populate() -> List[dict[str, str]]:
    """ Function that manipulates saved data """
    with open("data.json", "r") as file:
        data = json.load(file)
        jobs = data.get("results")

        unique_res = set(frozenset({
           "role": job.get("role"),
           "job_id": job.get("id")
        }.items()) for job in jobs)

        results = [dict(item) for item in unique_res]
        return results


def job_details(detail: str, job_id: str) -> dict[str, str]:
    """ Function that returns job details """
    with open("data.json", "r") as file:
        data = json.load(file)
        jobs = data.get("results")
        for job in jobs:
            # Check each key to find the one containing the job ID
            for key, value in job.items():
                if str(value) == job_id:
                    return {
                        "Company": job.get("company_name"),
                        "Role": job.get("role"),
                        "Remote": "Yes" if job.get("remote") else "No",
                        "Location": job.get("location") if not
                        job.get("remote") else "Anywhere",
                        "Date Listed": job.get("date_posted"),
                        "Application url": job.get("url")
                    }
        return {"Error": "Job not found"}
