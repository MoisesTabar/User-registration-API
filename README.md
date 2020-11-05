<h5>User registration API</h5>

<p>This API allows users to register and login. when logged in users can update its credentials and password passing a token</p>
<p>Also users can register secrets using their respective tokens</p>

<h4><b>Available scripts</b></h4>
<hr>
<p>To use this API you must have uvicorn installed for running the server. Use:</p>
<code>pip install uvicorn</code>
<p>After that run the server by using:</p>
<h5><b>In windows</b></h5>
<code>py uvicorn main:app --reload</code>
<h5><b>In Linux</b></h5>
<code>python3 -m uvicorn main:app --reload</code>
