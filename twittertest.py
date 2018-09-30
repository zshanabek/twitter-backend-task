from start import app
import unittest
import json

class TestFlaskTwitter(unittest.TestCase):
    def test_existing_user(self):
        tester = app.test_client(self)
        response = tester.get('/users/zshanabek', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_non_existing_user(self):
        tester = app.test_client(self)
        response = tester.get('/users/zshanabekkk', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_tweets_limit(self):
        limit = 10
        tester = app.test_client(self)
        response = tester.get(f'/hashtags/faceitmajor?limit={limit}', content_type='application/json')
        data = response.get_json()
        tlen = len(data['tweets'])
        self.assertEqual(limit, tlen)        
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()