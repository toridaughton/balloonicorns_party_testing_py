"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        # Checking to see if the byte literal contains "having a party" in the 
        # data based on the result we get. It should inculde the b literal info:
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/")
       
        self.assertIn(b"Please RSVP", result.data)

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)
        self.assertIn(b"Yay!", result.data)
        self.assertNotIn(b"Please rsvp", result.data)
        self.assertIn(b"Party Details", result.data)


    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': "Mel", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info, follow_redirects=True)

        self.assertNotIn(b"Yay!", result.data)
        self.assertNotIn(b"Party Details", result.data)
        self.assertIn(b"Please RSVP", result.data)

if __name__ == "__main__":
    unittest.main()
