import json
import subprocess
import time
import unittest
import urllib.request


class PaymentServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = subprocess.Popen(
            ["python3", "app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait()

    def test_health_endpoint(self):
        with urllib.request.urlopen("http://localhost:8000/health") as response:
            data = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(data["status"], "ok")

    def test_payment_endpoint(self):
        with urllib.request.urlopen("http://localhost:8000/payment") as response:
            data = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertIn(data["status"], ["approved", "declined", "failed"])
            self.assertIn("payment_id", data)


if __name__ == "__main__":
    unittest.main()