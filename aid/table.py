"""Table classes and functions."""


class Table():
    """Table class."""

    def __init__(self, table=None, column_paddings=None):
        """Initialise object."""
        self.table = table

        # How many spaces there are to the LEFT of the column.
        # First row gets ignored.
        self.column_paddings = column_paddings

        if self.table is None:
            self.table = []
        if self.column_paddings is None:
            self.column_paddings = []

    @property
    def column_widths(self):
        """Get a list of column widths."""
        widths = []

        for row in self.table:
            for i, cell in enumerate(row):
                cell_size = len(cell.content)

                if len(widths) <= i:
                    widths.append(0)

                if widths[i] < cell_size:
                    widths[i] = cell_size

        return widths

    def __str__(self):
        """Get a table string representation."""
        string = ""
        column_widths = self.column_widths

        for row in self.table:
            if string != "":
                string += "\n"

            for i, cell in enumerate(row):
                string += (" " * self.get_column_padding(i))
                string += cell.get_cell_string(column_widths[i])

        return string

    async def add_row(self, row):
        """Add a row to the table."""
        self.table.append(row)

    async def add_column(self, column):
        """Add a column to the table."""
        for i, cell in enumerate(column):
            if i < len(self.table):
                row = self.table[i]
                row.append(column[i])
            else:
                await self.add_row([column[i]])

    def get_column_padding(self, index):
        """Get the padding of a column."""
        if index == 0:
            return 0

        index -= 1
        if index < len(self.column_paddings):
            return self.column_paddings[index]

        return 1


class TableCell():
    """Table cell class."""

    def __init__(self, content="", alignment="<"):
        """Initialise object."""
        self.content = str(content)
        self.alignment = alignment

    def get_cell_string(self, filling):
        """Get the cell string."""
        cell_string = "{cell.content:" + self.alignment + str(filling) + "}"
        return cell_string.format(cell=self)
