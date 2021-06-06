import requests
import json
import creds
import logging
from secretsManager import get_secret
from dynamoDB import index_tweet


logger = logging.getLogger("twitter stream")
logger.setLevel(logging.INFO)

endpoint = "https://api.twitter.com/2/tweets/sample/stream"
auth = get_secret()
# token = creds.api_details['bearerToken']
# print(auth)
# logger.info(f"auth {auth}")
token = auth['bearerToken']
headers = {"Authorization": "Bearer {}".format(token)}


def connect_to_endpoint(url):
    response = requests.request("GET", url, headers=headers, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response["data"]
            index_tweet(tweet)
            # print(tweet)
            # logger.log(json.dumps(json_response, indent=4, sort_keys=True))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    # timeout = 0
    # while timeout < 5:
    #     connect_to_endpoint(endpoint)
    #     timeout += 1
    connect_to_endpoint(endpoint)


if __name__ == "__main__":
    main()