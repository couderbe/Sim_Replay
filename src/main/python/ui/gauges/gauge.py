from abc import abstractmethod

class Gauge:

    @abstractmethod
    def updateValues(val:dict)->None:
        """Updates the values displayed in the Gauge.
            Has to be implemented.

        Args:
            val (dict): the set of datas that the gauge partially uses

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")