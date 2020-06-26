from sys import maxsize
from pprint import pprint

# implementation of traveling Salesman Problem

class TSPMatrix():

    def __init__(self, **kwargs):
        self.matrix = kwargs.get('matrix', [])
        self.map_list = kwargs.get('map_list', [])

    def from_gmaps_matrix(self, gmaps_matrix_dict:dict, **kwargs):
        self.map_list = kwargs.get('map_list', gmaps_matrix_dict['origin_addresses'])

        if gmaps_matrix_dict['status'] == 'OK':
            origin_addresses = gmaps_matrix_dict['origin_addresses']
            destination_addresses = gmaps_matrix_dict['destination_addresses']
            rows = gmaps_matrix_dict['rows']
            for row in rows:
                el_list = []
                for element in row['elements']:
                    el_list.append(element['distance']['value'])
                self.matrix.append(el_list)
            pprint(self.matrix)
        return self

class TSP(TSPMatrix):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Enjoy the Algorithm!!!")

    def normal_ans(self, start=0, **kwargs):

        graph = kwargs.get('graph', self.matrix)

        # store all vertex apart from source vertex
        V = len(graph)
        # V = 4
        s = start
        vertex = []
        for i in range(V):
            if i != s:
                vertex.append(i)
        # store minimum weight Hamiltonian Cycle
        min_path = maxsize
        Visted_dict = {}

        # next_permutation implementation
        def next_permutation(L):
            # It will change the list L.
            n = len(L)
            i = n - 2
            while i >= 0 and L[i] >= L[i + 1]:
                i -= 1
            if i == -1:
                return False
            j = i + 1
            while j < n and L[j] > L[i]:
                j += 1
            j -= 1
            L[i], L[j] = L[j], L[i]
            left = i + 1
            right = n - 1
            while left < right:
                L[left], L[right] = L[right], L[left]
                left += 1
                right -= 1
            return True

        while True:
            # store current Path weight(cost)
            current_pathweight = 0
            # compute current path weight
            k = s
            for i in range(len(vertex)):
                current_pathweight += graph[k][vertex[i]]
                k = vertex[i]
            current_pathweight += graph[k][s]
            Visted_dict[current_pathweight] = list(vertex) #用list把它給實例化並存在dict裡，
            # update minimum
            min_path = min(min_path, current_pathweight)
            if not next_permutation(vertex):
                break
        # pprint(Visted_dict)

        # return min_path, list(map(self.map_list,Visted_dict[min_path][::-1]))
        order_list = [self.map_list[i] for i in Visted_dict[min_path][::-1]] if self.map_list else Visted_dict[min_path][::-1]
        return min_path, order_list

    def backtracking_ans(self, start=0, **kwargs):

        graph = kwargs.get('graph', self.matrix)

        def tsp(graph, v, currPos, n, count, cost): 
            # If last node is reached and it has  
            # a link to the starting node i.e  
            # the source then keep the minimum  
            # value out of the total cost of  
            # traversal and "ans" 
            # Finally return to check for  
            # more possible values 
            if (count == n and graph[currPos][0]): 
                answer.append(cost + graph[currPos][0]) 
                return
        
            # BACKTRACKING STEP 
            # Loop to traverse the adjacency list 
            # of currPos node and increasing the count 
            # by 1 and cost by graph[currPos][i] value 
            for i in range(n): 
                if (v[i] == False and graph[currPos][i]): 
                    # Mark as visited 
                    v[i] = True
                    tsp(graph, v, i, n, count + 1, cost + graph[currPos][i]) 
                    # Mark ith node as unvisited 
                    v[i] = False

        n = len(graph)
        v = [False for i in range(n)] 
        v[start] = True
        answer = []
        tsp(graph, v, 0, n, 1, 0)

        return min(answer)
        