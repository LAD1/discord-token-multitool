from colorama import Fore, init
import httpx
import toml
import os

def get_dcf_sdc(cookie):
    sep = cookie.split(";")
    sx = sep[0]
    sx2 = sx.split("=")
    dcf = sx2[1]

    split = sep[6]
    split2 = split.split(",")
    split3 = split2[1]
    split4 = split3.split("=")
    sdc = split4[1]

    return dcf, sdc

def http_headers(token):
    cookie = httpx.get("https://discord.com/register").headers['set-cookie']
    dcf, sdc = get_dcf_sdc(cookie)
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.263 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
        "Referer": "https://discord.com/register",
        "Authorization": token,
        "X-Super-Properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMC4xNDsgcnY6ODguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC84OC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiODguMCIsIm9zX3ZlcnNpb24iOiIxMC4xNCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5MTczNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
        "X-Fingerprint": '873691818078920745.AdL-Gi4qePqVs4lEO8acceJAgxc',
        "Cookie": f"__dcfduid={dcf}; __sdcfduid={sdc}; OptanonConsent=isIABGlobal=false&datestamp=Mon+Aug+09+2021+04%3A31%3A04+GMT%2B0300+(Arabian+Standard+Time)&version=6.17.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2Floggin&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _gcl_au=1.1.62729347.1628472664; _ga=GA1.2.1942394829.1628472665; _gid=GA1.2.2001024037.1628472665",
        "DNT": "1",
        "Connection": "keep-alive"
    }

def getGuilds(tokens, amount):
    tokens_scraped = 0
    with open(f'tokens.txt', 'a') as f:
        for token in tokens:
            headers = http_headers(token)
            while True:
                try:
                    e = httpx.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
                    break
                except:
                    pass
            if e.status_code == 200:
                json_response = e.json()
                if len(e.json()) >= amount:
                    print(f"{token} has {len(e.json())} guilds")
                    with open(f'more_than_amount.txt', 'a') as f:
                            try:
                                f.write(token + "\n")
                            except:
                                pass
                else:
                    print(Fore.GREEN + f"{token} has {len(e.json())} guilds")
                    with open(f'less_than_amount.txt', 'a') as f:
                        try:
                            f.write(token + "\n")
                        except:
                            pass
            else:
                print(Fore.RED + f"{token} is invalid!")
                with open(f'invalid.txt', 'a') as f:
                    f.write(token + "\n")       


        print(f"Finished")


def guildcount(tokens):
    tokens_scraped = 0
    for token in tokens:
        headers = http_headers(token)
        while True:
            try:
                e = httpx.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
                break
            except:
                pass
        if e.status_code == 200:
            json_response = e.json()
            print(Fore.GREEN + f"{token} has {len(e.json())} guilds")
            with open(f'guildcount.txt', 'a') as f:
                try:
                    f.write(f"{token} | {len(e.json())} Guilds\n")
                except:
                    pass

        else:
            print(Fore.RED + f"{token} is invalid! Skipping.")
            with open(f'invalid.txt', 'a') as f:
                f.write(token + "\n")       
    print(f"Finished")


def checker(tokens):
    for token in tokens:
        headers = http_headers(token)
        r = httpx.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
        if r.status_code == 200:
            print(Fore.GREEN + f"{token} valid")
            with open(f'valid.txt', 'a') as f:
                f.write(token + "\n")       
        else:
            print(Fore.RED + f"{token} invalid")
            
            with open(f'invalid.txt', 'a') as f:
                f.write(token + "\n")       

def verified(tokens):
    for token in tokens:
        headers = http_headers(token)
        r = httpx.get("https://discord.com/api/v9/users/@me" , headers=headers)
        if r.status_code == 401:
            print(Fore.RED + f"{token} invalid")
            with open(f'invalid.txt', 'a') as f:
                f.write(token + "\n")
        elif r.status_code == 200:
            data = r.json()
            phone = data['phone']
            verified = data['verified']
            if phone == None:
                print(Fore.YELLOW + f"{token} no phone number")
                with open(f'not_fully_verified.txt', 'a') as f:
                    f.write(token + "\n")
            if verified == False:
                print(Fore.YELLOW + f"{token} needs to be verified")
                with open(f'need_verification.txt', 'a') as f:
                    f.write(token + "\n")
            if phone and verified:
                print(Fore.GREEN + f"{token} fully verified")
                with open(f'fully_verified.txt', 'a') as f:
                    f.write(token + "\n")

try:
    tokens = []
    with open('tokens.txt', 'r') as f:
        for i in f:
            tokens.append(i.split(' | ')[0].strip())
    tokens = list(set(tokens))
except:
    print("No tokens.txt file found! Please create the file and try again.", Fore.RED)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.BLUE+"DISCORD TOKEN TOOL!\n",Fore.GREEN)
    print(Fore.GREEN+"1. Split token by guild count\n2. Save all tokens with guild count\n3. Token checker\n4. check if token is fully verified",Fore.BLUE)
    r = input("x] ")
    if r == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.GREEN+"Select number of servers to split the tokens by",Fore.BLUE)
        amount = int(input("[x] "))
        getGuilds(tokens, amount)
    elif r == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        guildcount(tokens)
    elif r == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        checker(tokens)
    elif r == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        verified(tokens)
    else:
        main()

if __name__ == '__main__':
    main()
