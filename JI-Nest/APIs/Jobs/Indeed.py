#!/usr/bin/env python3
import asyncio
import aiohttp
import json


async def fetch(session, url):
    async with session.get(url,
                           headers={
                               "Host":
                               'data.usajobs.gov',
                               "User-Agent":
                               'spikymalcom00@gmail.com',
                               "Authorization-Key":
                               '9Q3RpAduqyC5Wn37FjfmJJ5Dq3T5MYEjqh64Bbh7S3k='
                           }) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        res = await fetch(
            session,
            'https://data.usajobs.gov/api/Search?PositionTitle=Civil%20Engineer&LocationName=New+York'
        )
        with open('us_jobs.json', 'w') as f:
            json.dump(res, f, indent=5)


def list_jobs():
    results = []
    with open('us_jobs.json') as f:
        data = json.load(f)
        for job in data['SearchResult']['SearchResultItems']:
            results.append(job['MatchedObjectDescriptor']['PositionTitle'])
        return results
