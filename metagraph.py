from math import prod
from re import compile
from abc import ABC, abstractmethod


class InputDataParser:
    int_int = compile(r'(\d+) *(\d+)')
    e_func = compile(r'((\*)|([ev] *\d+)|(\d+(\.\d+)?(e[\+-]?\d+)?))')
    v_func = compile(r'((min)|([ev] *\d+)|(\d+(\.\d+)?(e[\+-]?\d+)?))')

    def __init__(self, src):
        with open(src, mode='r') as f:
            self.NV, self.NE = self.parse_NV_NE(f)                          # Read number of vertexes and edges
            self.edges = self.parse_edges(f)                                # Read topology of the graph
            self.vertex_rules = self.parse_rules(f, self.NV, self.v_func)   # Read Agent-functions of vertexes
            self.edges_rules = self.parse_rules(f, self.NE, self.e_func)    # Read Agent-functions of edges
            
    def parse_NV_NE(self, f):
        line = f.readline()
        _ = f.readline()
        return tuple(map(int, self.int_int.findall(line)[0]))

    def parse_edges(self, f):
        res = []

        line = f.readline()
        while repr(line) != repr('\n'):
            res.append(tuple(map(int, self.int_int.findall(line)[0])))
            line = f.readline()

        return res

    def parse_rules(self, f, N, pattern):
        res = []
        for _ in range(N):
            line = f.readline()
            rule = pattern.findall(line)[0][0].replace(' ','')
            
            if rule.replace('.', '', 1).isdigit():
                res.append(float(rule))
            else:
                res.append(rule)
        
        return res


class Metagraph:
    _vertexes = {}
    _edges = {}

    def __init__(self, inp_pth):
        self.data = InputDataParser(inp_pth)    # Parse file with parameters of the problem

        self.init_items(                        # Vertexes initialization
            N=self.data.NV,
            rules_dict=self.data.vertex_rules,
            items_dict=self._vertexes,
            cls=Vertex,
            key=lambda x: x+1
        )

        self.init_items(                        # Edges initialization
            N=self.data.NE,
            rules_dict=self.data.edges_rules,
            items_dict=self._edges,
            cls=Edge,
            key=lambda x: self.data.edges[x]
        )
        
        self.link_graph()                       # Link all elements of the graph
    
    @staticmethod
    def init_items(N, rules_dict, items_dict, cls, key):
        for i in range(N):
            val = None

            if isinstance(rules_dict[i], float):
                val = rules_dict[i]                
    
            items_dict[key(i)] = cls(val, rules_dict[i])

    def link_graph(self):
        for e in self._edges:
            self._edges[e].income[e[0]] = self._vertexes[e[0]]
            self._vertexes[e[1]].income[e] = self._edges[e]

    def calculate_attributes(self):
        def items_without_attributes(items_dict):
            res = []
            
            for e in items_dict:
                if items_dict[e].val == None:
                    res.append(e)
            return res
        
        def check_items(items_to_check, items_list):
            res = items_to_check.copy()

            for i in range(len(items_to_check)):                
                if items_list[items_to_check[i]].try_set_value() != None:
                    res.remove(items_to_check[i])

            return res

        edges_left = items_without_attributes(self._edges)
        vertexes_left = items_without_attributes(self._vertexes)
        
        while len(edges_left) > 0 or len(vertexes_left) > 0:
            items_left = edges_left + vertexes_left
            edges_left = check_items(edges_left, self._edges)
            vertexes_left = check_items(vertexes_left, self._vertexes)
            
            if items_left == edges_left + vertexes_left:
                raise ValueError("Incorrect metagraph! It's imposible to find some attributes!")

    def print_attrs_in_file(self, name):
        with open(name, mode='w') as f:
            for e in self._vertexes:
                f.write(str(self._vertexes[e].val)+'\n')

            for e in self._edges:
                f.write(str(self._edges[e].val)+'\n')


class AbstractGraphElement(ABC, Metagraph):
    def __init__(self, val, func):
        self.func = func                    # Agent-function of the graph element
        self.val = val                      # Attribute of the graph element
        self.income = {}                    # Dict of previous elements

    def try_set_value(self):
        
        if self.func[0] in ['v', 'e'] and self.func[1:].isdigit():
            if self.func[0] == 'v':
                self.val = self._vertexes[int(self.func[1:])].val
            else:
                self.val = self._edges[list(self._edges.keys())[int(self.func[1:]) - 1]].val

        elif self.multioperand_cond():
            self.val = self.mult_operator()

        return self.val
    
    @abstractmethod
    def multioperand_cond(self):
        '''This function checks if element of the graph is ready to perfom attribute calculation
           with complex operator ('*' for edges and 'min' for vertexes)'''

    @abstractmethod
    def mult_operator(self):
        '''This function perfom attribute calculation with complex operator
           ('*' for edges and 'min' for vertexes)'''


class Vertex(AbstractGraphElement):
    multioperand_cond = lambda x: x.func == 'min' and all([x.income[e].val != None for e in x.income])
    mult_operator = lambda x: min([x.income[e].val for e in x.income])


class Edge(AbstractGraphElement):

    def multioperand_cond(self):
        C1 = self.func == '*'
        C2 = self.income[list(self.income.keys())[0]].val != None
        C3 = all([e.val != None for e in self.income[list(self.income.keys())[0]].income.values()])
        return (C1 and C2 and C3)
    
    def mult_operator(self):
        x1 = prod([e.val for e in self.income[list(self.income.keys())[0]].income.values()])
        x2 = self.income[list(self.income.keys())[0]].val
        return x1*x2
    
