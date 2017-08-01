
import requests
import unittest
import json
import random
from validate_email import validate_email


class RestApiException(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "RestApiException: status={}".format(self.status)


class RestApiTest(unittest.TestCase):
    def setUp(self):
        self.url = 'https://jsonplaceholder.typicode.com/'

    def get(self, path):
        resp = requests.get(self.url + path)
        if resp.status_code != 200:
            raise RestApiException("GET " + path + " err:" + str(resp.status_code))
        return resp.json()

    def post(self, path, data):
        resp = requests.post(self.url + path, data)
        if resp.status_code != 201:
            raise RestApiException("POST " + path + " err:" + str(resp.status_code))
        return resp.json()

    def validatePosts(self, posts):
        for post in posts:
            self.assertIsInstance(post["id"], int)
            self.assertGreater(post["id"], 0)
            self.assertIsInstance(post["title"], basestring)
            self.assertTrue(post["title"])
            self.assertIsInstance(post["body"], basestring)
            self.assertTrue(post["body"])

    @staticmethod
    def printAddress(address):
        print json.dumps({"address" : address}, indent=4)

    def validateEmailFormat(self, email):
        self.assertTrue(validate_email(email))

    @staticmethod
    def constructPost(user_id):
        return {"userId": user_id,
                "title": "This title was made by some test",
                "body": "This body is an Lorem ipsum: Sed ut perspiciatis, "
                        "unde omnis iste natus error sit voluptatem accusantium "
                        "doloremque laudantium, totam rem aperiam eaque ipsa, quae ab "
                        "illo inventore veritatis "}

    def test(self):
        users = self.get("users")
        random_user = random.choice(users)
        self.validateEmailFormat(random_user["email"])
        self.printAddress(random_user["address"])
        user_id = random_user["id"]
        posts = self.get("posts?userId=" + str(user_id))
        self.validatePosts(posts)
        self.post("posts", self.constructPost(user_id))


if __name__ == '__main__':
    unittest.main()
