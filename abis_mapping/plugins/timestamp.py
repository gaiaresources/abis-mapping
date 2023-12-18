"""Provides custom frictionless timestamp plugin for the package"""


# Standard
import datetime
import re

# Third-Party
import attrs
import frictionless

# Local
from abis_mapping.utils import types
from abis_mapping.utils import timestamps

# Typing
from typing import Any, Optional, Type


class TimestampPlugin(frictionless.Plugin):
    """Custom Timestamp Plugin"""

    # Class Attributes
    code = "timestamp"
    status = "stable"

    def select_field_class(self, type: Optional[str] = None) -> Optional[Type[frictionless.Field]]:
        """Return the custom field class for the plugin.

        Args:
            type (str): Denotes the type passed in from the frictionless
                framework for a field.

        Returns:
            Optional[Type[frictionless.Field]]: Reference to TimestampField if type
                matches code else None.
        """
        if type == self.code:
            return TimestampField
        return None


@attrs.define(kw_only=True, repr=False)
class TimestampField(frictionless.Field):
    """Custom timestamp type implementation."""

    # Class attributes
    type = "timestamp"
    builtin = False
    supported_constraints = [
        "required",
        "minimum",
        "maximum",
        "enum"
    ]

    # Flags to allow for year and yearMonth types
    allow_year: bool = False
    allow_year_month: bool = False

    def create_value_reader(self) -> frictionless.schema.types.IValueReader:
        """Creates value reader callable."""

        def value_reader(cell: Any) -> types.Timestamp | None:
            """Convert cell (read direction).

            Args:
                cell (Any): Cell to convert

            Returns:
                Optional[types.DateOrDatetime]: Converted cell, or none if invalid.
            """
            # Perform year only parsing if enabled
            if self.allow_year:
                if (res_year := self._year_reader(cell)) is not None:
                    return res_year

            # Perform yearmonth parsing if enabled
            if self.allow_year_month:
                if (res_ym := self._year_month_reader(cell)) is not None:
                    return res_ym

            # Base implementation proceeds for only date or datetime possibilities
            # Check that cell is not already a "date" or "datetime"
            if isinstance(cell, (datetime.date, datetime.datetime)):
                return cell
            # Check that cell is a string
            if not isinstance(cell, str):
                # Invalid
                return None

            # Catch Parsing Errors
            try:
                # Parse and return
                return timestamps.parse_timestamp(cell)

            except ValueError:
                # Invalid
                return None

        # Return value_reader callable
        return value_reader

    def _year_month_reader(self, cell: Any) -> types.YearMonth | None:
        """Attempts to convert cell into a yearmonth tuple.

        Formats accepted:
        - YYYY-mm
        - (m)m/YYYY - month does not have to be zero padded when less than 10

        Args:
            cell (Any): Cell to convert.

        Returns:
            types.YearMonth | None: Converted cell, or None if invalid

        """
        # Check that the cell is not already a tuple or list for year month
        if (
            isinstance(cell, (tuple, list))
            and len(cell) == 2
            and timestamps.is_year(cell[0])
            and timestamps.is_month(cell[1])
        ):
            return types.YearMonth(year=cell[0], month=cell[1])
        # Check that cell is a string
        if not isinstance(cell, str):
            return None

        # Construct regexes for each of the year-month possibilities
        year_month_dash = re.compile(r"^(\d{4})-(\d{2})$")
        year_month_slash = re.compile(r"^(\d{1,2})/(\d{4})$")

        # Match for the YYYY-MM format
        if match := year_month_dash.match(cell):
            # Parse the matched nums
            month = int(match.group(2))
            year = int(match.group(1))
            # Confirm sensical number ranges
            if not timestamps.is_year(year) or not timestamps.is_month(month):
                # Invalid
                return None
            return types.YearMonth(year=year, month=month)

        # Match for the mm/YYYY format
        if match := year_month_slash.match(cell):
            # Parse the matched nums
            month = int(match.group(1))
            year = int(match.group(2))
            # Confirm sensical number ranges
            if not timestamps.is_year(year) or not timestamps.is_month(month):
                # Invalid
                return None
            return types.YearMonth(year=year, month=month)

        return None

    def _year_reader(self, cell: Any) -> int | None:
        """Attempts to convert a cell into a year number.

        Year format is YYYY only (must be four digits when string)

        Args:
            cell (Any): Cell to convert.

        Returns:
            int | None: Year number if successful or None otherwise.
        """
        # Check that the cell is not already an int for a year
        if isinstance(cell, int) and timestamps.is_year(cell):
            return cell
        # Check that cell is a string
        if not isinstance(cell, str):
            return None

        # Construct regex for year possibility
        year_only = re.compile(r"^\d{4}$")

        # Perform match and convert if possible
        if year_only.match(cell):
            year = int(cell)
            if not timestamps.is_year(year):
                # Invalid
                return None
            # Return year number
            return year

        # Shouldn't make it here
        return None

    def create_value_writer(self) -> frictionless.schema.types.IValueWriter:
        """Creates value writer callable."""
        def value_writer(cell: types.Timestamp) -> str:
            """Convert cell (write direction)

            Args:
                cell (types.DateOrDatetime | int | types.YearMonth): Cell to convert

            Returns:
                str: Converted cell
            """
            # Perform serialization to iso format for DateOrDatetime
            if isinstance(cell, (datetime.datetime, datetime.date)):
                return cell.isoformat()

            # Perform serialization for Yearmonth or Year
            match cell:
                case types.YearMonth(year=year, month=month):
                    return f"{year}-{month:02}"
                case _:
                    return str(cell)

        # Return value writer callable
        return value_writer

    # Add the extra params to the metadata profile
    metadata_profile_patch = {
        "properties": {
            "allowYear": {"type": "boolean"},
            "allowYearMonth": {"type": "boolean"}
        }
    }


# Register Timestamp Plugin
frictionless.system.register(
    name=TimestampPlugin.code,
    plugin=TimestampPlugin(),
)
