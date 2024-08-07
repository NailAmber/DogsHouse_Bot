import json
import random
import re
import time
from datetime import datetime, timezone, timedelta
from utilities.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
import os
import ast
from pyrogram import Client, raw
from filelock import FileLock
from random import randrange

class DogsHouse:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.reference, self.telegram_id = None, None
        self.ref_code = 'jq3HuDDdRoWMYOsHBK9JdQ'
        self.proxy = f"{config.PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None
        self.user_agent_file = "sessions/user_agents.json"
        self.dogs_ref_file = 'data/dogs_ref_links.json'

        if proxy:
            proxy = {
                "scheme": config.PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        # headers = {'User-Agent': UserAgent(os='android').random}
        # self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)


    async def init_async(self, proxy):
        # self.refferal_link = await self.get_ref_link()
        user_agent = await self.get_user_agent()
        headers = {'User-Agent': user_agent}
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)
        self.initialized = True


    @classmethod
    async def create(cls, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        instance = cls(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
        await instance.init_async(proxy)
        return instance
    
    # Функция для чтения и парсинга файла
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    # Функция для изменения значения в словаре
    def modify_value(self, content, target_key, decrement):
        ref_link_start = content.find("REF_LINK = {")
        ref_link_end = content.find("}", ref_link_start) + 1

        ref_link_str = content[ref_link_start:ref_link_end]
        ref_link_str_cleaned = ref_link_str.split('=', 1)[1].strip()

        ref_link_dict = ast.literal_eval(ref_link_str_cleaned)

        if target_key in ref_link_dict:
            new_value = ref_link_dict[target_key] - decrement
            ref_link_dict[target_key] = max(new_value, 0)

        updated_ref_link_str = f"REF_LINK = {ref_link_dict}"
        updated_content = content[:ref_link_start] + updated_ref_link_str + content[ref_link_end:]

        return updated_content, ref_link_dict

    # Функция для сохранения измененного содержимого в файл
    def write_file(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)


    async def get_ref_link(self):
        # Пробуем получить чат по username бота
        try:
            await self.client.connect()
            
            bot_username = "dogshouse_bot"
            bot = await self.client.get_users(bot_username)
            messages = self.client.get_chat_history(bot.id, limit=1)
            
            async for message in messages:
                logger.info(f"DogHouse | Thread {self.thread} | {self.account} | Chat found")
                await self.client.disconnect()
                return "jq3HuDDdRoWMYOsHBK9JdQ"
            else:
                file_path = 'data/config.py'
                lock_path = file_path + '.lock'
                lock = FileLock(lock_path)

                ref_link_to_return = None

                # Используем синхронную блокировку внутри асинхронного кода
                with lock:
                    content = self.read_file(file_path)

                    # Получаем словарь REF_LINK из содержимого файла
                    ref_link_start = content.find("REF_LINK = {")
                    ref_link_end = content.find("}", ref_link_start) + 1
                    ref_link_str = content[ref_link_start:ref_link_end]
                    ref_link_str_cleaned = ref_link_str.split('=', 1)[1].strip()
                    ref_link_dict = ast.literal_eval(ref_link_str_cleaned)

                    # Находим первый подходящий ref_link и уменьшаем его значение
                    for ref_link in ref_link_dict:
                        if ref_link_dict[ref_link] > 0:
                            updated_content, ref_link_dict = self.modify_value(content, ref_link, 1)
                            self.write_file(file_path, updated_content)
                            ref_link_to_return = ref_link
                            logger.info(f"DogHouse | Thread {self.thread} | {self.account} | Ref link {ref_link}")
                            break

                await self.client.disconnect()

                if ref_link_to_return:
                    return ref_link_to_return.split('startapp=')[1]
                else:
                    return "jq3HuDDdRoWMYOsHBK9JdQ"
                
        except Exception as e:
            print("Error:", e)    

    async def get_user_agent(self):
        user_agents = await self.load_user_agents()
        if self.account in user_agents:
            return user_agents[self.account]
        else:
            new_user_agent = UserAgent(os='ios').random
            user_agents[self.account] = new_user_agent
            await self.save_user_agents(user_agents)
            return new_user_agent
        

    async def load_user_agents(self):
        if os.path.exists(self.user_agent_file):
            with open(self.user_agent_file, "r") as f:
                return json.load(f)
        else:
            return {}
        

    async def save_user_agents(self, user_agents):
        os.makedirs(os.path.dirname(self.user_agent_file), exist_ok=True)
        with open(self.user_agent_file, "w") as f:
            json.dump(user_agents, f, indent=4)


    async def make_tasks(self):

        try:
            await self.client.connect()
            await self.client.join_chat('dogs_community')
            await asyncio.sleep(1)
            await self.client.join_chat('notcoin')
            await asyncio.sleep(1)
            await self.client.join_chat('blumcrypto')
            await self.client.disconnect()
        except:
            logger.error(f"DogHouse | Thread {self.thread} | {self.account} | error")
        await asyncio.sleep(2)
        resp = await self.session.get(f'https://api.onetime.dog/tasks?user_id={self.telegram_id}&reference={self.reference}')
        tasks = await resp.json()
        for task in tasks:
            resp = await self.session.post(f'https://api.onetime.dog/tasks/verify?task={task['slug']}&user_id={self.telegram_id}&reference={self.reference}')
            resp_json = await resp.json()
            if 'success' in resp_json and resp_json['success'] == True:
                logger.success(f"DogHouse | Thread {self.thread} | {self.account} | {task['slug']} success!")
                await asyncio.sleep(2)

    async def change_Nickname(self):
        try:
            await self.client.connect()
            user = await self.client.get_me()
            
            if '🦴' not in user.first_name:
                await self.client.update_profile(first_name=f"{user.first_name}🦴")
            
            await self.client.disconnect()
        except:
            return None
        
    async def load_dogs_ref(self):
        if os.path.exists(self.dogs_ref_file):
            with open (self.dogs_ref_file, 'r') as f:
                return json.load(f)
        else:
            return {}
        
    async def save_dogs_ref(self, refs):
        os.makedirs(os.path.dirname(self.dogs_ref_file), exist_ok=True)
        with open(self.dogs_ref_file, 'w') as f:
            json.dump(refs, f, indent=4)

    async def stats(self):
        balance, age = await self.login()
        # ['Phone number', 'Name', 'Balance', 'Leaderboard', 'Age', 'Referrals', 'Referral link', 'Proxy (login:password@ip:port)']

        r = await (await self.session.get(f'https://api.onetime.dog/leaderboard?user_id={self.telegram_id}')).json()
        leaderboard = r.get('me').get('score')

        r = await (await self.session.get(f'https://api.onetime.dog/frens?user_id={self.telegram_id}&reference={self.reference}')).json()
        referrals = r.get('count')
        frens = [username['username'] for username in r.get('frens')]
        referral_link = f'https://t.me/dogshouse_bot/join?startapp={self.reference}'

        await self.logout()

        await self.client.connect()
        me = await self.client.get_me()
        phone_number, name = "'" + me.phone_number, f"{me.first_name} {me.last_name if me.last_name is not None else ''}"
        await self.client.disconnect()

        proxy = self.proxy.replace('http://', "") if self.proxy is not None else '-'

        return [phone_number, name, str(balance), str(leaderboard), str(age), str(referrals), str(frens), referral_link, proxy]

    async def logout(self):
        await self.session.close()

    async def login(self):
        
        
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        # self.ref_code = await self.get_ref_link()
        query = await self.get_tg_web_data()

        if query is None:
            logger.error(f"DogHouse | Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None, None

        r = await (await self.session.post(f'https://api.onetime.dog/join?invite_hash={self.ref_code}', data=query)).json()
        self.reference = r.get('reference')
        self.telegram_id = r.get('telegram_id')

        refs = await self.load_dogs_ref()
        if self.reference not in refs:
            refs[self.reference] = randrange(5,7)
            await self.save_dogs_ref(refs)

        await self.session.get(f'https://api.onetime.dog/rewards?user_id={self.telegram_id}')

        return r.get('balance'), r.get('age')

    async def get_tg_web_data(self):
        legit_ref = False
        refs = await self.load_dogs_ref()
        if refs != {}:
            for ref in refs:
                if refs[ref] > 0:
                    self.ref_code = ref
                    legit_ref = True
                    break
        try:
            await self.client.connect()
            
            bot_username = "dogshouse_bot"
            bot = await self.client.get_users(bot_username)
            messages = self.client.get_chat_history(bot.id)
            found_message = False   
            async for message in messages:
                found_message = True
                # Обрабатываем сообщение (или выполняем любую другую логику)
                pass
            if not found_message:
                refs[ref] -= 1
                logger.info(f"DogHouse | Thread {self.thread} | {self.account} | Login under ref link {ref}")
                await self.save_dogs_ref(refs)

            
            bot_username = 'dogshouse_bot'
            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer(bot_username),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer(bot_username), short_name="join"),
                platform='ios',
                write_allowed=True,
                start_param=self.ref_code
            ))
            
            

            await self.client.disconnect()
            auth_url = web_view.url
            query = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            return query

        except:
            return None
