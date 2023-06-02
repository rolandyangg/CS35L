"""
Roland Yang 506053914

I used strace to help me verify that there were no uses of git
by using
strace -e trace=execve -o topo-test.tr pytest
trace=execve tracks the execve call which calls other programs
since it only returned pytest then it means it called no others
besides pytest. therefore it satisfies the requirements
"""
import os
import sys
import zlib


class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


def get_git_repo():
    curr_directory = os.getcwd()
    while True:  # Mimic a "do while" loop
        if os.path.isdir(curr_directory + "/.git"):
            curr_directory = curr_directory + "/.git"
            break
        if curr_directory == "/":
            break
        curr_directory = os.path.dirname(curr_directory)
    if curr_directory[-5:] != "/.git":
        sys.stderr.write('Not inside a Git repository')
        exit(1)

    # print("Git directory found!: " + curr_directory)
    return curr_directory


def parse_object(repo_path, commit_hash):
    object_path = repo_path + "/objects/"
    object_path += commit_hash[:2] + "/" + commit_hash[2:]

    # 'rb' = read binary
    with open(object_path, 'rb') as f:
        compressed_data = f.read()

    decompressed_data = zlib.decompress(compressed_data)
    object_content = decompressed_data.decode('utf-8')

    return object_content


def get_parents(object_content):
    parents = []
    lines = object_content.split("\n")
    # print("LINES", parents)
    for line in lines:
        if line[:6] == "parent":
            words = line.split()
            parents.append(words[1].rstrip("\n"))
    return parents

#########################################################################


def topo_order_commits():
    # Find git repository
    repo_path = get_git_repo()
    # Represent the graph
    root_commits = []  # Contains all the leaf nodes [CommitNode]
    hash_to_branch = dict()  # [commit_hash : [branch_name1, ...]]
    graph = dict()  # Contins all nodes [commit_hash : CommitNode]

    #########################################################################

    # BFS to get branch heads
    heads_path = repo_path + "/refs/heads"

    queue = []
    queue.append('')  # Begin with no branch
    root_commit_hashes = []

    while queue:
        popped = queue.pop(0)
        branches_path = heads_path + "/" + popped  # .git/refs/heads/ + .../...

        for file in os.listdir(branches_path):
            file_path = branches_path + file  # .git/refs/heads/.../ + file

            # Traverse deeper into branches if they're folders
            if os.path.isdir(file_path):
                queue.append(file + "/")  # ex. dev + /
                continue

            head_file = open(file_path)
            commit_hash = head_file.read().rstrip("\n")
            head_file.close()

            root_commit_hashes.append(commit_hash)
            node = CommitNode(commit_hash)
            graph[commit_hash] = node  # Starter nodes
            root_commits.append(node)  # root_commits[file] = node

            if commit_hash not in hash_to_branch.keys():
                hash_to_branch[commit_hash] = [popped + file]  # ex.'dev/'+'a'
            else:
                hash_to_branch[commit_hash].append(popped + file)
    #########################################################################

    # Build out the branches using iterative dfs
    stack = root_commit_hashes[:]  # Make a shallow copy of root_commit_hashes
    while stack:
        child_hash = stack.pop()
        parents = get_parents(parse_object(repo_path, child_hash))
        for parent_hash in parents:
            # So the vertex will always exist in the graph & no check needed
            if parent_hash not in graph:
                graph[parent_hash] = CommitNode(parent_hash)

            # Check to see if the edge already exists to avoid repeats
            if graph[child_hash] not in graph[parent_hash].children:
                # Add the edge in the graph
                graph[child_hash].parents.add(graph[parent_hash])
                graph[parent_hash].children.add(graph[child_hash])
                stack.append(parent_hash)
    #########################################################################

    # Generate a topological ordering via Kahn's algorithm
    # Calculate indegree for every node
    indegree = dict()
    for commit_hash, node in graph.items():
        indegree[commit_hash] = len(node.children)
    queue = []
    topological_ordering = []

    # Pick all vertices with indegree 0 and enqueue
    for commit_hash, degree in indegree.items():
        if degree == 0:
            queue.append(commit_hash)

    while queue:
        commit_hash = queue.pop(0)
        topological_ordering.append(commit_hash)

        parents = get_parents(parse_object(repo_path, commit_hash))

        for parent_hash in parents:
            indegree[parent_hash] -= 1
            if indegree[parent_hash] == 0:
                queue.append(parent_hash)

    #########################################################################

    # Output ordering in format requested
    sticky_created = False
    for i in range(len(topological_ordering)):
        # Handle sticky start
        if sticky_created is True:
            sticky_created = False
            print("=", end="")
            children_nodes = graph[topological_ordering[i]].children
            children = []
            for node in children_nodes:
                children.append(node.commit_hash)
            print(*children)

        print(topological_ordering[i], end="")

        # Print the branches associated with it in order
        if topological_ordering[i] in hash_to_branch:
            branches_for_commit = hash_to_branch[topological_ordering[i]]
            branches_for_commit.sort()  # Make sure in lexiographic order
            print(" ", end="")  # Separate from the previous print
            print(*branches_for_commit, end="")
        print()  # Newline it

        # Finished, don't check next commit because there is none
        if i == len(topological_ordering) - 1:
            break

        # Handle sticky end
        parents = get_parents(parse_object(repo_path, topological_ordering[i]))
        if topological_ordering[i + 1] not in parents:
            sticky_created = True
            print(*parents, end="")
            print("=\n")


if __name__ == "__main__":
    topo_order_commits()
