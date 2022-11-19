## API Spec & Example Usage


`/plates/`

### Creates plates with given name and size

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/ -d '{"name":"exp_1", "size":96}'
</pre>

`/plates/<id>/wells/`

### Inserts well information to specified plate

### 
Adding well to row 5, column 3 in plate 1 (exp_1)

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":5, "col":3, "cell_line":4, "chemical":"Ascorbic acid", "concentration":0.83}'
</pre>

Adding well to row 1, column 1 in plate 1 (exp_1)

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":1, "col":1, "cell_line":47, "chemical":"Arabinose", "concentration":0.19}'
</pre>

Adding well to row 12, column 8 in plate 1 (exp_1)

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":12, "col":8, "cell_line":18, "chemical":"Phenol", "concentration":0.24}'
</pre>

`/plates/id`

### Checking contents of plate 1 (exp_1)

<pre>
curl -i http://127.0.0.1:5000/plates/1
</pre>


## Edge Cases

Specified: cell_line

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":1, "cell_line":18}'
</pre>

Specified: chemical

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":2, "chemical":"Glucose"}'
</pre>

Specified: concentration

<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":6, "concentration":0.83}'
</pre>

Specified: cell_line, chemical


<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":3, "cell_line":47, "chemical":"PMSF"}'
</pre>

Specified: chemical, concentration


<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":4, "chemical":"DMF", "concentration":0.83}'
</pre>

Specified: cell_line, concentration


<pre>
curl -i -H "Content-type: application/json" \
-X POST http://127.0.0.1:5000/plates/1/wells/ -d '{"row":7, "col":5, "cell_line":47, "concentration":0.83}'
</pre>