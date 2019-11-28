from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import time
import requests
import schedule
from beem import Steem
from beem.nodelist import NodeList
from steemengine.api import Api

beem_pass = ""
api = Api()
stm = Steem()
stm.wallet.unlock(pwd=beem_pass)

def claim_tokens():
    username = ["ufm.reserve", "taskmanager", "tmholdings", "upfundme", "tmps"]
    for username in username:
        url = "http://scot-api.steem-engine.com/@" + username
        r = requests.get(url)
        result = r.json()

        json_data = []
        for token in result:
            scot = result[token]
            if int(scot["pending_token"]) > 0:
                json_data.append({"symbol": token})
                print(username + " can claim %s" % (token))

        if len(json_data) > 0:
            nodes = NodeList()
            nodes.update_nodes()
            stm = Steem(nodes.get_nodes())
            try:
                stm.unlock(pwd=beem_pass)
            except:
                stm = Steem(node=nodes.get_nodes(), keys=[pwd])
            stm.custom_json("scot_claim_token", json_data, required_posting_auths=[username])
        else:
            print(username + " Has nothing to claim")

claim_tokens()
schedule.every(5).minutes.do(claim_tokens)


while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
