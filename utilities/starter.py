import random
from utilities.dogs import DogsHouse
from data import config
from utilities.core import logger
import datetime
import pandas as pd
from utilities.core.telegram import Accounts
import asyncio
import os


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    dogs = await DogsHouse.create(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'
    try:
        balance, age = await dogs.login()
        await asyncio.sleep(2)
        await dogs.change_Nickname()
        await asyncio.sleep(2)
        await dogs.make_tasks()
        logger.success(f'DogHouse | Thread {thread} | {account} | Account age: {age}; Balance: {balance}')
        await dogs.logout()
    except Exception as e:
        logger.error(f'DogHouse | Thread {thread} | {account} | Error: {e}')


async def stats():
    accounts = await Accounts().get_accounts()

    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        dog_instance = await DogsHouse.create(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
        tasks.append(asyncio.create_task(dog_instance.stats()))

    data = await asyncio.gather(*tasks)

    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Phone number', 'Name', 'Balance', 'Leaderboard', 'Age', 'Referrals', 'Referral link', 'Proxy (login:password@ip:port)']

    if not os.path.exists('statistics'): os.mkdir('statistics')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')

    logger.success(f"Saved statistics to {path}")
