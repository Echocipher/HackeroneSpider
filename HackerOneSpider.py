import requests
import json
import time
from alive_progress import alive_bar

item_list = []
localtime = time.localtime(time.time())
time = time.strftime('%Y%m%d%s',time.localtime(time.time()))
time_name = str(time)

def hackerone_spider():
    targets = {
        'domains': [],
        'wildstar': [],
        'bounty_domains': [],
        'code': [],

    }
    print("[*] Fetching all item quantities")
    spider_url = "https://hackerone.com/programs/search?query=type:hackerone&sort=published_at:descending&page=1"
    try:
        first_request = requests.get(url=spider_url, headers={'Accept': 'application/json'})
    except:
        print("[x] Unable to access hackerone, please check the agent or network")
    total_num = json.loads(first_request.text)["total"]
    print("[+] All item quantity fetched successfully. The item quantity is {}".format(str(total_num)))
    pages_num = int(total_num/100) + 1
    for page in range(1, pages_num + 1):
        print("[*] Crawling the page {} of data".format(str(page)))
        url = "https://hackerone.com/programs/search?query=type:hackerone&sort=published_at:descending&page={}".format(page)
        try:
            item_request = requests.get(url=url, headers={'Accept': 'application/json'})
            item_results = json.loads(item_request.text)["results"]
            for item in item_results:
                submission_state = item["meta"]["submission_state"]
                if submission_state == "open":
                    item_list.append(item["url"])
                else:
                    break            
        except:
            print("[x] Craw page {} Error!")

    print("[+] The matching of items submission state open is completed, and the quantity is {}".format(len(item_list)))
    print("[+] Crawling node URL")
    with alive_bar(len(range(len(item_list)))) as bar:
        for item_url in item_list:
            bar()
            item_url = item_url.strip("/")
            try:
	            site_url = "https://hackerone.com:443/graphql"
	            site_headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"", "Accept": "*/*", "Content-Type": "application/json", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://hackerone.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
	            site_json={"operationName": "test", "query": "query LayoutDispatcher($url: URI!) {\n  resource(url: $url) {... on Team {\n     ...TeamProfileHeaderTeam\n      __typename\n    }\n    ... on User {\n      id\n      username\n      __typename\n    }\n    __typename\n  }\n  me {\n    id\n    ...TeamProfileHeaderUser\n    __typename\n  }\n}\n\nfragment TeamProfileHeaderTeam on Team {\n                  structured_scopes {\n    edges {\n      node {\n        max_severity\n   eligible_for_bounty\n     asset_identifier\n        asset_type\n      }\n      __typename\n    }\n    __typename\n  }\n  child_teams {\n    total_count\n    edges {\n      node {\n        id\n        name\n        handle\n        offers_bounties\n               structured_scopes {\n          edges {\n            node {\n              id\n              asset_identifier\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  posts {\n    total_count\n    __typename\n  }\n  external_program {\n    id\n    __typename\n  }\n  assets_in_scope: structured_scopes(\n    archived: false\n    eligible_for_submission: true\n  ) {\n    total_count\n    __typename\n  }\n  ...TeamTableAverageBounty\n        ...TeamNoticeBanner\n    __typename\n}\n\nfragment TeamTableAverageBounty on Team {\n    __typename\n}\n\nfragment TeamNoticeBanner on Team {\n  id\n  handle\n  state\n  offers_bounties\n      __typename\n}\n\n\n\nfragment TeamProfileHeaderUser on User {\n  id\n  has_active_ban\n  ...TeamCTAMe\n  ...BanNoticeModal\n  __typename\n}\n\nfragment TeamCTAMe on User {\n  id\n  has_active_ban\n  __typename\n}\n\nfragment BanNoticeModal on User {\n  id\n  active_ban {\n    id\n    starts_at\n    ends_at\n    duration_in_days\n    __typename\n  }\n  __typename\n}\n", "variables": {"url": item_url}}
	            result = requests.post(site_url, headers=site_headers, json=site_json)
	            for e in json.loads(result.text)["data"]["resource"]["structured_scopes"]["edges"]:
	                if e['node']['asset_type'] == 'URL' and e['node']['max_severity']  != 'none':
	                    domain = e['node']['asset_identifier']
	                    if domain[0] == '*':
	                        targets['wildstar'].append(domain[2:])
	                    if e['node']['eligible_for_bounty']:
	                        targets['bounty_domains'].append(domain)
	                    targets['domains'].append(domain)
	                elif e['node']['asset_type'] == 'SOURCE_CODE' and e['node']['max_severity']  != 'none':
	                    domain = e['node']['asset_identifier']
	                    targets['code'].append(domain)
            except:
                break
    return targets


if __name__ == '__main__':
    banner = """
                               _            
 /_/_  _  /__  __  _  _   /_`_  . _/_  _
/ //_|/_ /\/_'//_// //_' ._//_///_//_'/ 
                           /              
       {}
    """.format("V 0.1 Author: Echocipher")
    print(banner)
    targets = hackerone_spider()
    with open(time_name + '_domains.txt', 'w') as f:
        f.write('\n'.join(targets['domains']))
    print("[+] Save domains as {}".format(time_name + '_domains.txt'))
    with open(time_name + '_wildstar.txt', 'w') as f:
        f.write('\n'.join(targets['wildstar']))
    print("[+] Save wildstar as {}".format(time_name + '_wildstar.txt'))
    with open(time_name + '_with_bounties.txt', 'w') as f:
        f.write('\n'.join(targets['bounty_domains']))
    print("[+] Save with_bounties as {}".format(time_name + '_with_bounties.txt'))
    with open(time_name + '_code.txt', 'w') as f:
        f.write('\n'.join(targets['code']))
    print("[+] Save code as {}".format(time_name + '_code.txt'))


