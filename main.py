import asyncio
import json
import time
import os
import httpx
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_logo():
    console.print(Panel.fit(
        "[bold cyan] ██████████                               ███████████ █████   █████ ████   ████████ [/]\n"
        "[bold cyan]░░███░░░░███                             ░█░░░███░░░█░░███   ░░███ ░░███  ███░░░░███[/]\n"
        "[bold cyan] ░███   ░░███  ██████   ██████  ████████ ░   ░███  ░  ░███    ░███  ░███ ░░░    ░███[/]\n"
        "[bold cyan] ░███    ░███ ███░░███ ███░░███░░███░░███    ░███     ░███    ░███  ░███    ███████[/]\n"
        "[bold cyan] ░███    ░███░███████ ░███████  ░███ ░███    ░███     ░░███   ███   ░███   ███░░░░[/]\n"
        "[bold cyan] ░███    ███ ░███░░░  ░███░░░   ░███ ░███    ░███      ░░░█████░    ░███  ███      █[/]\n"
        "[bold cyan] ██████████  ░░██████ ░░██████  ░███████     █████       ░░███      █████░██████████[/]\n"
        "[bold cyan]░░░░░░░░░░    ░░░░░░   ░░░░░░   ░███░░░     ░░░░░         ░░░      ░░░░░ ░░░░░░░░░░[/]\n"
        "\n[bold yellow]© DeepTV | Telegram: [blue]https://t.me/DeepTV12[/][/]"
    ))

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def watermark(text, status="INFO", color="white"):
    timestamp = get_time()
    return f"[{timestamp}] [{status}] [bold {color}]{text}[/] [dim]— DeepTV12[/]"

async def read_tokens():
    file_path = "data.txt"
    if not os.path.exists(file_path):
        console.print(watermark("data.txt file not found!", "ERROR", "red"))
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tokens = [line.strip() for line in file.readlines() if line.strip()]
            if not tokens:
                console.print(watermark("data.txt is empty!", "WARNING", "yellow"))
                return []
            return tokens
    except Exception as e:
        console.print(watermark(f"Failed to read tokens: {e}", "ERROR", "red"))
        return []

async def tap(token):
    url = "https://api.mokl.io/public/api/clicker/tap"

    payload = {
        "count": 100,
        "energy": 100,
        "timestamp": int(time.time() * 1000)
    }

    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://play.mokl.io',
        'referer': 'https://play.mokl.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                console.print(watermark(f"Success: {response.json()}", "SUCCESS", "green"))
            else:
                console.print(watermark(f"Failed: {response.status_code} {response.text}", "ERROR", "red"))
        except httpx.HTTPError as e:
            console.print(watermark(f"Request error: {e}", "ERROR", "red"))

async def main():
    display_logo()
    
    tokens = await read_tokens()
    if not tokens:
        return
    
    while True:
        for token in tokens:
            await tap(token)
            console.print(watermark("Waiting 5 seconds before switching accounts", "INFO", "cyan"))
            await asyncio.sleep(5)

        console.print(watermark("Waiting 5 minutes before restarting all accounts", "INFO", "cyan"))
        await asyncio.sleep(5 * 60)

asyncio.run(main())
