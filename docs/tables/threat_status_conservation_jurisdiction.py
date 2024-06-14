"""Tool for generating the threat status conservation jurisdiction table."""

# Standard
import io
import csv

# Third-party
import pydantic

# Local
from docs import tables
from abis_mapping import utils

# Typing
from typing import IO

class ThreatStatConsJurTableRow(pydantic.BaseModel):
    """Threat status conservation jurisdiction table row."""
    conservation_jurisdiction: str = pydantic.Field(serialization_alias="conservationJurisdiction")
    threat_status: str = pydantic.Field(serialization_alias="threatStatus")
    threat_status_alt_labels: str = pydantic.Field(serialization_alias="threatStatus alternative labels")


class ThreatStatConsJurTabler(tables.base.BaseTabler):

    def generate_table(
        self,
        dest: IO | None = None,
        as_markdown: bool = False,
    ) -> str:
        """Generates threat status conservation jurisdiction table.

        Args:
            dest (IO, optional): Destination file. Defaults to None.
            as_markdown (bool, optional): True to generate a markdown table. Defaults to False, as csv.

        Returns:
            str: Table either in markdown or csv.
        """
        # Create in-memory io
        output = io.StringIO()

        # Get header list
        header = [hdr.serialization_alias for hdr in ThreatStatConsJurTableRow.model_fields.values()]

        # Create writer
        if as_markdown:
            writer = tables.base.MarkdownDictWriter(output, fieldnames=header)
        else:
            writer = csv.DictWriter(output, fieldnames=header)

        writer.writeheader()

        # Iterate through vocab's terms
        for term in sorted(utils.vocabs.get_vocab("threatStatus").terms, key=lambda x: x.preferred_label):
            # Generate row
            row = self.generate_row(term)
            # Write to output
            writer.writerow(row.model_dump(by_alias=True))

        # Write to destination
        if dest is not None:
            print(output.getvalue(), file=dest)

        # Return
        return output.getvalue()

    def generate_row(
        self,
        threat_stat_cons_jur_term: utils.vocabs.Term
    ) -> ThreatStatConsJurTableRow:
        """Generates a single row for the table.

        Args:
            threat_stat_cons_jur_term (utils.vocabs.Term): Threat
                status conservation jurisdiction term.

        Return;
            ThreatStatConsJurTableRow: Table row.
        """
        # Split out preferred label
        splt_preferred = threat_stat_cons_jur_term.preferred_label.split('/')

        # Split threat status alt labels
        threat_stat_alt: list[list[str]] = [lbl.split('/')[1] for lbl in threat_stat_cons_jur_term.alternative_labels]

        # Perform mapping
        row = ThreatStatConsJurTableRow(
            conservation_jurisdiction=splt_preferred[0],
            threat_status=splt_preferred[1],
            threat_status_alt_labels=", ".join(threat_stat_alt),
        )

        # Return
        return row
