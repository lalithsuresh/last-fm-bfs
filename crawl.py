import urllib2
import re
import collections
import sys,os,signal
import datamanip as dm
from threading import Thread

API_KEY = '1b4218629b50c1159e15a6b8285b90ba'
ROOT_USER = "RJ"
BASE_LIMIT = 1000
NUM_LEVELS = 4
NUM_THREADS = 200
MAX_FRIENDS_ALLOWED = 10000

def sigterm_handler(signum, frame):
    print "\nSIGINT handler.  Shutting Down."
    global SIGINT_SENT
    os.kill(os.getpid(), signal.SIGINT)
    sys.exit()


def fetch_vertex(user, limit, page, level_count):
    #Consider a space in the user name
    temp_user="%20".join(user.split(' ')) 
    command = "http://ws.audioscrobbler.com/2.0/?method=user.getfriends"\
              + "&user=" + temp_user\
              + "&limit=" + str(limit)\
              + "&page=" + str(page)\
              + "&api_key=" +API_KEY
    try:
        # XML format
        data = urllib2.urlopen(command).read() 
        # First 10 friends (because page=1 and limit=10).
        degree = int(re.search('total="(\d+)"', data).group(1)) 
        totalpages = int(re.search('totalPages="(\d+)"', data).group(1))
        friends = []

        # Some corner cases
        if (degree > MAX_FRIENDS_ALLOWED or totalpages == 0):
            return (None,None)

        if (level_count != NUM_LEVELS):
            # number of friends of "rj"
            friends = re.findall("<name>(.*)</name>", data) 
            if (totalpages - page != 0):
                print user, page,"of",totalpages

                # 2nd element of tuple is list of friends
                friends += fetch_vertex(user, limit, page + 1, level_count)[1] 

        return (degree, friends)
    except:
        print
        print "URL Fetch failed for node: '" + user + "' with error: ", sys.exc_info()[0]
        print "Executed command: " + command
        print
        return (None, None)

def worker_function(nodes_to_visit, degree_queue, friends_queue, visited_list, level_count):
    while len(nodes_to_visit) != 0:
        #print len(nodes_to_visit)
        node = nodes_to_visit.popleft()

        if (node not in visited_list):
            degree, friends = fetch_vertex(node, BASE_LIMIT, 1, level_count)

            if (degree != None and friends != None):
                #print "Visited " + str(node) + " " + str(degree)
                degree_queue.append(degree)        
                friends_queue.extend(friends)

if __name__ == '__main__':
    bfs_queue = collections.deque([ROOT_USER])
    level_count = 0
    visited = set()
    signal.signal(signal.SIGINT, sigterm_handler)
    
    while (len(bfs_queue) != 0 and level_count < NUM_LEVELS):
        level_count += 1 
        degree_queue = collections.deque()
        friends_queue = collections.deque()

        tmp = list(bfs_queue)[0:]
        #print tmp, bfs_queue, visited
        threads = [Thread(target=worker_function, \
              args=(bfs_queue, degree_queue, friends_queue, visited, level_count))\
              for i in xrange(NUM_THREADS)]

        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

        visited = visited.union(set(tmp))
        bfs_queue = friends_queue
        
        sum = reduce(lambda x, y: x + y, degree_queue)
        avg = float(sum) / len(degree_queue)
        print "LEVEL %s done with avg degree is %s, %s nodes would have been sampled after level %s"\
              % (level_count, avg,sum,  level_count + 1)
    dm.savetofile(list(degree_queue))
    dm.prepare_data(list(degree_queue))
