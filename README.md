COMP249 Web Technology 2019: Javascript Web Application
===

This year's web application project is an online store.  In this assignment you will 
re-implement the core functionality using Javascript in the browser rather than 
Python on the server. 

You are provided with a web application that supports a JSON API. Using this you can fetch
JSON versions of the list of products and the shopping cart.  You can also send a
POST request to add items to the shopping cart. 

  * `/` - delivers the index.html template, you will use this template to write the HTML for your application, this is the only URL that web users would access directly.  In the starter kit, this contains links to some of the URLs below and a sample form for demo purposes; you do not need to retain any of these in your solution.
  * `/static/<path>` - delivers static files in the normal manner
  * `/products` - delivers a JSON representation of a list of products
  * `/cart` - accepts a POST request to add an item to the shopping cart with form fields:
      * productid - id of the product to be added
      * quantity - quantity to be added
      * update - if set (value=1), quantity of item is set to quantity, otherwise quantity is added to any existing quantity in the cart already. If quantity=0 and update=1, item is removed from the cart.
  * `/cart` returns a JSON representation of the shopping cart

Run the application in main.py in the usual way (first run `dbschema.py` to create the database).  
The default HTML page delivered links to the two
JSON URLs and provides an example form that can add to the cart.  

Note that this implementation relies on the `beaker` module to provide sessions, you'll need to install
`beaker` and `bottle-beaker` to run this code.  

Your task is to modify script.js and add other Javascript modules as needed to implement the solution.  You may modify
the `index.html` template as you wish but do not change any of the Python files.  