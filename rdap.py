#!/usr/bin/python3
# 4/21/2025  Tom Willett
# Simple code to query rdap (the replacement for whois) - in my testing rdap was not as reliable as whois and often ran into rate limits
# Not all registrars return the same information.
# The reliable things that were returned were:  'type', 'status', 'startAddress', 'rdapConformance', 'port43', 'objectClassName', 
# 'notices', 'name', 'links', 'ipVersion', 'handle', 'entities' and 'endAddress'.  
# Usually 'events', 'country' and  'cidr0_cidrs' are available and seldom 'remarks' and 'redacted' are available.

import sys
import requests
import pprint
import argparse
import re

parser = argparse.ArgumentParser(description="Lookup IPs and Domains and other objects with RDAP - the replacement for Whois")
parser.add_argument('arg', help="Domain or IP to lookup")
parser.add_argument('-t','--type', help='Type to look up other than IP or Domain, e.g. autnum or entity')
parser.add_argument('-p','--property', help='Comma delimited list of properties to return - if "keys" is used a list of available properties will be returned')
parser.add_argument('-j','--json', help='Return the json response instead of pretty print', action="store_true")
args=parser.parse_args()

# The requests were not reliable without a user-agent string (my server will reject any such request).
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
# Regex to detect a valid IP
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
# Url to perform the lookup at
baseurl='https://rdap.org/'

# check what type to lookup
if (args.type):
    url=baseurl + args.type + '/' + args.arg
elif (re.search(regex,args.arg)):
    # Assume IP  if valid regex
    url = baseurl + 'ip/' + args.arg
else:
    # Assume domain
    url=baseurl + 'domain/' + args.arg

# Download the info and convert to a dictionary
try:
    r=requests.get(url, headers=headers)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
except requests.exceptions.Timeout:
    raise SystemExit("Timeout Error")
except requests.exceptions.TooManyRedirects:
    raise SystemExit("Too Many Redirects")
except requests.exceptions.RequestException as e:
    raise SystemExit(e)
else:
    results=r.json()

# check if only specific properties will be returned
if (args.property):
    if (args.property=='keys'):
        output=results.keys()
    else:
        output={}
        for x in args.property.split(','):
            try:
                output[x]=results[x]
            except Exception as e:
                output[x]=''
else:
    output=results

# check to see if json output is desired
if (args.json):
    print(output)
else:
    pprint.pprint(output)
