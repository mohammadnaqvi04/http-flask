from flask import Flask, request, json, Response
from classes import Assay
app = Flask(__name__)

in_memory_datastore = {}

@app.route('/')
def api_root():
    return 'Hello! Please create an API request using cURL to get started.'

@app.route('/plates/', methods = ['POST'])
def api_create_plate():
    #determining request input type
    if request.headers['Content-Type'] == 'application/json':
        name = request.json["name"]
        size = request.json["size"]
        #create assay once inputs are parsed
        def create_assay(name, size):
            assay = Assay(name, size, Assay.uniqueID)
            in_memory_datastore[Assay.uniqueID] = assay
            #updating uniqueID for the next assay
            Assay.uniqueID += 1

        create_assay(name, size)
        js = json.dumps(in_memory_datastore[Assay.uniqueID - 1].as_dict())
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers["Message"] = "Plate created!"
        return resp
    else:
        resp = Response(status=404)
        resp.headers["Message"] = "Data type not supported!"
        return resp

@app.route('/plates/<int:id>/wells/', methods  = ['POST'])
def api_update_well(id):
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if id in in_memory_datastore:
            # check for valid inputs
            insert_row = data.get("row") - 1
            insert_col = data.get("col") - 1
            insert_cell_line = data.get("cell_line", None)
            insert_chemical = data.get("chemical", None)
            insert_concentration = data.get("concentration", None)

            # check against input conditions to prevent overwriting
            if insert_cell_line and insert_chemical and insert_concentration:
                in_memory_datastore[id].insert_well(insert_row, insert_col, insert_cell_line, insert_chemical, insert_concentration)
            elif insert_cell_line and insert_chemical:
                in_memory_datastore[id].update_grid(insert_row, insert_col, cell_line = insert_cell_line, chemical = insert_chemical)
            elif insert_chemical and insert_concentration:
                in_memory_datastore[id].update_grid(insert_row, insert_col, chemical = insert_chemical, concentration = insert_concentration)
            elif insert_cell_line:
                in_memory_datastore[id].update_grid(insert_row, insert_col, cell_line = insert_cell_line)
            elif insert_chemical:
                in_memory_datastore[id].update_grid(insert_row, insert_col, chemical = insert_chemical)
            elif insert_concentration:
                in_memory_datastore[id].update_grid(insert_row, insert_col, concentration = insert_concentration)

            resp = Response(status=200, mimetype='application/json')
            resp.headers["Message"] = "Well updated!"
            return resp
            
        else:
            resp = Response(status=404)
            resp.headers["Message"] = "That plate doesn't exist!"
            return resp
    else:
        resp = Response(status=404)
        resp.headers["Message"] = "Data type not supported!"
        return resp

@app.route('/plates/<int:id>', methods = ['GET'])
def api_lookup_assay(id):
    # check for assay id and return as json if it exists
    if id in in_memory_datastore:
        js = json.dumps(in_memory_datastore[id].as_json())
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers["Message"] = "Here is your plate!"
        return resp
    else:
        resp = Response(status=404)
        resp.headers["Message"] = "That plate doesn't exist!"
        return resp


if __name__ == '__main__':
    app.run()