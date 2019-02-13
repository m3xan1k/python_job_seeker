import scraper
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)


with open('bot_settings.json') as f:
    bot_settings = json.load(f)

with open('proxies.json') as f:
    proxies = json.load(f)

chat_id = bot_settings['chat_id']
bot_token = bot_settings['bot_token']
url = f'https://api.telegram.org/bot{bot_token}/'

def get_updates():
    r = requests.get(url + 'getUpdates', proxies=proxies)
    print(r.text)

def format_job(job):
    normalized_text = f'{job.title}\n{job.pub_date}\n{job.price}\n{job.link}\n\n\n'
    return normalized_text

def send_all(chat_id, bot_token):
    all_jobs = scraper.get_all()
    for job in all_jobs:
        text = format_job(job)
        full_url = url + f'sendMessage?chat_id={chat_id}&text={text}'
        r = requests.get(full_url, proxies=proxies)


def main():
    send_all(chat_id, bot_token)



if __name__ == '__main__':
    main()
