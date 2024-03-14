from django.test import TestCase
from login.models import OsmUser
from model_bakery import baker


class OsmUserModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user = baker.make(OsmUser, username="test_user", password="test_password", osm_id=12345)

    def test_create_user(self):
        # Test case for creating a user, checking the username, password, and osm_id.
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.password, "test_password")
        self.assertEqual(self.user.osm_id, 12345)

    def test_create_duplicate_user_fails(self):
        # Creating the exact same user should fail because of duplication.
        with self.assertRaises(Exception):
            baker.make(OsmUser, username="test_user", password="test_password", osm_id=12345)

    def test_create_invalid_user_fails(self):
        # Creating a user without a username should fail.
        with self.assertRaises(Exception):
            baker.make(OsmUser, password="test_password", osm_id=12345)           

    def test_missing_osm_id_fails(self):
        # Creating a user without osm_id should fail.
        with self.assertRaises(Exception):
            baker.make(OsmUser, username="test_user", password="test_password")

    def test_string_representation(self):
        # Test the string representation of an OsmUser instance
        self.assertEqual(str(self.user), self.user.username)

    def test_string_representation_with_different_username(self):
        # Test the string representation of an OsmUser instance with a different username
        self.user.username = "different_user"
        self.assertEqual(str(self.user), self.user.username)

    def test_string_representation_with_different_osm_id(self):
        # Test the string representation of an OsmUser instance with a different osm_id
        self.user.osm_id = 54321
        self.assertEqual(str(self.user), self.user.username)

    def test_string_representation_with_different_password(self):
        # Test the string representation of an OsmUser instance with a different password
        self.user.password = "different_password"
        self.assertEqual(str(self.user), self.user.username)