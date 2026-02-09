from abc import abstractmethod


class Interpoler:
    
    @abstractmethod
    def compute_interpolation(self, index:int, current_time:float)->dict:
        """Computes the current state based on a temporal interpolation.
            Has to be implemented.

        Args:
            index (int): the index of the data interpolated
            current_time (float): the current time of interpolation

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")