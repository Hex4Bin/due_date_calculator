import unittest
import datetime as dt
from app import CalculateDueDate


class TestApp(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase.
    """

    def setUp(self):
        """
        Initial parameters
        """
        self.duedate = CalculateDueDate(dt.datetime.now(), 4)
        self.test_time = dt.datetime(2021, 6, 18, 11, 0, 0)
        self.test_turn_time = 4

    def test_create(self):
        """
        Testing the instanciation
        """
        self.assertIsInstance(self.duedate, CalculateDueDate)

    def test_check_args_submit_time(self):
        """
        Testing the return value of the check_args method (submit_time).
        """
        test_time = "2021/06/18 11:00:00"
        with self.assertRaises(TypeError) as context:
            self.duedate.check_args(test_time, self.test_turn_time)
        self.assertTrue("Invalid input format. 'submit_time' must be <datetime> format." in str(
            context.exception))

    def test_check_args_turn_time(self):
        """
        Testing the return value of the check_args method (turn_time).
        """
        test_turn_time = "xxx"
        with self.assertRaises(TypeError) as context:
            self.duedate.check_args(self.test_time, test_turn_time)
        self.assertTrue("Invalid input format. 'turn_time' must be <int> format." in str(
            context.exception))

    def test_check_args_weekend(self):
        """
        Testing the return value of the check_args method (weekend).
        """
        test_date = dt.datetime(2021, 6, 20, 11, 0, 0)
        with self.assertRaises(ValueError) as context:
            self.duedate.check_args(test_date, self.test_turn_time)
        self.assertTrue(
            "You can submit requests during weekdays only." in str(context.exception))

    def test_check_args_working_hours(self):
        """
        Testing the return value of the check_args method (working hours).
        """
        test_date = dt.datetime(2021, 6, 18, 7, 0, 0)
        with self.assertRaises(ValueError) as context:
            self.duedate.check_args(test_date, self.test_turn_time)
        self.assertTrue(
            "You can submit requests from 9AM till 5PM." in str(context.exception))

    def test_add(self):
        """
        Testing the return value of the calculate method.
        """
        result = CalculateDueDate.add(self.test_time, self.test_turn_time)
        self.assertEqual(dt.datetime(2021, 6, 18, 15, 0, 0), result)

    def test_friday_8_hours(self):
        """
        Testing the return value of the calculate method on Friday with 8 hours turn_time.
        """
        test_time = dt.datetime(2021, 6, 18, 15, 0, 0)
        test_turn_time = 8
        result = CalculateDueDate.add(test_time, test_turn_time)
        self.assertEqual(dt.datetime(2021, 6, 21, 15, 0, 0), result)

    def test_0_turn_time(self):
        """
        Testing the return value of the calculate method with 0 hours turn_time.
        """
        test_time = dt.datetime(2021, 6, 18, 15, 0, 0)
        test_turn_time = 0
        result = CalculateDueDate.add(test_time, test_turn_time)
        self.assertEqual(dt.datetime(2021, 6, 18, 15, 0, 0), result)


if __name__ == "__main__":
    unittest.main()
