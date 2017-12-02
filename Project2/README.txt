Jessie Adkins
jsa70@case.edu
EECS 325 Project 2

This is my report for the assignment.

First of all, there are no special instructions on how to run my program. Just use the command stated in the assignment and it will all work out fine.

Second of all, there is a .png saved in this folder that contains the plot of data requested. My observation is that with the sites I visited, there was little to no correlation between the TTL and the number of hops. Perhaps I should have chosen some internationally hosted sites for a better set of data.

Reasons a host might not respond:
- There might be some kind of anti-DDOS protocol that handles non-standard packets in an unexpected way
- There might be physical interference with the wire
- The request might get bounced around internally in a series of routers at the company that owns the site, and my program would timeout before the error message got back to me
- The servers might be configured to never send anyone back error messages like that

Matching ICMP responses:
- you could send every packet out to a different port and then determine what packets you got back by checking its port number
- you could do a DNS lookup of the IP address returned to figure out which website it correlates to and compare that to the list of strings from your text file