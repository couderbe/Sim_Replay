class Source:

    def get_param_value_from_name(self, param: str):
        """Getter of a data with a specific name.
            Has to be implemented.

        Args:
            param (str): the name of the desired data

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")
