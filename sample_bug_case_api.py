import requests
import json

# Constants - replace with your own client_id and client_secret from Cisco API console
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# Cisco API URLs
AUTH_URL_OLD = 'https://cloudsso.cisco.com/as/token.oauth2'
AUTH_URL = 'https://id.cisco.com/oauth2/default/v1/token'
BUG_API_URL = 'https://apix.cisco.com/bug/v3.0/bugs'
CASE_API_URL = 'https://apix.cisco.com/case/v3/cases'


# Get the Access Token
def get_access_token(client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(AUTH_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")

## produces something like this in return..
##{
##  "token_type": "Bearer",
##  "expires_in": 3600,
##  "access_token": "eyJraWQiOiJjbGRsYmY0ejhkTG9wbG9GNGhGeWVQb014b25nTEp3aFVQN3p3Zkk0cFowIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULnFxcW1qTTJvU0tZcHNCWHIxOG13Z1RtLWlWRHk5UFlhdEQ5UjZhRm56bHMiLCJpc3MiOiJodHRwczovL2lkLmNpc2NvLmNvbS9vYXV0aDIvZGVmYXVsdCIsImF1ZCI6ImFwaTovL2RlZmF1bHQiLCJpYXQiOjE3MjU5Nzc2NDEsImV4cCI6MTcyNTk4MTI0MSwiY2lkIjoiY3M1enNmMnMyZmVlOTVlcWR6ZjZncXk1Iiwic2NwIjpbImN1c3RvbXNjb3BlIl0sImFjY2Vzc19sZXZlbCI6MSwic3ViIjoiY3M1enNmMnMyZmVlOTVlcWR6ZjZncXk1IiwiZnVsbF9uYW1lIjoibnVsbCBudWxsIiwiYXpwIjoiY3M1enNmMnMyZmVlOTVlcWR6ZjZncXk1In0.AeQWXrj8dhHMVc9EW_oywKUFmEoE2cjWIlWi_dKSiMkgKpZvoex3s0c88MRhkOAI-ahiDtvowdcHaqZc1ZJErhQX6p7WxYcJqJVFF3-H3JiecR4NMwyONSSbP-aAncYU4HzG_XI0-GT6yL2WyuxbFnlW4fCB1gjzEym5C8Ug5IYdlnsU0O1v-CPdsdfnSXv5_W-9NMtn4tKJHMqMdElInem6RX-UvP6gzKXQKqyV6gjDpCQm59BFMrK5cliQECYMpnykfpMSsIsEW1MXTNrBYb9E_I_ncNOB7M6yMfUuaWNgRrBOfCmRrWfNuOY89pMgNQGL09ppnngFjtCNff1rng",
##  "scope": "customscope"
##}

# Call the Cisco Bug API
# Doc at https://developer.cisco.com/docs/support-apis/bug/#introduction
def get_bug_details(token, bug_ids):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    #old method
    params = {
        'bugid': ','.join(bug_ids)  # Comma-separated list of bug IDs
    }
    params = {}
    #example - https://apix.cisco.com/bug/v3.0/bugs/bug_ids/CSCdr21997,CSCdr72939
    #new method
    bugs_url = f"/bug_ids/{','.join(bug_ids)}"

    response = requests.get(BUG_API_URL + bugs_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get bug details: {response.status_code} {response.text}")


# returns like...
#{
#  "bugs": [
#    {
#      "id": "1",
#      "bug_id": "CSCdr72939",
#      "headline": "Access List setup on snmp community stop traps generation",
#      "description": "The issue occur till the SNMPv3 engine have been included in the train. It so affect 12.0T , 12.1 and 12.1T train.\n\nWhen configuring an access list , applied to snmp-server community, on a running router, the trap generation fully stops on the device. The reload of the machine make it works, with the access-list.\n\nRemoving the acces listed community will stops the trap generation as well.\n\nExpl:\n-----\nPassword: \nPassword: \ncognac>ena\nPassword: \ncognac#\ncognac#\ncognac#sh ver          \nCisco Internetwork Operating System Software \nIOS (tm) C2600 Software (C2600-I-M), Version 12.0(4)T,  RELEASE SOFTWARE (fc1)\nCopyright (c) 1986-1999 by cisco Systems, Inc.\nCompiled Wed 28-Apr-99 16:50 by kpma\nImage text-base: 0x80008088, data-base: 0x806B44EC\n \nROM: System Bootstrap, Version 11.3(2)XA4, RELEASE SOFTWARE (fc1)\n \ncognac uptime is 0 minutes\nSystem restarted by reload\nSystem image file is \"flash:c2600-i-mz.120-4.T\"\n \ncisco 2612 (MPC860) processor (revision 0x101) with 39936K/9216K bytes of memory.\nProcessor board ID JAB040200L7 (469253333)\nM860 processor: part number 0, mask 49\nBridging software.\nX.25 software, Version 3.0.0.\n1 Ethernet/IEEE 802.3 interface(s)\n1 Token Ring/IEEE 802.5 interface(s)\n2 Serial(sync/async) network interface(s)\n32 terminal line(s)\n32K bytes of non-volatile configuration memory.\n16384K bytes of processor board System flash (Read/Write)\n \nConfiguration register is 0x2102\n \ncognac#sh run | include snmp-server\nsnmp-server engineID local 00000009020000B0647AE7E0\nsnmp-server community private RW\nsnmp-server community public RO\nsnmp-server enable traps snmp\nsnmp-server enable traps config\nsnmp-server enable traps entity\nsnmp-server enable traps envmon\nsnmp-server enable traps rtr\nsnmp-server enable traps syslog\nsnmp-server host 172.17.246.208 public \nsnmp-server host 172.17.246.225 public \nsnmp-server host 172.17.246.240 public \ncognac#debug snmp packets\nSNMP packet debugging is on\ncognac#sh debug\nSNMP:\n  SNMP packet debugging is on\ncognac#\ncognac#conf t\nEnter configuration commands, one per line.  End with CNTL/Z.\ncognac(config)#\n00:01:33: SNMP: Queuing packet to 172.17.246.208\n00:01:33: SNMP: V1 Trap, ent ciscoConfigManMIB.2, addr 172.17.246.6, gentrap 6, spectrap 1 \n ccmHistoryEventEntry.3.2 = 1 \n ccmHistoryEventEntry.4.2 = 2 \n ccmHistoryEventEntry.5.2 = 3\n00:01:33: SNMP: Queuing packet to 172.17.246.225\n00:01:33: SNMP: V1 Trap, ent ciscoConfigManMIB.2, addr 172.17.246.6, gentrap 6, spectrap 1 \n ccmHistoryEventEntry.3.2 = 1 \n ccmHistoryEventEntry.4.2 = 2 \n ccmHistoryEventEntry.5.2 = 3\n00:01:33: SNMP: Queuing packet to 172.17.246.240\n00:01:33: SNMP: V1 Trap, ent ciscoConfigManMIB.2, addr 172.17.246.6, gentrap 6, spectrap 1 \n ccmHistoryEventEntry.3.2 = 1 \n ccmHistoryEventEntry.4.2 = 2 \n ccmHistoryEventEntry.5.2 = 3\n00:01:33: SNMP: Packet sent via UDP to 172.17.246.208\n00:01:33: SNMP: Packet sent via UDP to 172.17.246.225\n00:01:34: SNMP: Packet sent via UDP to 172.17.246.240\ncognac(config)#end\n\n-------> Config mib trap generated\n\ncognac#\ncognac#\ncognac#conf t\nEnter configuration commands, one per line.  End with CNTL/Z.\ncognac(config)#snmp-server community public ro 1\ncognac(config)#end\ncognac#\n00:04:16: %SYS-5-CONFIG_I: Configured from console by console\ncognac#conf t\nEnter configuration commands, one per line.  End with CNTL/Z.\ncognac(config)#end\n\n------> No config mib trap generated\n\ncognac#conf t\nEnter configuration commands, one per line.  End with CNTL/Z.\ncognac(config-if)#shu\n00:04:51: %LINK-5-CHANGED: Interface Serial0/0, changed state to administratively down\n00:04:52: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial0/0, changed state to down\ncognac(config-if)#no shut\ncognac(config-if)#\n00:04:57: %LINK-3-UPDOWN: Interface Serial0/0, changed state to up\n00:04:58: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial0/0, changed state to up\ncognac(config-if)#\ncognac(config-if)#end\ncognac#n\n\n\n-----> no linkup trap.\n\n\nthe access list is properly defined:\naccess-list 1 permit any\n",
#      "severity": "2",
#      "status": "OT",
#      "behavior_changed": "",
#      "duplicate_of": "CSCdr21997",
#      "created_date": "",
#      "last_modified_date": "2002-02-18",
#      "products": [
#        {
#          "product_name": "Cisco 2600 Series Multiservice Platforms"
#        }
#      ],
#      "known_affected_releases": "12.0(4)T",
#      "known_fixed_releases": "",
#      "support_case_count": "0"
#    }
#  ]
#}


# Call the Cisco Case API to get case details
# doc at https://developer.cisco.com/docs/support-apis/case/#introduction
def get_case_summary(token, case_ids):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    #old method
    params = {
        'case_ids': ','.join(case_ids)  # Comma-separated list of case IDs
    }
    params = {}
    #example: https://apix.cisco.com/case/v3/cases/case_ids/682299374,682299374
    
    #new method
    cases_url = f"/case_ids/{','.join(case_ids)}"
    
    response = requests.get(CASE_API_URL + cases_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get case details: {response.status_code} {response.text}")

#returns like this...
#{
#  "cases": [
#    {
#      "item_entry_id": 1,
 #     "user_id": "directcust4",
 #     "case_id": "682299374",
 #     "title": "SNTC : Day 2 : NOS Handover Collector Training :TARGET CORPORATION",
 #     "severity": "3",
 #     "contact_name": "CPRSMOKE TESTER",
 #     "status_flag": "C",
 #     "status": "Closed",
 #     "creation_date": "2017-05-09T20:08:45.000Z",
 #     "updated_date": "2017-05-11T18:44:01.000Z",
 #     "serial_number": "",
 #     "contract_id": "",
 #     "technology_name": "Smart Services Capabilities",
 ##     "sub_technology_name": "Collector Deployment SNTC (Contract Required)",
 #     "rmas": [],
 #     "bugs": []
 #   }
 # ],
 # "count": 1
#}

# Main function
if __name__ == "__main__":
    try:
        # Get access token
        token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        print(f"Access Token: {token}")
        
        # Get bug details (example bug IDs)
        bug_ids = ['CSCdr21997', 'CSCdr72939']
        bug_details = get_bug_details(token, bug_ids)
        
        # Print the results
        print(json.dumps(bug_details, indent=4))

        # Get case details (example case IDs)
        case_ids = ['682299374', '682299374']  # Replace with actual case IDs
        case_summary = get_case_summary(token, case_ids)
        
        # Print the results
        print(json.dumps(case_summary, indent=4))
    
    except Exception as e:
        print(f"Error: {e}")
