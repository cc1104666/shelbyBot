import asyncio
import random
import string
import json
from curl_cffi.requests import AsyncSession
from concurrent.futures import ThreadPoolExecutor
from cf_solver import CloudflareSolver


def build_proxy(channel, password):
    session = ''.join(random.choices(string.digits + string.ascii_letters, k=10))
    return f"http://{channel}-residential-country_ANY-r_0m-s_{session}:{password}@gate.nstproxy.io:24125"


def get_turnstile_token_sync(solver, website_url, sitekey):
    return solver.solve_turnstile(website_url, sitekey, "submit")

async def get_turnstile_token(solver, website_url, sitekey, loop=None):
    loop = loop or asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        token = await loop.run_in_executor(pool, get_turnstile_token_sync, solver, website_url, sitekey)
    return token

async def submit_form(email, config, solver):
    proxy = build_proxy(config['nstproxy_Channel'], config['nstproxy_Password'])
    session = AsyncSession(timeout=60, proxies={"http": proxy, "https": proxy}, impersonate="chrome110")

    token = await get_turnstile_token(solver, config['website_url'], config['turnstile_sitekey'])

    payload = {
        "email": email,
        "extra_field": "",
        "form_timestamp": int(asyncio.get_event_loop().time() * 1000),
        "turnstileToken": token
    }
    headers = {
        "Referer": config["website_url"],
        "Origin": config["website_url"]
    }

    try:
        resp = await session.post(config['hubspot_api_url'], json=payload, headers=headers)
        print(f"[{email}] 状态码: {resp.status_code}, 响应: {resp.text}")
    except Exception as e:
        print(f"[{email}] 提交异常: {e}")
    session.close()

async def main():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    with open('emails.txt', 'r', encoding='utf-8') as ef:
        emails = [line.strip() for line in ef if line.strip()]
    solver = CloudflareSolver(config['capmonster_api_key'])

    for email in emails:
        await submit_form(email, config, solver)

        await asyncio.sleep(config.get('delay_between_requests', 15.0))

if __name__ == "__main__":
    asyncio.run(main())
