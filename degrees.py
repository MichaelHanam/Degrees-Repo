import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    source_neighbors_paths = []
    source_neighbors = list(neighbors_for_person(source))
    item_index = -1
    for path in source_neighbors:
        source_neighbors_paths.append([(path)])
    return connection(source, target, source_neighbors_paths)
    for item in source_neighbors:
        
        # index which item number it is
        item_index += 1

        # returns target if they're one of the source's neighbors
        if target in item:
            print("Returned:", [item])
            return [item]

        # if the neighbor only has the same neighbors as source, erase them from the list
        if sorted(list(neighbors_for_person(item[1]))) == source_neighbors:
            source_neighbors.pop(item_index)
        
        # returns full path to target if they're a neighbor of one of the source's neighbors
        elif target in list(neighbors_for_person(item[1])):
            print("Returned:", list(item, (item[0], target)))
            return list(item, (item[0], target))

    
    
    final_connection = connection(source, target, source_neighbors_paths)
    return final_connection
    # TODO
    raise NotImplementedError


def connection(source, target, paths):


    """
    # important 
    + make sure there's something to follow all the steps to the target as they're checked.
    + add the if-return for when the target is found
    + jic return none after the for
    - make sure to not add paths that lead to a person that's already in any of the existing paths!
    """


    paths_checked = set()
    exists = False
    path_index = -1
    print("Paths:",paths)

    for path in paths:

        #print("Checking path:", path, "\nChecking person:", path[-1][1])

        if target in path:

            #print("Returned:", path)
            return path

        for movie_person_tuple in list(neighbors_for_person(path[-1][1])):

            if not movie_person_tuple[1] in paths and not movie_person_tuple[1] in path:

                paths.append([path,movie_person_tuple])
                #print("Added:",paths[-1])

            else:
                print(movie_person_tuple[1], "in", paths)

        paths.pop(0)

        print(path)

    # for path in paths:
    #     if target in list(neighbors_for_person(path[-1][1])):
    #         print("Returned:", path)
    #         return path
    #     else:
    #         path_index += 1
            
    #     for next_step in list(neighbors_for_person(path[-1][1])):
            
    #         for options in paths:
    #             if options != None:
    #                 print("Options:", options)
    #                 if next_step in options:
    #                     exists = True

    #         if not exists:
    #             print("Next Step:", next_step)
    #             option = path.append(next_step)

    #             paths.append(option)

    #         exists = False
    # while sorted(paths_checked) != set(sorted(neighbors_for_person(source))):
    #     for path in paths:
    #         #print(path[-1][1])
    #         #print("Paths checked:", paths_checked) # Debug
    #         #print("Paths:", paths) # Debug
    #         path_index += 1

    #         for next_step in list(neighbors_for_person(path[-1][1])):
    #             if not next_step in paths_checked:
    #                 #print(next_step, "Not Checked")
    #                 path += tuple(next_step)
    #                 #print("Added:", next_step)
    #                 paths_checked.add(next_step)
    #         if target in path:
    #             #print("Returned:", path)
    #             return path
        


    print("Returned: None")
    return None
    
    # for path in current_paths:
    #     print("Looking at", path)
    #     path_index += 1

    #     for next_step in list(neighbors_for_person(path[-1][1])):
    #         for path_check in current_paths:
    #             if next_step in path_check:
    #                 exists = True

    #         if not exists:
    #             current_paths[path_index].append(next_step)
    #             print("Added", next_step, "To", current_paths[path_index])
    #         exists = False


    # for target_check in current_paths:
    #     if target in target_check:
    #         print("Returned",target_check)
    #         return list(target_check)
        #[[(1,100),(2,200)],[(1,100),(3,300)]]
        
    # for neighbor, options in current_paths.items():
    #     for item in options:
    #         for next_option in list(neighbors_for_person(item[1])):
    #             if not next_option in current_paths:
    #                 for steps in source_neighbors.values():
    #                     if next_option in steps:
    #                         exists = True
    #             if not exists:
    #                 options.append(next_option)
    #             exists = False
    #         source_neighbors[neighbor] = options
    


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
