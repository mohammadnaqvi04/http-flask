# Plate Management API

This API allows scientists to manage experimental assay plates, including creating plates, updating wells, and retrieving plate information. It's built using Python and Flask and adheres to common standards for API development.

## Table of Contents

- [Plate Management API](#plate-management-api)
  - [Table of Contents](#table-of-contents)
    - [Project Overview](#project-overview)
    - [Features](#features)
    - [Running the Server](#running-the-server)
    - [Example cURL Commands](#example-curl-commands)
    - [Add a Well to a Plate:](#add-a-well-to-a-plate)
    - [Get Plate Information:](#get-plate-information)
    - [Authentication](#authentication)
    - [API Endpoints](#api-endpoints)
      - [Create a Plate](#create-a-plate)
    - [Error Handling](#error-handling)
      - [Example error response:](#example-error-response)
    - [Development](#development)
      - [Project Structure](#project-structure)
    - [Limitations](#limitations)

### Project Overview

The Plate Management API is designed to help scientists manage experimental assay plates, which are rectangular grids composed of wells. Each well contains specific reagents used in experiments. The API provides operations to create plates, update wells, and retrieve information about plates and their contents.

This project is part of a software engineering challenge to build a simple, useful API that interacts with biological experiment data using HTTP methods.

### Features

- Create a new assay plate (96 or 384 wells)
- Update the contents of wells (cell line, chemical, and concentration)
- Retrieve plate details, including its wells and their contents
- Error handling for invalid operations or inputs

### Running the Server
To start the API server, run the following command:
```bash
python server.py
```

The server will run at ```localhost:5000``` by default.

### Example cURL Commands
Create a Plate:
```bash
curl -X POST http://localhost:5000/plates \
  -H "Content-Type: application/json" \
  -d '{"name": "exp_1", "size": 96}'
```
### Add a Well to a Plate:
```bash
curl -X POST http://localhost:5000/plates/1/wells \
  -H "Content-Type: application/json" \
  -d '{
    "row": 1,
    "col": 1,
    "cell_line": "c47",
    "chemical": "O123",
    "concentration": 0.19
  }'
```
### Get Plate Information:
```bash
curl http://localhost:5000/plates/1
```
### Authentication
No authentication is required for this API.

### API Endpoints
#### Create a Plate

Endpoint: ```POST /plates```

Description: Creates a new assay plate.
Request Body:
json

{
  "name": "exp_1",
  "size": 96
}
name: Name of the plate (string)
size: Size of the plate (96 or 384 wells)
Response:
```json
{
  "id": 1,
  "name": "exp_1",
  "size": 96
}
```
Update a Well

Endpoint: ```POST /plates/{plate_id}/wells```

Description: Adds or updates information for a specific well in a plate.
Request Body:
```json
{
  "row": 1,
  "col": 1,
  "cell_line": "c47",
  "chemical": "O123",
  "concentration": 0.19
}
```
row: Row of the well (integer, 1-indexed)
col: Column of the well (integer, 1-indexed)
cell_line: (optional) Identifier for the cell line (string)
chemical: (optional) Identifier for the chemical (string)
concentration: (optional) Concentration of the chemical (float)
Response:
```json
{
  "message": "Well updated!"
}
```
Get Plate Information

Endpoint: ```GET /plates/{plate_id}```

Description: Retrieves information about a specific plate, including its wells.
Response:
```json
{
  "id": 1,
  "name": "exp_1",
  "size": 96,
  "plate": {
    "1, 1": {
      "cell_line": "c47",
      "chemical": "O123",
      "concentration": 0.19
    }
  }
}
```
### Error Handling
The API uses standard HTTP status codes to indicate the success or failure of requests:

```200 OK```: Operation was successful.
```404 Not Found```: The requested resource (plate, well) was not found.
```400 Bad Request```: Invalid input data or parameters.
#### Example error response:

```bash
HTTP/1.1 404 NOT FOUND
{
  "message": "That plate doesn't exist!"
}
```
### Development
#### Project Structure

```server.py```: Main Flask application
```classes.py```: Contains the Assay and Well classes
```README.md```: Project documentation (this file)
```Tutorial.md```: Additional usage examples and edge cases

For more detailed examples, refer to the [Tutorial](Tutorial.md).

### Limitations
* Plate sizes are restricted to 96 (12x8) or 384 (24x16) wells.
* Well positions are 1-indexed.
* A concentration can only be added if a chemical is present in the well.
* The API only accepts JSON input.


