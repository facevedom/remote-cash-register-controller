import unittest
import xmlrunner
from tests.test_config_loader import TestConfigLoader

if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
