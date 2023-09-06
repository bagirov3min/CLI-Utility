import unittest
from tests import test_other_moduls, test_crud_and_menu

test_suite = unittest.TestLoader().loadTestsFromTestCase(test_other_moduls.TestModuls)
test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_crud_and_menu.TestTextCreated))
test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_crud_and_menu.TestUserCreated))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite)