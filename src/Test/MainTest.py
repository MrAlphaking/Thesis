import unittest
from DataCleanerTest import *
from DataCreatorTest import *

def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [DataCleanerTest, DataCreatorTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

    # ...


if __name__ == '__main__':
    run_some_tests()