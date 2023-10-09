import requests
import yaml
import json
from prettytable import PrettyTable

class QuakeAPI:
    def __init__(self):
        self.config = self.read_yaml()

    def read_yaml(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def user_info(self):
        url = 'https://quake.360.net/api/v3/user/info'
        quake_key = self.config['Quake']['KEY']
        headers = {
            "X-QuakeToken": quake_key
        }
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            print('请求失败，请检查配置文件及网络')
            return False
        else:
            if response.status_code == 200:
                json_data = json.loads(response.text)
                if json_data['message'] == 'Successful.' and json_data['code'] == 0:
                    return True
                else:
                    print(json_data['message'])
                    return False
            else:
                print('请求失败，请检查网络')
                return False

    def quake_search(self, query, start, size):
        if self.user_info():
            url = 'https://quake.360.net/api/v3/search/quake_service'
            quake_key = self.config['Quake']['KEY']
            headers = {
                "X-QuakeToken": quake_key,
                "Content-Type": "application/json"
            }
            data = {
                "query": query,
                "start": start,
                "size": size,
                "ignore_cache": False,
                "include": ["ip", "port", "service.http.host", "service.http.title", "location.country_cn",
                            "location.province_cn", "location.city_cn"]
            }
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
            except Exception as e:
                print(e)
                print('请求失败，请检查配置文件及网络')
                return False
            else:
                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    table = PrettyTable(['序号', 'IP', 'PORT', 'TITLE', 'HOST', 'COUNTRY', 'PROVINCE', 'CITY', 'URL'])
                    for index, i in enumerate(json_data['data'], start=1):
                        url = f"{i['ip']}:{i['port']}"
                        table.add_row([index, i['ip'], i['port'], i['service']['http']['title'],
                                       i['service']['http']['host'], i['location']['country_cn'],
                                       i['location']['province_cn'], i['location']['city_cn'], url])
                    print(table)
                    print("共搜索到：" + str(json_data['meta']['pagination']['total']) + " 条结果")
                    print("当前页：" + str(json_data['meta']['pagination']['page_index']) + " 页，共" +
                          str(len(json_data['data'])) + "条数据")
                    return json_data
