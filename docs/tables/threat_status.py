"""Tool for generating the threat status conservation authority table."""

# Standard
import argparse
import sys

# Third-party
import pydantic

# Local
from docs import tables
from abis_mapping import utils

# Typing
from typing import IO, Literal


class ThreatStatusRow(pydantic.BaseModel):
    """Threat status conservation Authority table row."""

    conservation_authority: str = pydantic.Field(serialization_alias="conservationAuthority")
    threat_status: str = pydantic.Field(serialization_alias="threatStatus")
    threat_status_alt_labels: str = pydantic.Field(serialization_alias="threatStatus alternative labels")


class ThreatStatusRowDeprecated(ThreatStatusRow):
    """Threat status conservation jurisdiction table row."""

    # Redefine as previously conservationAuthority was declared as conservationJurisdiction
    conservation_authority: str = pydantic.Field(serialization_alias="conservationJurisdiction")


class ThreatStatusTabler(tables.base.BaseTabler):
    """Tabler implementation for the threat status table."""

    # Class attributes
    alignment = ["c", "l", "l"]
    SupportedFormats = Literal["csv", "markdown"]

    def __init__(
        self,
        template_id: str,
        format: SupportedFormats = "csv",  # noqa: A002
    ) -> None:
        """Constructor for ThreatStatConsJurTabler.

        Args:
            template_id (str): ID of mapper template.
            format (SupportedFormats, optional): Output
                format of the table should be one of supported formats, default is "csv".

        Raises:
            ValueError: If the threat status vocabulary isn't used
                by the mapper template.
        """
        super().__init__(template_id=template_id, format=format)
        fields = self.mapper.schema()["fields"]
        if not [fld for fld in fields if fld.get("vocabularies") and "THREAT_STATUS" in fld.get("vocabularies")]:
            raise ValueError(f"No THREAT_STATUS vocabularies found for template {template_id}")

    @property
    def header(self) -> list[str]:
        """Getter for the header row."""
        # Pick and set the correct row model for the instance
        fields = self.mapper.fields()
        self.row_model = ThreatStatusRow if "conservationAuthority" in fields else ThreatStatusRowDeprecated

        # Get header list
        raw_hdr = (hdr.serialization_alias or hdr.title for hdr in self.row_model.model_fields.values())
        return [hdr for hdr in raw_hdr if hdr is not None]

    def generate_table(
        self,
        dest: IO[str] | None = None,
    ) -> str:
        """Generates threat status conservation authority table.

        Args:
            dest (IO, optional): Destination file. Defaults to None.

        Returns:
            str: Table either in markdown or csv.
        """
        # Write header
        self.writer.writeheader()

        # Iterate through vocab's terms
        for term in sorted(utils.vocabs.get_vocab("THREAT_STATUS").terms, key=lambda x: x.preferred_label):  # type: ignore[arg-type, return-value]
            # Generate row
            row = self.generate_row(term)
            # Write to output
            self.writer.writerow(row.model_dump(by_alias=True))

        # Write to destination
        if dest is not None:
            print(self.output.getvalue(), file=dest)

        # Return
        return self.output.getvalue()

    def generate_row(self, threat_stat_cons_jur_term: utils.vocabs.Term) -> ThreatStatusRow:
        """Generates a single row for the table.

        Args:
            threat_stat_cons_jur_term (utils.vocabs.Term): Threat
                status conservation authority term.

        Return;
            ThreatStatusRow: Table row.

        Raises:
            ValueError: If there is no preferred label for the supplied Term.'
        """
        # Check preferred label
        if (preferred_label := threat_stat_cons_jur_term.preferred_label) is not None:
            # Split out preferred label
            splt_preferred = preferred_label.split("/")
        else:
            # Raise
            raise ValueError(f"No preferred label for {threat_stat_cons_jur_term}")

        # Split threat status alt labels
        threat_stat_alt: set[str] = {lbl.split("/")[1] for lbl in threat_stat_cons_jur_term.alternative_labels}
        threat_stat_alt.difference_update({splt_preferred[1]})

        # Perform mapping
        row = self.row_model(
            conservation_authority=splt_preferred[0],
            threat_status=splt_preferred[1],
            threat_status_alt_labels=", ".join(sorted(threat_stat_alt)),
        )

        # Return
        return row


if __name__ == "__main__":
    """Main entry point."""
    # Create argument parser
    parser = argparse.ArgumentParser(description="A tool to generate a csv table of vocabularies from a mapper.")
    parser.add_argument("template_id", type=str, help="ID of the template.")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout.",
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Create tabler
    tabler = tables.threat_status.ThreatStatusTabler(args.template_id)

    # Generate table
    tabler.generate_table(args.output_dest)
