import urllib2
import re
import collections
import multiprocessing
import Queue
from threading import Thread

API_KEY = '1b4218629b50c1159e15a6b8285b90ba'
ROOT_USER = "rj"
BASE_LIMIT = 500
NUM_PROCESSES = 5
NUM_LEVELS = 3
NUM_THREADS = 1000


def fetch_vertex(user, limit, page):
    command = "http://ws.audioscrobbler.com/2.0/?method=user.getfriends"\
              + "&user=" + user\
              + "&limit=" + str(limit)\
              + "&page=" + str(page)\
              + "&api_key=" +API_KEY
    data = urllib2.urlopen(command).read() # XML format
    degree = int(re.search('total="(\d+)"', data).group(1)) # first 10 friends (because page=1 and limit=10).
    friends = re.findall("<name>(.*)</name>", data) # number of friends of "rj"
    totalpages = int(re.search('totalPages="(\d+)"', data).group(1))


    if (totalpages - page != 0):
        friends += fetch_vertex(user, limit, page + 1)[1] # 2nd element of tuple is list of friends

    return (degree, friends)


def worker_function(nodes_to_visit, degree_queue, friends_queue, visited_list):
    while len(nodes_to_visit) != 0:
            node = nodes_to_visit.popleft()

            if (node not in visited_list):
                degree, friends = fetch_vertex(node, BASE_LIMIT, 1)
                degree_queue.append(degree)
            
                print "Visited " + str(node) + " " + str(degree)
                friends_queue.extend(friends)


if __name__ == '__main__':
      bfs_queue = collections.deque([ROOT_USER])
      level_count = 0
      visited = collections.deque()

      while (len(bfs_queue) != 0 and level_count < NUM_LEVELS):
          level_count += 1 
          degree_queue = collections.deque()
          friends_queue = collections.deque()
          threads = [Thread(target=worker_function, args=(bfs_queue, degree_queue, friends_queue, visited)) for i in xrange(NUM_THREADS)]

          for t in threads:
              t.start()
          for t in threads:
              t.join()

          visited = collections.deque()

          bfs_queue = friends_queue
          print "LEVEL %s done" %(level_count)
