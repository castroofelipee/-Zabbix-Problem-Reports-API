import requests
import json


zabbix_url = ""
zabbix_user = "user"
zabbix_password = "password"


def call_zabbix_api(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": None,
        "id": 1,
    }

    headers = {"Content-Type": "application/json-rpc"}

    response = requests.post(zabbix_url, data=json.dumps(payload), headers=headers, verify=False)
    return response.json()


def authenticate():
    params = {"user": zabbix_user, "password": zabbix_password}
    response = call_zabbix_api("user.login", params)
    return response.get("result")

try:
 
    auth_token = authenticate()

    if auth_token:
        
        host_params = {
            "output": ["hostid", "host"],
            "selectInterfaces": ["ip"],
            "searchByAny": 1,
        }
        
        hosts_response = call_zabbix_api("host.get", host_params)
        hosts = hosts_response.get("result")

        if hosts:
            print("Hosts no Zabbix:")
            for host in hosts:
                print(f"Host ID: {host['hostid']}, Nome: {host['host']}, IP: {host['interfaces'][0]['ip']}")

except Exception as e:
    print(f"Erro: {e}")
