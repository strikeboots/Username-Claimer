import requests
import random
import string
import time
from colorama import Fore, Style, init
import sys

# Initialize Colorama
init(autoreset=True)

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}

 ▄████▄   ██▓    ▄▄▄       ██▓ ███▄ ▄███▓▓█████  ██▀███  
▒██▀ ▀█  ▓██▒   ▒████▄    ▓██▒▓██▒▀█▀ ██▒▓█   ▀ ▓██ ▒ ██▒
▒▓█    ▄ ▒██░   ▒██  ▀█▄  ▒██▒▓██    ▓██░▒███   ▓██ ░▄█ ▒
▒▓▓▄ ▄██▒▒██░   ░██▄▄▄▄██ ░██░▒██    ▒██ ▒▓█  ▄ ▒██▀▀█▄  
▒ ▓███▀ ░░██████▒▓█   ▓██▒░██░▒██▒   ░██▒░▒████▒░██▓ ▒██▒
░ ░▒ ▒  ░░ ▒░▓  ░▒▒   ▓▒█░░▓  ░ ▒░   ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░  ▒   ░ ░ ▒  ░ ▒   ▒▒ ░ ▒ ░░  ░      ░ ░ ░  ░  ░▒ ░ ▒░
░          ░ ░    ░   ▒    ▒ ░░      ░      ░     ░░   ░ 
░ ░          ░  ░     ░  ░ ░         ░      ░  ░   ░     
░                                                                                                               
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT}        Username Availability Checker{Style.RESET_ALL}
"""

def random_letters(n):
    characters = string.ascii_lowercase + string.digits + "._"
    return ''.join(random.choice(characters) for _ in range(n))

def check_user_status(letter_count, interval, platform_url, save_to_file=True, webhook_url=None):
    while True:
        random_suffix = random_letters(letter_count)
        url = platform_url + random_suffix

        try:
            response = requests.get(f"https://{url}")

            if "This user is not claimed" in response.text:
                status = f"{Fore.GREEN}[UNCLAIMED]"
                if save_to_file:
                    with open("unclaimed.txt", "a") as file:
                        file.write(f"{url}\n")
                if webhook_url:
                    payload = {"content": f"Unclaimed username found: {url} @everyone"}
                    try:
                        requests.post(webhook_url, json=payload)
                    except Exception as e:
                        print(f"{Fore.RED}Webhook failed: {e}")
            else:
                status = f"{Fore.RED}[CLAIMED]"

            print(f"{Fore.MAGENTA}URL: {platform_url}{random_suffix} {status}")

        except Exception as e:
            print(f"{Fore.YELLOW}Error accessing {url}: {e}")

        time.sleep(interval)

if __name__ == "__main__":
    print(BANNER)
    print(f"{Fore.YELLOW}Choose a platform to search for usernames:\n")
    print(f"{Fore.CYAN}1.{Fore.WHITE} guns.lol")
    print(f"{Fore.CYAN}2.{Fore.WHITE} coming soon")

    choice = input(f"{Fore.GREEN}Enter choice (1 or 2): {Fore.WHITE}").strip()

    if choice == "1":
        platform_url = "guns.lol/"
    elif choice == "2":
        platform_url = "coming soon"
    else:
        print(f"{Fore.RED}Invalid choice. Exiting...")
        sys.exit()

    try:
        letter_count = int(input(f"{Fore.GREEN}How many letter usernames to check? {Fore.WHITE}"))
        if letter_count <= 0:
            print(f"{Fore.RED}Letter count must be positive.")
            sys.exit()

        interval = float(input(f"{Fore.GREEN}Delay between checks (seconds, e.g., 0.1): {Fore.WHITE}"))
        if interval <= 0:
            print(f"{Fore.RED}Delay must be positive.")
            sys.exit()

        save_to_file = input(f"{Fore.GREEN}Save unclaimed usernames to file? (Y/N): {Fore.WHITE}").strip().lower() == 'y'
        use_webhook = input(f"{Fore.GREEN}Send to Discord webhook? (Y/N): {Fore.WHITE}").strip().lower()

        webhook_url = None
        if use_webhook == 'y':
            webhook_url = input(f"{Fore.GREEN}Enter Discord webhook URL: {Fore.WHITE}").strip()

        print(f"\n{Fore.CYAN}Starting search on {platform_url}...\n")
        check_user_status(letter_count, interval, platform_url, save_to_file, webhook_url)

    except ValueError:
        print(f"{Fore.RED}Invalid number entered.")
