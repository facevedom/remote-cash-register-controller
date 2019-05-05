import unittest
from helpers import config_loader


class TestConfigLoader(unittest.TestCase):
    def test_reading_property_from_config_file(self):
        """
        Test that the config loader can properly load configurations from a file
        """
        config = config_loader.load_config("tests/resources/test_config.ini")
        self.assertEqual(config['CASH-REGISTER-1']
                         ['SERVO_INITIAL_POSITION'], '7')

    def test_non_existing_config_file(self):
        """
        Test that the config loader fails if config file doesn't exist
        """
        with self.assertRaises(Exception):
            config_loader.load_config("bogus.ini")
