import requests
import uuid
from colorama import Fore
import threading


def header():
    headers = {
    'User-Agent':'Instagram 125.0.0.18.125 (iPhone11,8; iOS 13_3; en_US; en-US; scale=2.00; 828x1792; 193828684)', 
    'Accept':'*/*', 
    'Accept-Encoding':'gzip, deflate', 
    'Accept-Language':'en-US', 
    'X-IG-Capabilities':'3brTvw==', 
    'X-IG-Connection-Type':'WIFI', 
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
    'Host':'i.instagram.com'}
    return headers




def isGetID(ID): # 고유 아이디 함수
    res = requests.get(f"https://api.instagram.com/web/search/topsearch/?context=blended&query={ID}&rank_token=0.3953592318270893&count=1")
    try:
        user = res.json()["users"] 
        for i in user:
            if i["user"]["username"] == ID: #json 에서 실제 아이디랑 변수 ID 랑 비교
                return i["user"]["pk"] #고유 유저 ID (숫자)
            else: return "아이디가 일치 하지 않습니다." #If Invaild Instagram ID 
    except KeyError as e: #users가 json에 없다고 키 에러가 뜸 
         return f"{Fore.RED}[-] {res.json()['message']}(STATUS : {res.json()['status']}){Fore.RESET}"
    

def isLoginInstagram(acc,pw,tg):
    _uuid = uuid.uuid4() 
    data = {
    '_uuid':_uuid, 
    'username':acc, 
    'enc_password':f"#PWD_INSTAGRAM_BROWSER:0:1589682409:{pw}", 
    'queryParams':'{}', 
    'optIntoOneTap':'false', 
    'device_id':_uuid, 
    'from_reg':'false', 
    '_csrftoken':'missing', 
    'login_attempt_count':'0'}

    re = requests.Session()
    r = re.post("https://i.instagram.com/api/v1/accounts/login/",data=data,headers=header())
    if "logged_in_user" in r.text:
        try:
             session_id = r.cookies.get_dict()['sessionid']
             private_id = isGetID(tg)
             if len(private_id) != 11: return print(f"{Fore.RED}[-] 나중에 다시 시도 해 주세요.\n오류 : {private_id}{Fore.RESET}") #타임아웃 오류 처리
             else:
                print(f"{Fore.BLUE}[+] SESSION ID : {session_id}\n[+] PRIVATE ID : {private_id}{Fore.RESET}")
                cnt = 0
                headers_ = {
                    'User-Agent':'Instagram 125.0.0.18.125 (iPhone12,11; iOS 14_3; en_US; en-US; scale=2.00; 828x1792; 193828684)'}
                req = re.post(f"https://www.instagram.com/api/v1/web/friendships/{private_id}/follow/",headers=headers_,allow_redirects=False)
                if req.status_code == 200 or req.status_code == 302: #302 는 유저에이전트 오류지만 해결 할 수 없음으로 추가 [302가 떠도 팔로우는 정상적으로 들어가는걸 확인함
                    cnt += 1 
                    print(f"{Fore.GREEN}[+] Follow Success! | {tg} | {cnt}{Fore.RESET}")
                else: return print(f"{Fore.RED}[-] Follow Failed.. | {tg}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[-] ERROR : {e}{Fore.RESET}")

    else:
        print(f"{Fore.RED}[-] login Failed..{Fore.RESET}")


def RunStart():
    try:
        import os 
        if os.path.isfile("accounts.txt"):
            target = input(f"{Fore.YELLOW}[+] 팔로우 할 타겟을 입력 해 주세요 > {Fore.RESET}")
            read_ = open("accounts.txt","r")
            s = read_.read().split("\n")     
            acc = s.split(":")[0]
            pw = s.split(":")[1]
            GoFollowers = isLoginInstagram(acc,pw,target) 
        else: return input(f"{Fore.RED}[-] Can't Open File 'accounts.txt'{Fore.RESET}")
    except FileNotFoundError:
        return input(f"{Fore.RED}[-] Can't Open File 'accounts.txt'{Fore.RESET}")
if __name__ == "__main__":
    RunStart()
