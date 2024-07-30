# DogsHouse-Bot
Bot for https://t.me/dogshouse_bot

My tg: https://t.me/Zzjjjuuu

Thanks to ApeCryptor:
[ApeCryptor](https://t.me/+_xCNXumUNWJkYjAy "ApeCryptor") 🦧

## Functionality
| Functional                                                       | Supported |
|------------------------------------------------------------------|:---------:|
| Multithreading                                                   |     ✅     |
| Binding a proxy to a session                                     |     ✅     |
| Auto-login                                                       |     ✅     |
| Auto task completion | ✅ |
| Flexible auto ref system with special generated file with refs of all accounts |  ✅ |
| Random sleep time between accounts, complete tasks, claim points |     ✅     |
| Support pyrogram .session                                        |     ✅     |
| Get statistics for all accounts                                  |     ✅     |

## Settings data/config.py
| Setting                      | Description                                                                                    |
|------------------------------|------------------------------------------------------------------------------------------------|
| **REF_LINKS: how much refs you need** | Your ref links and how much refs you need on account (5 recommended) |  
| **API_ID / API_HASH (in api_config.json)**        | Platform data from which to launch a Telegram session                                          |
| **DELAYS-ACCOUNT**           | Delay between connections to accounts (the more accounts, the longer the delay)                |
| **PROXY_TYPE**               | Proxy type for telegram session                                                                |
| **WORKDIR**                  | directory with session                                                                         |

## Requirements
- Python 3.12 (you can install it [here](https://www.python.org/downloads/release/python-390/)) 
- Telegram API_ID and API_HASH (you can get them [here](https://my.telegram.org/auth))

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage
1. Run the bot:
   ```bash
   python main.py
   ```
