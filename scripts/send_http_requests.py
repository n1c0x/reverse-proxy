#!/usr/bin/env python
"""
Generates trafic to a given url (default : 127.0.0.1) using a random header
https://pypi.org/project/random-user-agent/
https://pypi.org/project/fake-headers/
"""

# general imports
import requests 
import json
import pprint
import argparse
from time import sleep
import random
import string
from datetime import datetime

# random header imports
from random_user_agent.user_agent import UserAgent
from fake_headers import Headers

def set_url(url):
    """ Return the destination url with a random string at the end, at 30% of time """
    start_range = 1
    end_range = 10
    random_number = random.randint(start_range, end_range)

    string_length = 5
    letters = string.ascii_lowercase
    random_url = "".join(random.choice(letters) for i in range(string_length))

    if random_number > 7:
        url = "http://"+url+"/"+random_url
    else:
        url = "http://"+url
    return url

def set_random_user_agent():
    """ Return random user-agent"""
    limit = 100
    user_agent_rotator = UserAgent(limit=limit)
    random_user_agent = user_agent_rotator.get_random_user_agent()
    return random_user_agent

def set_header():
    """ Set random header user set_random_user_agent() """
    header = Headers(headers = True).generate()
    random_user_agent = {'User-Agent': set_random_user_agent()}
    header.update(random_user_agent)
    return header

def print_results(r, verbose):
    """ Print request and response details """
    if verbose:
        print("Request Header : ")
        pprint.pprint(set_header())
        print("Response Header : ")
        pprint.pprint(dict(r.headers))
        print("Encoding : {}".format(r.encoding))
        print("URL : {}".format(r.url))
        print("Content, in text : {}".format(r.text))
        print("Status code : {}".format(r.status_code))
        print("Status code, in text : {}".format(r.reason))
        print("Error : {}".format(r.raise_for_status))
    else:
        print("Request sent to {}".format(r.url))
        print("Result : {} - {}".format(r.status_code, r.reason))

def print_final_results(r, counter, start_time, end_time):
    """ print final results """
    duration = end_time - start_time
    print("\n{} requests send in {} seconds".format(counter, duration.total_seconds()))

def send_http_request(url, headers):
    """ Send the HTTP request """
    r = requests.get(url = url, headers = headers)
    return r

def set_random_sleep_time():
    start_range = 1
    end_range = 10000
    random_sleep_time = random.randint(start_range, end_range) / 100000
    print("Wait {} before next request".format(random_sleep_time))
    return random_sleep_time

def request_count(count, address, verbose):
    """ Display requests results for limited and unlimited amount of requests """
    if count > 0:
        start_time = datetime.now()
        for _ in range(count):
            r = send_http_request(set_url(address), set_header())
            print_results(r, verbose)
        end_time = datetime.now()
        print_final_results(r, count, start_time, end_time)
    elif count <= 0:
        try:
            counter = 0
            start_time = datetime.now()
            while True:
                r = send_http_request(set_url(address), set_header())
                print_results(r, verbose)
                counter = counter + 1
                sleep(set_random_sleep_time())
        except(KeyboardInterrupt):
            end_time = datetime.now()
            print_final_results(r, counter, start_time, end_time)
    else: 
        print_results(r, verbose)

def main():
    parser = argparse.ArgumentParser(description="Generate HTTP requests to the destination IP address")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-a", "--address", type=str, help = "Destination ip address in format A.B.C.D. Default is 127.0.0.1", default="127.0.0.1")
    group.add_argument("-v", "--verbose", help="Display request and response details", action = "store_true")
    group.add_argument("-q", "--quiet", help="Only display dots", action = "store_true")
    parser.add_argument("-c", "--count", type=int, help = "Amount of requests to send. If 0, send unlimited requests", default="1")
    
    args = parser.parse_args()
    
    request_count(args.count, args.address, args.verbose)
    # TODO : quiet parameter

if __name__ == "__main__":
    main()