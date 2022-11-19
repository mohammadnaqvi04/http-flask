from dataclasses import dataclass
from flask import Response, abort

@dataclass
class Assay:
    """Class for representing an assay

        Attributes:
            name (str): A string.
            size (int): An integer for number of wells in assay. 
                        Can take on either 96 or 384.
            id (int): A unique integer identifier for an assay.

    """
    # an id that updates with each instantiation of an assay
    uniqueID = 1

    def __init__(self, name, size, id):
        self.name = name
        self.size = size
        self.id = id
        self.grid = self.make_wells(size)
        self.num_rows = len(self.grid)
        self.num_columns = len(self.grid[0])

    def make_wells(self, size):
        if size == 384:
            rows, columns = 24, 16
        elif size == 96:
            rows, columns = 12, 8
        else:
            resp = Response(status=404)
            resp.headers["Message"] = "Assay can only have either 96 or 384 wells."
            return abort(resp)
        
        return [[None for x in range(columns)] for y in range(rows)]
    
    def as_json(self):
        grid_json = {}
        rows, columns = len(self.grid), len(self.grid[0])
        for i in range(rows):
            for j in range(columns):
                if self.grid[i][j]:
                    grid_json[f"{i+1}, {j+1}"] = {
                                                "cell_line":self.grid[i][j].cell_line,
                                                "chemical":self.grid[i][j].chemical,
                                                "concentration":self.grid[i][j].concentration
                                               }
        return {
            "id":self.id, 
            "name":self.name, 
            "size":self.size,
            "plate":grid_json
        }
    
    def insert_well(self, row, col, cell_line, chemical, concentration):
        if row < 0 or row > self.num_rows - 1 or col < 0 or col > self.num_columns -1:
            resp = Response(status=404)
            resp.headers["Message"] = "You are attempting to access a row or column out of the assay's scope."
            return abort(resp)
        else: 
            self.grid[row][col] = Well(row, col, cell_line, chemical, concentration)
    
    def update_grid(self, row, col, cell_line = None, chemical = None, concentration = None):
        """Updates grid based on existnce of well and passed args"""
        if self.grid[row][col]:
            if cell_line:
                self.grid[row][col].cell_line = cell_line
            if chemical:
                self.grid[row][col].chemical = chemical
            if concentration:
                if self.grid[row][col].chemical or chemical:
                    self.grid[row][col].concentration = concentration
                else:
                    return Well.invalid_concentration()
        # cannot create a well with concentration alone
        elif concentration and not chemical:
            return Well.invalid_concentration()   
        else:
            self.insert_well(row, col, cell_line, chemical, concentration)
    
    def as_dict(self):
        return {"id":self.id, 
                "name":self.name, 
                "size":self.size,
                }
    
    def __str__(self):
        return f"{self.id} \n{self.name} \n{self.size}"

@dataclass
class Well:
    """Class for keeping track of a well in an assay

        Attributes:
            row (int): An integer representing the well's row.
            col (int): An integer representing the well's column.
            cell_line (str): A string starting with 'c' and followed by numbers.
            chemical (str): A string starting with 'O' and followed by numbers.
            concentration (float): A floating point number.
    """

    def __init__(self, row, col, cell_line = None, chemical = None, concentration = None):
        self.row = row
        self.col = col
        self.cell_line = cell_line
        self.chemical = chemical
        self.concentration = concentration if chemical else None
    
    def invalid_concentration():
        resp = Response(status=404)
        resp.headers["Message"] = "You cannot add a concentration for a well without a chemical."
        return abort(resp)