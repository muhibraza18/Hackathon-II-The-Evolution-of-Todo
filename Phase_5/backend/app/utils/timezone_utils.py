from datetime import datetime, timezone, timedelta
from typing import Optional
import pytz


class TimezoneUtils:
    """Utility class for handling timezone conversions related to due dates."""

    @staticmethod
    def convert_to_utc(dt: datetime, source_timezone_str: Optional[str] = None) -> datetime:
        """
        Convert a datetime to UTC.

        Args:
            dt: The datetime to convert
            source_timezone_str: The source timezone string (e.g., 'America/New_York')

        Returns:
            Datetime in UTC
        """
        if dt.tzinfo is None:
            # If datetime is naive, assume it's in the source timezone or UTC
            if source_timezone_str:
                tz = pytz.timezone(source_timezone_str)
                dt = tz.localize(dt)
            else:
                # Assume naive datetime is in UTC
                dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    @staticmethod
    def convert_from_utc_to_local(utc_dt: datetime, target_timezone_str: str) -> datetime:
        """
        Convert a UTC datetime to a local timezone.

        Args:
            utc_dt: The UTC datetime to convert
            target_timezone_str: The target timezone string (e.g., 'America/New_York')

        Returns:
            Datetime in the target timezone
        """
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)

        target_tz = pytz.timezone(target_timezone_str)
        return utc_dt.astimezone(target_tz)

    @staticmethod
    def get_user_timezone_offset_minutes(user_timezone_str: str) -> int:
        """
        Get the timezone offset in minutes for a given timezone string.

        Args:
            user_timezone_str: The timezone string (e.g., 'America/New_York')

        Returns:
            Timezone offset in minutes
        """
        tz = pytz.timezone(user_timezone_str)
        now = datetime.now(tz)
        offset_seconds = now.utcoffset().total_seconds()
        return int(offset_seconds // 60)

    @staticmethod
    def format_due_date_for_timezone(due_date: Optional[datetime], user_timezone_str: str, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
        """
        Format a due date for a specific user's timezone.

        Args:
            due_date: The due date to format
            user_timezone_str: The user's timezone string
            format_str: The format string for output

        Returns:
            Formatted date string in user's timezone
        """
        if due_date is None:
            return ""

        if due_date.tzinfo is None:
            # Assume naive datetime is in UTC
            due_date = due_date.replace(tzinfo=timezone.utc)

        user_tz = pytz.timezone(user_timezone_str)
        local_due_date = due_date.astimezone(user_tz)
        return local_due_date.strftime(format_str)

    @staticmethod
    def get_current_time_in_timezone(timezone_str: str) -> datetime:
        """
        Get the current time in a specific timezone.

        Args:
            timezone_str: The timezone string (e.g., 'America/New_York')

        Returns:
            Current datetime in the specified timezone
        """
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz)

    @staticmethod
    def is_same_day_in_timezone(dt1: datetime, dt2: datetime, timezone_str: str) -> bool:
        """
        Check if two datetimes represent the same day in a specific timezone.

        Args:
            dt1: First datetime
            dt2: Second datetime
            timezone_str: The timezone string to compare in

        Returns:
            True if both datetimes represent the same day in the timezone, False otherwise
        """
        tz = pytz.timezone(timezone_str)

        if dt1.tzinfo is None:
            dt1 = dt1.replace(tzinfo=timezone.utc)
        if dt2.tzinfo is None:
            dt2 = dt2.replace(tzinfo=timezone.utc)

        local_dt1 = dt1.astimezone(tz)
        local_dt2 = dt2.astimezone(tz)

        return local_dt1.date() == local_dt2.date()

    @staticmethod
    def add_timezone_offset(dt: datetime, offset_minutes: int) -> datetime:
        """
        Add a timezone offset to a datetime.

        Args:
            dt: The datetime to adjust
            offset_minutes: The offset in minutes

        Returns:
            Adjusted datetime
        """
        offset = timedelta(minutes=offset_minutes)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt + offset

    @staticmethod
    def validate_timezone(timezone_str: str) -> bool:
        """
        Validate if a timezone string is valid.

        Args:
            timezone_str: The timezone string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            pytz.timezone(timezone_str)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False