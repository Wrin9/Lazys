import asyncio
import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore

class WebsiteValidator:
    def __init__(self, url_list):
        self.url_list = url_list

    async def validate_url(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{url}", timeout=5, allow_redirects=False) as response:
                    status_code = response.status
                    if status_code == 302:
                        redirect_url = response.headers.get('Location')
                        print(f"{Fore.GREEN}[+]{Fore.RESET}{url} is accessible via HTTP. Redirects to: {redirect_url}")
                        return status_code, redirect_url
                    elif status_code != 200:
                        print(f"{Fore.RED}[-]{Fore.RESET}{url} is not accessible via HTTP. Status code: {status_code}")
                    else:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        title_tag = soup.title
                        if title_tag is not None and title_tag.string is not None:
                            title = title_tag.string
                            length = len(title)
                            print(f"{Fore.GREEN}[+]{Fore.RESET}{url} is accessible via HTTP. Title: {title} ({length} characters)")
                        else:
                            print(f"{Fore.GREEN}[+]{Fore.RESET}{url} is accessible via HTTP. Title not found.")
                    return status_code, url  # Skip HTTPS validation if HTTP is accessible
            except asyncio.TimeoutError:
                print(f"{Fore.YELLOW}[!]{Fore.RESET}{url} HTTP validation timed out. Skipping...")
                return None
            except aiohttp.ClientError:
                pass

            try:
                async with session.get(f"https://{url}", timeout=5, allow_redirects=False) as response:
                    status_code = response.status
                    if status_code == 302:
                        redirect_url = response.headers.get('Location')
                        print(f"{Fore.RED}[-]{Fore.RESET}{url} is accessible via HTTPS. Redirects to: {redirect_url}")
                        return status_code, redirect_url
                    elif status_code != 200:
                        print(f"{Fore.RED}[-]{Fore.RESET}{url} is not accessible via HTTPS. Status code: {status_code}")
                    else:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        title_tag = soup.title
                        if title_tag is not None and title_tag.string is not None:
                            title = title_tag.string
                            length = len(title)
                            print(f"{Fore.RED}[-]{Fore.RESET}{url} is accessible via HTTPS. Title: {title} ({length} characters)")
                        else:
                            print(f"{Fore.RED}[-]{Fore.RESET}{url} is accessible via HTTPS. Title not found.")
                    return status_code, url
            except aiohttp.ClientError:
                pass

    async def validate_urls(self):
        tasks = []
        for url in self.url_list:
            task = asyncio.create_task(self.validate_url(url))
            tasks.append(task)

        try:
            results = await asyncio.gather(*tasks)
        except asyncio.exceptions.TimeoutError:
            print("任务超时")

        return results
