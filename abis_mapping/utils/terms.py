"""Provides custom implementations of rdflib terms"""

# Standard
import uuid

# Third-party
import rdflib
import rdflib.term

# Typing
from typing import Generator, Callable


class BNodeAlwaysUUID4(rdflib.BNode):
    def __new__(
        cls,
        value: str | None = None,
        _sn_gen: Callable[[], str] | Generator | None = None,
        _prefix: str = "N",
    ) -> "BNodeAlwaysUUID4":
        """This overrides the base implementation.

        It only assigns new ids using uuid4s, avoiding identifier collisions
        during set-theoretic union operations (and other areas of concern).

        Args:
            value (str | None): Would typically be assigned as identifier but
                here should only be `None`. A string value will raise an exception.
            _sn_gen (callable[[], str] | Generator | None): A custom supplied str generating
                function or generator that could be used to generate ids. Again this
                should only be `None`, supplying anything else will cause an exception.
            _prefix (str): Prefix to be prepended to produced node identifier.

        Returns:
            rdflib.BNode: Newly created blank node.

        Raises:
            ValueError: When a value besides `None` is supplied for arguments `value`
                or `_sn_gen`.
        """
        # Check to see value and _sn_gen are both None
        if value is not None or _sn_gen is not None:
            raise ValueError(
                f"Arguments supplied for `value` and `_sn_gen` should be `None`;"
                f"got value={value} and _sn_gen={_sn_gen}."
                "This is a custom implementation of rdflib.BNode."
            )

        # Produce node_id
        node_id = uuid.uuid4().hex

        # Create value
        value = _prefix + f"{node_id}"

        return super().__new__(cls, value, _prefix=_prefix)  # type: ignore[return-value]
