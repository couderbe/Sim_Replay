import re

# SDVFR Patterns
SDVFR_GS_FR = r"Vitesse\s*:\s*(\d+)\s*kmh"
SDVFR_HEADING_FR = r"Cap\s*:\s*(\d+)[^0-9]+"


class SpecificParser:
    """Utility Class to parse Supplementary data found in information tag in GPX files (like Speed for SDVFR).

    Attributes:
        headers (dict): dictionnary that associates attribute data name and Pattern.
    """

    def __init__(self, init_descr: str):
        """Initializes headers with all attribute data name and Pattern pair that can be found in the initial description.

        **For each Attribute, the last matching Pattern will be used**

        Args:
            init_descr (str): the first description used to initiate supplementary data availability.
        """
        self.headers: dict = {}
        if self._pattern_matcher(init_descr, SDVFR_GS_FR) != None:
            self.headers["GPS GROUND SPEED"] = SDVFR_GS_FR
        if self._pattern_matcher(init_descr, SDVFR_HEADING_FR) != None:
            self.headers["GPS GROUND TRUE HEADING"] = SDVFR_HEADING_FR

    def parse_data(self, descr):
        """Retrieves data in a description that corresponds to the Patterns listed in headers.

        Args:
            descr (str): the description containing data.
        Returns:
            dict: a dictionnary containing attribute name as key and its associated data as value.
        """
        res: dict = {}
        for k, p in self.headers.items():
            res[k] = self._pattern_matcher(descr, p) or 0.0  # default value
        return res

    def _pattern_matcher(self, str: str, pattern) -> int | None:
        if str != None:
            matched = re.search(pattern, str)
            if matched:
                # Convert numbers when possible
                return int(matched.group(1))
        return None
