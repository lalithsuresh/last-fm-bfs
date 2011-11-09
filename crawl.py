import urllib2
import re
import collections

API_KEY = '1b4218629b50c1159e15a6b8285b90ba'
ROOT_USER = "lalithsuresh"
BASE_LIMIT = 500

visited = []


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
        print totalpages

    return (degree, friends)


bfs_queue = collections.deque()
bfs_queue.extend([ROOT_USER]) # Start with root user
count = 0

while (len(bfs_queue) != 0):
  count += 1
  node_to_visit = bfs_queue.popleft()
  degree, friends = fetch_vertex(node_to_visit, BASE_LIMIT, 1)
  print count, node_to_visit, degree
  bfs_queue.extend(friends)
