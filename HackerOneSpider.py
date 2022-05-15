import requests
import json
import time
from alive_progress import alive_bar

item_list = []
url_list = []
localtime = time.localtime(time.time())
time = time.strftime('%Y%m%d%s',time.localtime(time.time()))
file_name = str(time) + ".txt"

def hackerone_spider():
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

	print("[+] The matching of items providing bounty is completed, and the quantity is {}".format(len(item_list)))
	print("[+] Crawling node URL")
	with alive_bar(len(range(len(item_list)))) as bar:
		for item_url in item_list:
			bar()
			item_url = item_url.strip("/")
			try:
				site_url = "https://hackerone.com:443/graphql"
				site_headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"", "Accept": "*/*", "Content-Type": "application/json", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://hackerone.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
				site_json={"operationName": "", "query": "query LayoutDispatcher($url: URI!) {\n  resource(url: $url) {\n    ... on ResourceInterface {\n      url\n      __typename\n    }\n    ... on Team {\n      id\n      type\n      handle\n      ...TeamProfileHeaderTeam\n      __typename\n    }\n    ... on User {\n      id\n      username\n      __typename\n    }\n    __typename\n  }\n  me {\n    id\n    ...TeamProfileHeaderUser\n    __typename\n  }\n}\n\nfragment TeamProfileHeaderTeam on Team {\n  id\n  name\n  about\n  website\n  handle\n  only_cleared_hackers\n  is_team_member\n  launched_at\n  offers_bounties\n  state\n  offers_thanks\n  url\n  triage_active\n  critical_submissions_enabled\n  controlled_launch_setting {\n    id\n    controlled_launch_team\n    __typename\n  }\n  allows_private_disclosure\n  allows_bounty_splitting\n  publicly_visible_retesting\n  policy_setting {\n    id\n    i_can_subscribe_to_policy_changes\n    __typename\n  }\n  submission_state\n  i_can_view_program_info\n  i_can_view_hacktivity\n  i_can_view_pentests\n  i_can_view_checklist_checks\n  child_program_directory_enabled\n  resolved_report_count\n  profile_picture(size: large)\n  cover_color\n  cover_photo_url\n  has_cover_photo\n  has_cover_video\n  twitter_handle\n  checklist {\n    id\n    checklist_checks {\n      total_count\n      __typename\n    }\n    __typename\n  }\n  structured_scopes {\n    edges {\n      node {\n        id\n        asset_identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  child_teams {\n    total_count\n    edges {\n      node {\n        id\n        name\n        handle\n        offers_bounties\n        profile_picture(size: medium)\n        structured_scopes {\n          edges {\n            node {\n              id\n              asset_identifier\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  posts {\n    total_count\n    __typename\n  }\n  external_program {\n    id\n    __typename\n  }\n  assets_in_scope: structured_scopes(\n    archived: false\n    eligible_for_submission: true\n  ) {\n    total_count\n    __typename\n  }\n  ...TeamTableAverageBounty\n  ...TeamTableResolvedReports\n  ...TeamCTATeam\n  ...TeamContentBanner\n  ...TeamNoticeBanner\n  ...BookmarkTeam\n  __typename\n}\n\nfragment TeamTableAverageBounty on Team {\n  id\n  currency\n  average_bounty_lower_amount\n  average_bounty_upper_amount\n  __typename\n}\n\nfragment TeamTableResolvedReports on Team {\n  id\n  resolved_report_count\n  __typename\n}\n\nfragment TeamCTATeam on Team {\n  id\n  abuse\n  allows_private_disclosure\n  allows_disclosure_assistance\n  allows_bounty_splitting\n  publicly_visible_retesting\n  handle\n  external_url\n  submission_state\n  policy_setting {\n    id\n    __typename\n  }\n  i_reached_abuse_limit\n  i_can_view_private\n  i_can_view_private_program_application_requirement\n  i_can_see_report_submit_button\n  i_can_view_hacktivity\n  i_can_edit_program_profile\n  facebook_team\n  settings_link\n  external_program {\n    id\n    disclosure_email\n    disclosure_url\n    __typename\n  }\n  __typename\n}\n\nfragment TeamContentBanner on Team {\n  id\n  name\n  handle\n  critical_submissions_enabled\n  submission_state\n  __typename\n}\n\nfragment TeamNoticeBanner on Team {\n  id\n  handle\n  state\n  offers_bounties\n  ...DemoTeamNoticeBanner\n  ...SoftLaunchedTeamNoticeBanner\n  __typename\n}\n\nfragment DemoTeamNoticeBanner on Team {\n  id\n  allowed_to_use_saml_in_sandbox\n  handle\n  has_avatar\n  has_payment_method\n  policy_setting {\n    id\n    has_policy\n    __typename\n  }\n  controlled_launch_setting {\n    id\n    controlled_launch_team\n    __typename\n  }\n  launch_link\n  offers_bounties\n  review_requested_at\n  review_rejected_at\n  state\n  team_member_groups {\n    id\n    permissions\n    __typename\n  }\n  __typename\n}\n\nfragment SoftLaunchedTeamNoticeBanner on Team {\n  id\n  name\n  i_can_view_invite_hackers\n  launch_link\n  i_am_a_whitelisted_reporter\n  __typename\n}\n\nfragment BookmarkTeam on Team {\n  id\n  bookmarked\n  __typename\n}\n\nfragment TeamProfileHeaderUser on User {\n  id\n  has_active_ban\n  ...TeamCTAMe\n  ...BanNoticeModal\n  __typename\n}\n\nfragment TeamCTAMe on User {\n  id\n  has_active_ban\n  __typename\n}\n\nfragment BanNoticeModal on User {\n  id\n  active_ban {\n    id\n    starts_at\n    ends_at\n    duration_in_days\n    __typename\n  }\n  __typename\n}\n", "variables": {"url": item_url}}
				result = requests.post(site_url, headers=site_headers, json=site_json)
				for node in json.loads(result.text)["data"]["resource"]["structured_scopes"]["edges"]:
					node_url = node["node"]["asset_identifier"]
					url_list.append(node_url)
			except:
				break
	with open(file_name, "w") as w:
		for url in url_list:
			w.write(url+"\n")
	print("[+] The web address is saved successfully. The number of web addresses is {}".format(len(url_list)))
	print("[+] Save results as {}".format(file_name))


if __name__ == '__main__':
	banner = """
	                           _            
 /_/_  _  /__  __  _  _   /_`_  . _/_  _
/ //_|/_ /\/_'//_// //_' ._//_///_//_'/ 
                           /              
       {}
	""".format("V 0.1 Author: Echocipher")
	print(banner)
	hackerone_spider()

