import unittest
from unittest.mock import Mock, MagicMock, patch

from fastapi.testclient import TestClient

import main
from main import app


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    @patch("main.bigquery.Client.query")
    def test_query_success(self, mock_bq):
        exp_result = [{"body": "Mock answer."}]
        mock_bq.return_value.result.return_value = exp_result
        # This is an online test as the method is simple
        query = "how to install pip?"
        res = main.query(query)
        
        self.assertEqual(res, exp_result)
    
    @patch("main.generate_response")
    @patch("main.query")
    def test_post_ask(self, mock_q, mock_gr):
        expected_response = {"answer": "Mock response"}
        mock_gr.return_value.content = expected_response["answer"]
        response = self.client.post("/ask",
                                    json={"question": "How to install numpy?"})
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
