from room import Room
from player import Player
from world import World
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()

# set player's current room as the starting point
# run DFS - mark every visited room unless a room has no unexplored paths
# when reach dead end, get back to nearest room w/ unexplored paths and update path
# if room is not in the map, find exits
# update map
# add unexplored rooms to list
# run BFS to find shortest path
# search for an exit == "?"
# if exit is found, put in BFS queue
# BFS will return the path as a list of ids
# convert ids to list of n, e, s, w before adding to path
# keep looping until graph has all entries and no ? in dict.


def reverse_direction(d):
    if d is 'n':
        return 's'
    elif d is 's':
        return 'n'
    elif d is 'e':
        return 'w'
    elif d is 'w':
        return 'e'


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# keep track of movement in the exploration map
exploration_map = {}

# find potential exits
potential_exits = player.current_room.get_exits()
exploration_map[player.current_room.id] = {i: "?" for i in potential_exits}

# unexplored room tracker
unexplored_rooms = []

for room_choice in player.current_room.get_exits():
    # add unexplored rooms
    unexplored_rooms.append({(player.current_room.id, room_choice)})

while unexplored_rooms:
    # run DFS until room has no unexplored choices
    if "?" in exploration_map[player.current_room.id].values():

        next_move = None
        starting_room = player.current_room.id

        # find an uneplored exit and move towards it
        if 'n' in exploration_map[starting_room] and exploration_map[starting_room]['n'] == "?":
            next_move = 'n'
        elif 's' in exploration_map[starting_room] and exploration_map[starting_room]['s'] == "?":
            next_move = 's'
        elif 'w' in exploration_map[starting_room] and exploration_map[starting_room]['w'] == "?":
            next_move = 'w'
        elif 'e' in exploration_map[starting_room] and exploration_map[starting_room]['e'] == "?":
            next_move = 'e'

        # remove the next room from unexplored roos
        unexplored_rooms.remove({(player.current_room.id, next_move)})
        print(unexplored_rooms)

        # move to next room
        player.travel(next_move)

        # add more to traversed array
        new_room = player.current_room.id
        traversal_path.append(next_move)

        # if new room is not is not in the exploration map, find potential exits
        if new_room not in exploration_map:
            exploration_map[new_room] = {
                i: "?" for i in player.current_room.get_exits()}

        # update exploration map
        exploration_map[starting_room][next_move] = new_room
        exploration_map[new_room][reverse_direction(next_move)] = starting_room

        # add all unexplored rooms to list
        for available_exit, room_id in exploration_map[new_room].items():
            if room_id == '?':
                unexplored_rooms.append({(new_room, available_exit)})

        # if exploration_map has 500 entries and there are no '?' left then break loop
        if len(list(exploration_map)) == 500 and '?' not in exploration_map[player.current_room.id].values():
            break
    else:
        # if all unexplored exits have discovered
        # execute bfs to find shortest path

        starting_room = player.current_room.id
        q = Queue()

        for available_exit, room_id in exploration_map[starting_room].items():
            # enqueue a path to the avail exits and rooms leading there
            q. enqueue([[available_exit, room_id]])

        # while the queue is not empty
        while q.size() > 0:
            # dequeue the first path
            path = q.dequeue()
            # get room from path
            room = path[-1]
            # if all exits have been explored in the room we move back
            if '?' not in [room_id for available_exit, room_id in exploration_map[room[1]].items()]:
                for available_exit, room_id in exploration_map[room[1]].items():
                    # if exit doesn't go to the path or current room
                    if room_id is not starting_room and room_id not in [room_id for available_exit, room_id in path]:
                        new_path = list(path)
                        new_path.append([available_exit, room_id])
                        q.enqueue(new_path)
            else:
                for available_exit, room_id in path:
                    player.travel(available_exit)
                    traversal_path.append(available_exit)
                break

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
