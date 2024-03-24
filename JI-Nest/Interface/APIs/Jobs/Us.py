#!/usr/bin/env python3
""" Module that queries the USA_Jobs api and return the data """
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
        headers["Host"] = getenv("Host")
        headers["User-Agent"] = getenv("User-Agent")
        headers["Authorization-Key"] = getenv("US_jobs")
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
        params["PositionTitle"] = search
    elif "location" in search_query:
        params["PositionTitle"] = search
        params["locationName"] = search_query.get("location")
        params["sort_by"] = "relevance"
    else:
        params["PositionTitle"] = search
    return params


async def fetch(search_query: dict) -> Union[dict[str, str], str]:
    """ Function that fetches the data from the api """
    url = "https://data.usajobs.gov/api/Search"
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
        jobs = data.get("SearchResult").get("SearchResultItems")

        unique_res = set(frozenset({
           "role": job.get("MatchedObjectDescriptor").get("PositionTitle"),
           "job_id": job.get("MatchedObjectDescriptor").get("PositionID"),
        }.items()) for job in jobs)

        results = [dict(item) for item in unique_res]
        return results


def job_details(detail: str, job_id: str) -> dict[str, str]:
    """ Function that returns job details """
    with open("data.json", "r") as file:
        data = json.load(file)
        jobs = data.get("SearchResult").get("SearchResultItems")

        for job in jobs:
            for key, value in job.items():
                if key == "MatchedObjectDescriptor" and\
                      value.get("PositionID") == job_id:
                    return {
                        "Company": job.get("MatchedObjectDescriptor")
                        .get("OrganizationName"),
                        "Role": job.get("MatchedObjectDescriptor")
                        .get("PositionTitle"),
                        "Location": job.get("MatchedObjectDescriptor")
                        .get("PositionLocationDisplay"),
                        "Date Listed": job.get("MatchedObjectDescriptor")
                        .get("PublicationStartDate"),
                        "Deadline":
                        job.get("MatchedObjectDescriptor")
                        .get("ApplicationCloseDate"),
                        "Application url": job.get("MatchedObjectDescriptor")
                        .get("ApplyURI")[0]
                    }
        return {"Error": "Job not found"}
