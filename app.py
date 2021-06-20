"""
We are looking for a solution that implements a due date calculator in an issue
tracking system. Your task is to implement the CalculateDueDate method:
• Input: Takes the submit date/time and turnaround time.
• Output: Returns the date/time when the issue is resolved.
Rules
• Working hours are from 9AM to 5PM on every working day, Monday to Friday.
• Holidays should be ignored (e.g. A holiday on a Thursday is considered as a
working day. A working Saturday counts as a non-working day.).
• The turnaround time is defined in working hours (e.g. 2 days equal 16 hours).
If a problem was reported at 2:12PM on Tuesday and the turnaround time is
16 hours, then it is due by 2:12PM on Thursday.
• A problem can only be reported during working hours. (e.g. All submit date
values are set between 9AM to 5PM.)
• Do not use any third-party libraries for date/time calculations (e.g. Moment.js,
Carbon, Joda, etc.) or hidden functionalities of the built-in methods.
Additional info
• Use your favourite programming language.
• Do not implement the user interface or CLI.
• Do not write a pseudo code. Write a code that you would commit/push to a
repository and which solves the given problem.
• You can submit your solution even if you have not finished it fully.
Bonus – Not mandatory
• Including automated tests to your solution is a plus.
• Test-driven (TDD) solutions are especially welcome.
• Clean Code (by Robert. C. Martin) makes us happy.
"""

import datetime as dt


class CalculateDueDate:
    """
    This class will handle the due time calculation.
    Input: 
        submit_time -> dt.datetime 
        turn_time -> int
    Output: 
        dt.datetime.now() + turn_time (modified based on the rules) -> dt.datetime 
    Call: duetime = CalculateDueDate(submit_time, turn_time); duetime.main()
    """

    def __init__(self, submit_time: dt.datetime, turn_time: int):
        self.submit_time = submit_time
        self.turn_time = turn_time

    @staticmethod
    def check_args(submit_time: dt.datetime, turn_time: int):
        """
        This method will check if the arguments meet the requirements or not.
        """

        if not isinstance(submit_time, dt.datetime):
            raise TypeError(
                "Invalid input format. 'submit_time' must be <datetime> format.")

        if not isinstance(turn_time, int):
            raise TypeError(
                "Invalid input format. 'turn_time' must be <int> format.")

        if submit_time.weekday() in [5, 6]:
            raise ValueError("You can submit requests during weekdays only.")
        else:
            if dt.time(17, 0, 0) >= submit_time.time() >= dt.time(9, 0, 0):
                pass
            else:
                raise ValueError(
                    "You can submit requests from 9AM till 5PM.")

    @staticmethod
    def add(submit_time: dt.datetime, turn_time: int) -> dt.datetime:
        """
        This function will calculate the due time.
        """
        turn_time_in_sec = turn_time * 3600  # we have to change the time into seconds
        due_date = submit_time

        while turn_time_in_sec > 0:
            remaining_time_sec = (dt.datetime(
                due_date.year, due_date.month, due_date.day, 17, 0, 0) - due_date).total_seconds()

            if remaining_time_sec > turn_time_in_sec:
                due_date += dt.timedelta(seconds=turn_time_in_sec)
                turn_time_in_sec = 0

            else:
                due_date += dt.timedelta(seconds=remaining_time_sec)
                turn_time_in_sec -= remaining_time_sec

            # if due_date is at 5PM and there is still remaining time then we have to increase the value till next-day 9AM
            if turn_time_in_sec != 0:
                due_date += dt.timedelta(hours=16)
            else:
                pass

            # If the (previously increased) due_date was weekend we would have to increase the value further till the next Monday
            if due_date.weekday() == 5:
                due_date += dt.timedelta(days=2)
            elif due_date.weekday() == 6:
                due_date += dt.timedelta(days=1)

        return due_date

    def main(self):
        """
        Main method of the class.
        Handles the proper value return.
        """
        self.check_args(self.submit_time, self.turn_time)
        return CalculateDueDate.add(self.submit_time, self.turn_time)
