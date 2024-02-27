import requests
import aiohttp
import asyncio
import time

# hard coded for now
resources = [
    {"resource": "users", "url": 'http://ec2-3-144-182-9.us-east-2.compute.amazonaws.com:8012/users'},
    {"resource": "properties", "url": 'https://e6156-i-am-bezos-402423.ue.r.appspot.com/properties'},
    {"resource": "bookings", "url": 'http://ec2-3-144-93-114.us-east-2.compute.amazonaws.com:8012/bookings'}
]

class Composite:
    # helper for async
    @staticmethod
    async def fetch(session, resource):
        url = resource["url"]
        async with session.get(url) as response:
            response_data = await response.json()
            print(f"{resource['resource']} service has returned a response (in async)")
            return {
                "resource": resource["resource"],
                "data": response_data
            }

    # async
    @staticmethod
    async def fetch_async():
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(Composite.fetch(session, res)) for res in resources]
            responses = await asyncio.gather(*tasks)
            return {response["resource"]: response for response in responses}

    # sync
    @staticmethod
    def fetch_sync():
        results = {}
        for resource in resources:
            response = requests.get(resource["url"])
            print(f"{resource['resource']} service has returned a response (in sync)")
            results[resource["resource"]] = response.json()
        return results