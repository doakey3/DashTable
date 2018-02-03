from .is_only import is_only


class Cell():
    """
    Holds the text and data for an rst text cell
    """
    def __init__(self, text, row, column, row_count, column_count):
        """
        Initializes the Cell class

        Parameters
        ----------
        text : str
            The string of a grid cell. For example::

                +-----+
                | foo |
                +-----+

        row : int
            The row where this cell is located in the table
        column : int
            The column where this cell is located in the table
        row_count : int
            The number of rows this cell spans
        column_count : int
            The number of columns this cell spans
        """
        self.text = text
        self.row = row
        self.column = column
        self.row_count = row_count
        self.column_count = column_count

    @property
    def left_sections(self):
        """
        The number of sections that touch the left side.

        During merging, the cell's text will grow to include other
        cells. This property keeps track of the number of sections that
        are touching the left side. For example::

                        +-----+-----+
            section --> | foo | dog | <-- section
                        +-----+-----+
            section --> | cat |
                        +-----+

        Has 2 sections on the left, but 1 on the right

        Returns
        -------
        sections : int
            The number of sections on the left
        """
        lines = self.text.split('\n')
        sections = 0

        for i in range(len(lines)):
            if lines[i].startswith('+'):
                sections += 1
        sections -= 1

        return sections

    @property
    def right_sections(self):
        """
        The number of sections that touch the right side.

        Returns
        -------
        sections : int
            The number of sections on the right
        """
        lines = self.text.split('\n')
        sections = 0
        for i in range(len(lines)):
            if lines[i].endswith('+'):
                sections += 1
        return sections - 1

    @property
    def top_sections(self):
        """
        The number of sections that touch the top side.

        Returns
        -------
        sections : int
            The number of sections on the top
        """

        top_line = self.text.split('\n')[0]
        sections = len(top_line.split('+')) - 2

        return sections

    @property
    def bottom_sections(self):
        """
        The number of cells that touch the bottom side.

        Returns
        -------
        sections : int
            The number of sections on the top
        """
        bottom_line = self.text.split('\n')[-1]
        sections = len(bottom_line.split('+')) - 2

        return sections

    @property
    def is_header(self):
        """
        Whether or not the cell is a header

        Any header cell will have "=" instead of "-" on its border.

        For example, this is a header cell::

            +-----+
            | foo |
            +=====+

        while this cell is not::

            +-----+
            | foo |
            +-----+

        Returns
        -------
        bool
            Whether or not the cell is a header
        """
        bottom_line = self.text.split('\n')[-1]

        if is_only(bottom_line, ['+', '=']):
            return True

        return False

    def __lt__(self, other):
        """For sorting instances of this class."""
        return [self.row, self.column] < [other.row, other.column]
