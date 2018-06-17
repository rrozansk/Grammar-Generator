"""
A scanner/parser generator targeting python.
Generates a single python (.py) file.
"""
from . import Generator


class Python(Generator):
    """
    A simple object for compiling scanner's and/or parser's to python programs.
    """

    def _output(self, filename):
        super(Python, self).output(filename)

    def output(self, filename):
        """
        Attempt to generate the python (.py) source file with the corresponding
        scanner and/or parser currently set in the object.

        Input Type:
          filename: String

        Output Type: List[Tuple[String, String]] | ValueError
        """
        if not isinstance(filename, str):
            raise ValueError('Invalid Input [Python Gen]: filename must be a string')

        if not filename:
            raise ValueError('Invalid Input [Python Gen]: filename must be a non empty string')

        return [(filename+'.py', self._output(filename))]
