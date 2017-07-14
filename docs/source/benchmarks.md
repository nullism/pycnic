[[
title: Benchmarks
]]

# Pycnic Bench (heh)

Pycnic benchmarks were ran with two [Gunicorn](http://gunicorn.org) workers
and hit with `ab -n 5000 -c 5` against a JSON endpoint (/json). 

*Note: the express.js benchmark can be located at [[nodejs-compare]].*

* <a href="https://github.com/nullism/pycnic/tree/master/benchmark">Source code <span class="fontawesome-github"></span></a>


{tpl:thumb}
image: http://pycnic.nullism.com/images/pycnic-bench.png
max_width: 736px
{endtpl}
