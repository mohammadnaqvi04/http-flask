### Here are some tips with getting the server up and running
 Some things you'll need:
 1. A recent version of cURL
 2. A Python 3 installation

Flask and its libraries can be loaded via pip.

### Here's a sequence of steps demonstrating the server's functionality:

1. Once you run server.py with your port of choice, run the following cURL command in your terminal. This creates a 96-well plate called "exp_1".
<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/ -d '{"name":"exp_1", "size":96}'
</pre>

This'll give you the following response:

<pre>
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: application/json
Content-Length: 36
Message: Plate created!

{"id": 1, "name": "exp_1", "size": 96}
</pre>
Now that we have a plate, we can add some data into it

2. Add some information to a well in the plate
<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":1, "col":1, "cell_line":47, "chemical":"Arabinose", "concentration":0.19}'
</pre>

The response will tell you whether the well was successfully created.

<pre>
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: application/json
Message: Well updated!
Content-Length: 0
</pre>

3. Let's add another well into our plate
<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":5, "col":3, "cell_line":4, "chemical":"Ascorbic acid", "concentration":0.83}'
</pre>

4. Now, we'll visualize what we have so far

<pre>
curl -i http://127.0.0.1:5000/plates/1
</pre>

This returns the following:

<pre>
{
  "id": 1,
  "name": "exp_1",
  "plate": {
    "1, 1": {
      "cell_line": 47,
      "chemical": "Arabinose",
      "concentration": 0.19
    },
    "5, 3": {
      "cell_line": 4,
      "chemical": "Ascorbic acid",
      "concentration": 0.83
    }
  },
  "size": 96
}
</pre>

The plate-JSON displays wells in the following format:

<pre>
  "plate": {
    "row, col": {
      "cell_line": int,
      "chemical": str,
      "concentration": float
    }
  }
</pre>

### Some additional notes:

*Response bodies summarized for brevity.

- All endpoints only support json input. If you try to pass anything else, like plain text, you'll get the following error

<pre>
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: text/html; charset=utf-8
Message: Data type not supported!
</pre>
- Requests to the endpoints containing row or column numbers should be 1-indexed. Here's the response when you try to access a nonexistent index.

<pre>
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: text/html; charset=utf-8
Message: You are attempting to access a row or column out of the assay's scope.
</pre>

- Attempting to create an assay that doesn't have either 96 or 384 wells triggers this response

<pre>
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: text/html; charset=utf-8
Message: Assay can only have either 96 or 384 wells.
</pre>

- Here's the message when you attempt to create a new well with only concentration specified or attempt to give a well a concentration without a chemical present

<pre>
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: text/html; charset=utf-8
Message: You cannot add a concentration for a well without a chemical.
</pre>

- If you try to work with data on a plate that doesn't exist, you'll get the following error

<pre>
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/2.2.2 Python/3.8.6
Content-Type: text/html; charset=utf-8
Message: That plate doesn't exist!
</pre>