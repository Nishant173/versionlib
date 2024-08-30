from __future__ import annotations

from collections import Counter
import string
from typing import Any, Tuple


CHARSET = set(string.digits + ".")
DIGITS = set(string.digits)


class Comparator:
    GT = ">"
    LT = "<"
    EQ = "=="


class ComparatorCollection:
    GTE = set([
        Comparator.GT,
        Comparator.EQ,
    ])
    LTE = set([
        Comparator.LT,
        Comparator.EQ,
    ])


class Version:
    """Class that represents a Version"""

    def __init__(self, version: str, /) -> None:
        Version._validate(version)
        self.version = version

    @staticmethod
    def _validate(version: Any, /) -> None:
        if not isinstance(version, str):
            raise TypeError(f"Expected param `version` to be a non-empty string; got value `{version}`")
        if not (
            bool(version)
            and all((char in CHARSET for char in version))
            and version[0] in DIGITS
            and version[-1] in DIGITS
        ):
            raise ValueError(f"Param `version` is invalid; got value `{version}`")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(version='{self.version}')"

    def __eq__(self, other: Version) -> bool:
        return Version._compare(self, other) == Comparator.EQ

    def __ne__(self, other: Version) -> bool:
        return not (self == other)

    def __gt__(self, other: Version) -> bool:
        return Version._compare(self, other) == Comparator.GT

    def __ge__(self, other: Version) -> bool:
        return Version._compare(self, other) in ComparatorCollection.GTE

    def __lt__(self, other: Version) -> bool:
        return Version._compare(self, other) == Comparator.LT

    def __le__(self, other: Version) -> bool:
        return Version._compare(self, other) in ComparatorCollection.LTE

    def _get_num_components(self) -> int:
        """Returns the number of components"""
        return Counter(self.version).get(".", 0) + 1

    @staticmethod
    def _compute_filler(*, difference: int) -> str:
        return "".join((".0" for _ in range(difference)))

    @staticmethod
    def _fill_gaps(a: Version, b: Version, /) -> Tuple[Version, Version]:
        """Returns tuple of 2 new Version instances after filling the gaps (if any)"""
        num_components_a = a._get_num_components()
        num_components_b = b._get_num_components()
        difference = abs(num_components_a - num_components_b)
        if num_components_a > num_components_b:
            new_b = b.version + Version._compute_filler(difference=difference)
            return (
                Version(a.version),
                Version(new_b),
            )
        elif num_components_a < num_components_b:
            new_a = a.version + Version._compute_filler(difference=difference)
            return (
                Version(new_a),
                Version(b.version),
            )
        return (
            Version(a.version),
            Version(b.version),
        )

    @staticmethod
    def _compare(a: Version, b: Version, /) -> str:
        """
        Returns one of: [">", "<", "=="].
            - If a > b, returns ">"
            - If a < b, returns "<"
            - If a == b, returns "=="
        """
        if a.version == b.version:
            return Comparator.EQ
        a, b = Version._fill_gaps(a, b)
        if a.version == b.version:
            return Comparator.EQ
        components_a, components_b = a.version.split("."), b.version.split(".")
        for component_a, component_b in zip(components_a, components_b):
            temp_a = int(component_a)
            temp_b = int(component_b)
            if temp_a > temp_b:
                return Comparator.GT
            elif temp_a < temp_b:
                return Comparator.LT
        return Comparator.EQ

