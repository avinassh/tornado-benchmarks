# Tornado Benchmarks

This is a simple app, like a blog, displays blog post retrieving from database. I used MongoDB as data store and Tornado for routing and templating. Tornado is running behind an nginx proxy.

This is how it looks once loaded: http://i.imgur.com/y3XiAMr.png

There are 3 apps (or Tornado servers). They are:

1. Uses `pymongo` and fetches data synchronously 
2. Uses `motor` and fetches data asynchronously
3. Combination of `tornado-redis` + `motor`

Then I used `siege` tool to benchmark:

    siege http://app.iavin.com/5427f88aa76036081aa5edbe -c10 -t10s

Here are the results of each:

1. 


		Transactions:		          68 hits
		Availability:		      100.00 %
		Elapsed time:		        9.14 secs
		Data transferred:	        0.05 MB
		Response time:		        0.75 secs
		Transaction rate:	        7.44 trans/sec
		Throughput:		        0.01 MB/sec
		Concurrency:		        5.55
		Successful transactions:          68
		Failed transactions:	           0
		Longest transaction:	        1.53
		Shortest transaction:	        0.64

2.

		Transactions:		          68 hits
		Availability:		      100.00 %
		Elapsed time:		        9.47 secs
		Data transferred:	        0.05 MB
		Response time:		        0.74 secs
		Transaction rate:	        7.18 trans/sec
		Throughput:		        0.00 MB/sec
		Concurrency:		        5.32
		Successful transactions:          68
		Failed transactions:	           0
		Longest transaction:	        1.25
		Shortest transaction:	        0.65

3.

		Transactions:		          78 hits
		Availability:		      100.00 %
		Elapsed time:		        9.93 secs
		Data transferred:	        0.05 MB
		Response time:		        0.66 secs
		Transaction rate:	        7.85 trans/sec
		Throughput:		        0.01 MB/sec
		Concurrency:		        5.20
		Successful transactions:          78
		Failed transactions:	           0
		Longest transaction:	        0.80
		Shortest transaction:	        0.61