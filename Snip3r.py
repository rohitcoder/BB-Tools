import asyncio 
from aiohttp import ClientSession
import uncurl
from ssl import SSLCertVerificationError
curl_string = "PASTE_RAW_CURL_REQUEST_HERE"

def decodeCurl(curl_string):
    context = uncurl.parse_context(curl_string)
    return context 

async def fetch(url, method, data, headers, session):
    if method == "get":
        async with session.get(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "post":
        async with session.post(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "put":
        async with session.put(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "delete":
        async with session.delete(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "head":
        async with session.head(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "options":
        async with session.options(url, data=data, headers=headers) as response:
            return await response.read()
    elif method == "patch":
        async with session.options(url, data=data, headers=headers) as response:
            return await response.read()

async def run(r): 
    tasks = []
    decoded = decodeCurl(curl_string)
    url = decoded.url
    method = decoded.method
    data = decoded.data
    headers = decoded.headers
    cookies = decoded.cookies
    async with ClientSession(cookies=cookies) as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i),method,data,headers, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print("\n Printing Response\n================\n")
        print(str(responses)+"\n") 

request_count = int(input("How many request you want to send: ")) 
try:
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(run(request_count))
  loop.run_until_complete(future) 
except SSLCertVerificationError as e:
        print(e)
