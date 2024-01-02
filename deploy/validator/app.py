import requests
import os
from flask import Flask, request, Response

xlog_domain = os.environ.get("XLOG_DOMAIN")
app = Flask(__name__)

@app.route("/")
def check_domain():
    domain = request.args.get("domain")
    if not domain:
        return Response(status=404)
    if domain.endswith(f'.{xlog_domain}') or domain == xlog_domain:
        return Response(status=200)

    # get TXT
    res = requests.get("https://cloudflare-dns.com/dns-query", params={
        "name": f"_xlog-challenge.{domain}",
        "type": "TXT",
    }, headers={"Accept": "application/dns-json"})
    if res.status_code != 200:
        return Response(status=res.status_code)
    answer = res.json().get("Answer") or [{}]
    tenant = answer[0].get("data", "").replace('"', "")
    if not tenant:
        return Response(status=404)

    # check crossbell
    res = requests.get(f"https://indexer.crossbell.io/v1/handles/{tenant}/character")
    if res.status_code != 200:
        return Response(status=404)
    attributes = res.json().get("metadata", {}).get("content", {}).get("attributes", [])
    for d in attributes:
        if d.get("trait_type") == "xlog_custom_domain":
            print(d)
            xlog_custom_domain = d.get("value", "").lower()
            if xlog_custom_domain == domain:
                return Response(status=200)

    return Response(status=404)