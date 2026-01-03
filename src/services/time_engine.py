"""
Time Engine
Handles time-related operations including recurring logic, reminders, and date formatting.
"""

from datetime import datetime, timedelta
from typing import Optional


class TimeSkill:
    """Generic time handling class for recurring logic, reminders, and date formatting."""

    @staticmethod
    def calculate_next_date(current_date: str, frequency: str) -> Optional[str]:
        """
        Calculate the next date based on the current date and frequency.

        Args:
            current_date: Current date in ISO format (YYYY-MM-DD)
            frequency: Frequency of recurrence ('daily', 'weekly', 'monthly')

        Returns:
            Next date in ISO format (YYYY-MM-DD) or None if invalid frequency
        """
        try:
            date_obj = datetime.strptime(current_date, '%Y-%m-%d')

            if frequency.lower() == 'daily':
                next_date = date_obj + timedelta(days=1)
            elif frequency.lower() == 'weekly':
                next_date = date_obj + timedelta(weeks=1)
            elif frequency.lower() == 'monthly':
                # Calculate next month - handle month overflow
                if date_obj.month == 12:
                    next_date = date_obj.replace(year=date_obj.year + 1, month=1)
                else:
                    next_date = date_obj.replace(month=date_obj.month + 1)
            else:
                return None

            return next_date.strftime('%Y-%m-%d')
        except ValueError:
            return None

    @staticmethod
    def is_reminder_due(due_date: str) -> bool:
        """
        Check if a due date is within the next 24 hours.

        Args:
            due_date: Due date in ISO format (YYYY-MM-DD)

        Returns:
            True if the due date is within the next 24 hours, False otherwise
        """
        try:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            now = datetime.now()
            tomorrow = now + timedelta(days=1)

            # Check if due date is today or tomorrow
            due_date_start = datetime(due_date_obj.year, due_date_obj.month, due_date_obj.day)
            due_date_end = due_date_start + timedelta(days=1)

            return due_date_start <= tomorrow < due_date_end
        except ValueError:
            return False

    @staticmethod
    def is_due_within_hours(due_date: str, hours: int = 1) -> bool:
        """
        Check if a due date is within the specified number of hours.

        Args:
            due_date: Due date in ISO format (YYYY-MM-DD)
            hours: Number of hours to check (default: 1)

        Returns:
            True if the due date is within the specified hours, False otherwise
        """
        try:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            now = datetime.now()
            future_time = now + timedelta(hours=hours)

            # Check if due date is today and within the specified hours
            due_date_start = datetime(due_date_obj.year, due_date_obj.month, due_date_obj.day)
            due_date_end = due_date_start + timedelta(days=1)

            return due_date_start <= future_time < due_date_end
        except ValueError:
            return False

    @staticmethod
    def format_date(date_str: str) -> Optional[str]:
        """
        Ensure the date follows ISO format (YYYY-MM-DD).

        Args:
            date_str: Date string in any format

        Returns:
            Date in ISO format (YYYY-MM-DD) or None if invalid
        """
        try:
            # Try to parse the date in various formats and return in ISO format
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                # Already in YYYY-MM-DD format
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            else:
                # Try to parse other formats and convert to ISO
                date_obj = datetime.fromisoformat(date_str.replace('T', ' ').split('.')[0])
                return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                # Try common formats
                formats = ['%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y']
                for fmt in formats:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        return date_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
                return None
            except:
                return None