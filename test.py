# paths = [[(1000,1),(2000,2),(3000,3)],[(1100,12),(2200,23),(3300,34)]]
# paths 
# source = 100
# def neighbors_for_person(person):
#     return [(person*10,1),(person*11,2),(person*12,3),(person*13,4)]
# while paths_checked != neighbors_for_person(source):
#     for path in paths:
#         print(path[-1][1])
#         #print("Paths checked:", paths_checked) # Debug
#         #print("Paths:", paths) # Debug
#         path_index += 1

#         for next_step in list(neighbors_for_person(path[-1][1])):
#             if not next_step in paths_checked:
#                 #print(next_step, "Not Checked")
#                 path += tuple(next_step)
#                 paths_checked.add(next_step)
#         if target in path:
#             print("Returned:", path)
#             return path

Kevin Bacon
Gary Sinise

i = [[(100, 200)]]
for j in i:
    if (100, 200) in j:
        print(j)    