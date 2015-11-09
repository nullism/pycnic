# Framework Benchmarks

The benchmarks perform the following framework-specific tasks.

1. Route '/json' to a method.
2. Encode the '/json' result as JSON.
3. Return JSON in the response body with "Content-Type: application/json". 

## Requirements

1. The app MUST work under Python3.


## Methods

All WSGI frameworks are hosted with Gunicorn (single worker). 

    gunicorn <framework>_test:app

The actual testing is performed with `ab`. 

    ab -n 5000 -c 5 http://localhost:8000/json

### Exceptions

* **tornado** was hosted using the built-in IOLoop.
* **muffin** was hosted with `muffin muffin_test run` due to various errors attempting to get it working with Gunicorn.
* **bobo** was hosted with the built-in `bobo -f bobo_test.py -p 8000` due to the lack of documentation. It may perform better
    using Gunicorn.
* **morepath** was disqualified for numerous errors and complexity issues. Interestingly enough, it installs through pip but does not uninstall.
* **hug** was ran using the `hug` script provided by the package.

## Results

[Chart](http://pycnic.nullism.com/images/pycnic-bench.png)

* **falcon (cython)** - 2357.61/sec, 2.121s
* **pycnic** - 2130.55/sec, 2.379s
* **bottle** - 2130.21/sec, 2.386s
* **pyramid** - 1773.52/sec, 2.819s
* **bobo** - 1555.34/sec, 3.215s 
* **hug** - 1550.79/sec, 3.224s
* **flask** - 1414.67/sec, 5.531s
* **tornado** - 1341.86/sec, 3.762s
* **muffin** - 1080.41/sec, 4.628s
* **cherrypy** - 994.73/sec, 5.026s


