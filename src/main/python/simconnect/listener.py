from abc import abstractmethod


class Listener:

    @abstractmethod
    def apply(val):
        """function called when the listened component send a value

        Args:
            val (_type_): the value sent by the listened compoenent
        """