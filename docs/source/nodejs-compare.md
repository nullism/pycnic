[[
title: Node.js Comparison
]]

[TOC]

# Async NodeJS compared to Pycnic

The purpose of these benchmarks was to test the claim 
that node.js's non-blocking nature is faster than other
production webservers. The most popular web framework for Node.js
is Express.js, by at least one order of magnitude (github stars). 

While Pycnic is definitely not the most popular Python framework,
this is still the Pycnic documentation. 


## Methods

Both tests were deployed in a production-ready fashion. Though there 
may be optimizations to both (using Nginx over Gunicorn, or PM2 instead of `node`) the 
goal was to reasonably simulate a small-scale deployment. 

1. Both tests were ran with `ab -c 5000 -n 5 127.0.0.1:<port>/`
2. Both tests read a .json file and returned its contents. 
3. The Express.js test uses asynchronous code and is served by `node`.
4. The Pycnic test uses synchronous code, and is served by `gunicorn -w 2`.

## Express.js Source

    :::javascript
    var express = require("express")
    var fs = require("fs")
    
    var app = express()
    
    function getFileData() {
      let p = new Promise(
        function(resolve, reject) {
          fs.readFile('/home/nullism/foo.json', 'utf8', function(err, data) {
            resolve(data)
          })
        }
      )
      return p
    }
    
    app.get("/", function(req, res) {
      getFileData().then(
        function(val) {
          res.end(val)
        }
      )
    })

    app.listen(3000, function() {
      console.log("Listening on port 3000")
    })


## Pycnic Source

    :::python
    from pycnic.core import WSGI, Handler
    
    def get_file_data():
    
        with open("/home/nullism/foo.json") as fh:
            return fh.read()
    
    class Root(Handler):
    
        def get(self):
            return get_file_data()
    
    class app(WSGI):
        routes = [("/", Root())]


## Results

### Express.js

    :::text
    This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 500 requests
    Completed 1000 requests
    Completed 1500 requests
    Completed 2000 requests
    Completed 2500 requests
    Completed 3000 requests
    Completed 3500 requests
    Completed 4000 requests
    Completed 4500 requests
    Completed 5000 requests
    Finished 5000 requests


    Server Software:
    Server Hostname:        127.0.0.1
    Server Port:            3000

    Document Path:          /
    Document Length:        61 bytes

    Concurrency Level:      5
    Time taken for tests:   2.278 seconds
    Complete requests:      5000
    Failed requests:        0
    Total transferred:      795000 bytes
    HTML transferred:       305000 bytes
    Requests per second:    2195.30 [#/sec] (mean)
    Time per request:       2.278 [ms] (mean)
    Time per request:       0.456 [ms] (mean, across all concurrent requests)
    Transfer rate:          340.87 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.1      0       2
    Processing:     1    2  11.3      2     358
    Waiting:        0    2  11.3      2     358
    Total:          1    2  11.3      2     358

    Percentage of the requests served within a certain time (ms)
      50%      2
      66%      2
      75%      2
      80%      2
      90%      2
      95%      2
      98%      3
      99%      4
     100%    358 (longest request)


### Pycnic


    :::text
    This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 500 requests
    Completed 1000 requests
    Completed 1500 requests
    Completed 2000 requests
    Completed 2500 requests
    Completed 3000 requests
    Completed 3500 requests
    Completed 4000 requests
    Completed 4500 requests
    Completed 5000 requests
    Finished 5000 requests


    Server Software:        gunicorn/19.6.0
    Server Hostname:        127.0.0.1
    Server Port:            8000

    Document Path:          /
    Document Length:        61 bytes

    Concurrency Level:      5
    Time taken for tests:   1.588 seconds
    Complete requests:      5000
    Failed requests:        0
    Total transferred:      965000 bytes
    HTML transferred:       305000 bytes
    Requests per second:    3148.74 [#/sec] (mean)
    Time per request:       1.588 [ms] (mean)
    Time per request:       0.318 [ms] (mean, across all concurrent requests)
    Transfer rate:          593.46 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     0    2   0.3      1      11
    Waiting:        0    1   0.2      1      11
    Total:          1    2   0.3      1      11
    ERROR: The median and mean for the processing time are more than twice the standard
           deviation apart. These results are NOT reliable.
    ERROR: The median and mean for the total time are more than twice the standard
           deviation apart. These results are NOT reliable.

    Percentage of the requests served within a certain time (ms)
      50%      1
      66%      2
      75%      2
      80%      2
      90%      2
      95%      2
      98%      2
      99%      2
     100%     11 (longest request)




## Conclusion

Though Express.js may outperform Pycnic in a single-worker scenario, 
this is not the case when using a production Python webserver (gunicorn with two workers in this case).

Multi-worker Pycnic outperforms Express.js, and it may be difficult to justify the additional verbosity
of Node.js server-side programming.


    :::text
    # Express.js
    Requests per second:    2195.30 [#/sec] (mean)
    Time per request:       2.278 [ms] (mean)
    Time per request:       0.456 [ms] (mean, across all concurrent requests)
    Transfer rate:          340.87 [Kbytes/sec] received
     
    # Pycnic
    Requests per second:    3148.74 [#/sec] (mean)
    Time per request:       1.588 [ms] (mean)
    Time per request:       0.318 [ms] (mean, across all concurrent requests)
    Transfer rate:          593.46 [Kbytes/sec] received

## Questions or Comments?

Feel free to open an issue on the Pycnic [Github page](https://github.com/nullism/pycnic/issues).
