import unittest

from fastapi.testclient import TestClient

import main
from main import app


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_query(self):
        # This is an online test as the method is simple
        query = "how to install pip"
        exp_result = [{
            "body": "\u003cp\u003eI recommend you to uninstall python and the\
                    n reinstall it again. In the installation window, use cus\
                    tom installation and check all the option which includes \
                    pip and also check to add pip to your environment variabl\
                    es.\u003c/p\u003e"
        }, {
            "body": "\u003cp\u003eYou can use the wheel directly like this:\
                    \u003c/p\u003e\n\n\u003cpre\u003e\u003ccode\u003epython3\
                    ./pip-19.2.2-py2.py3-none-any.whl/pip install ./pip-19.2\
                    .2-py2.py3-none-any.whl\n\u003c/code\u003e\u003c/pre\u003e"
        }]
        res = main.query(query)
        self.assertEqual(res, exp_result)

    def test_post_ask(self):
        response = self.client.post("/ask",
                                    json={"question": "How to install numpy?"})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
