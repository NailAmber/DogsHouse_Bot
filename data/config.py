# your ref link and countdown for refs by (OLD SYSTEM, NOT USING)
# REF_LINK = {'https://t.me/dogshouse_bot/join?startapp=jq3HuDDdRoWMYOsHBK9JdQ': 1, 'https://t.me/dogshouse_bot/join?startapp=x8Cd2Z_rSAO2GpXMMsztrA': 5}

DELAYS = {
    'ACCOUNT': [5, 30],  # delay between connections to accounts (the more accounts, the longer the delay)
    'SLEEP': [5, 60*20] # sleep time
}

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30