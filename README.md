# python_job_seeker
Programm to seek a freelance or permanent job in Russia for junior python developers. Developing is in progress.

1. You NEED to create "settings.json" file in "app" directory with "chat_id" and "bot_token" keys, that specify chat where you want to receive messages and telegram bot api token like this:
{
    "chat_id": "socks5://user:pass@host:port",
    "bot_token": "socks5://user:pass@host:port"
}

2. You MAY want to specify proxies in "proxies.json" file like this:
{
    "http": "socks5://user:pass@host:port",
    "https": "socks5://user:pass@host:port"
}
