import urllib2
import re
import collections
import sys,os,signal
from threading import Thread

API_KEY = '1b4218629b50c1159e15a6b8285b90ba'
ROOT_USER = "RJ"
BASE_LIMIT = 500
NUM_PROCESSES = 5
NUM_LEVELS = 10
NUM_THREADS = 100

def fetch_vertex(user, limit, page):
    #Consider a space in the user name
    temp_user="%20".join(user.split(' ')) 
    command = "http://ws.audioscrobbler.com/2.0/?method=user.getfriends"\
              + "&user=" + temp_user\
              + "&limit=" + str(limit)\
              + "&page=" + str(page)\
              + "&api_key=" +API_KEY
    try:
        data = urllib2.urlopen(command).read() # XML format
        degree = int(re.search('total="(\d+)"', data).group(1)) # first 10 friends (because page=1 and limit=10).
        friends = re.findall("<name>(.*)</name>", data) # number of friends of "rj"
        totalpages = int(re.search('totalPages="(\d+)"', data).group(1))


        if (totalpages - page != 0):
            friends += fetch_vertex(user, limit, page + 1)[1] # 2nd element of tuple is list of friends

        return (degree, friends)
    except:
        print
        print "URL Fetch failed for node: '" + user + "' with error: ", sys.exc_info()[0]
        print "Executed command: " + command
        print
        return (None, None)


def sigterm_handler(signum, frame):
    print "\nSIGINT handler.  Shutting Down."
    global SIGINT_SENT
    os.kill(os.getpid(), signal.SIGINT)
    sys.exit()

def worker_function(nodes_to_visit, degree_queue, friends_queue, visited_list):
    while len(nodes_to_visit) != 0:
        node = nodes_to_visit.popleft()

        if (node not in visited_list):
            degree, friends = fetch_vertex(node, BASE_LIMIT, 1)

            if (degree != None and friends != None):
                # print "Visited " + str(node) + " " + str(degree)
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
              args=(bfs_queue, degree_queue, friends_queue, visited))\
              for i in xrange(NUM_THREADS)]

        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
        

        visited = visited.union(set(tmp))
        bfs_queue = friends_queue
        #Some estimators, will change in the future
        sum = reduce(lambda x, y: x + y, degree_queue)
        avg = float(sum) / len(degree_queue)
        print "LEVEL %s done, %s nodes with avg dregree %s would have been sampled after level %s"\
              % (level_count,sum, avg,  level_count + 1)
