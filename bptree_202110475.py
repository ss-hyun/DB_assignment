import sys


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []
        
        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = []
        
        self.parent = None
        self.isLeaf = False
        
        # leaf node has next node pointer
        self.nextNode = None   
        self.values = []


class B_PLUS_TREE:
    def __init__(self, order):
        self.order = order
        self.root  = None
        pass      
        
    def insert(self, k):        
        n = Node()
        n.keys.append(k)
        n.values.append(k)
        self.root = n
        pass
    
    def delete(self, k):
        pass
    
    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self):
        pass
        
    def find_range(self, k_from, k_to):
        pass
        
    def find(self, k):
        pass


def main():
    myTree = None
    
    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue
        
        print(comm)
        
        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)
            
        elif params[0] == "EXIT":
            return
            
        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)
            
        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)            
            
        elif params[0] == "ROOT":            
            myTree.print_root()            
            
        elif params[0] == "PRINT":            
            myTree.print_tree()            
                  
        elif params[0] == "FIND":            
            k = int(params[1])
            myTree.find(k)
            
        elif params[0] == "RANGE":            
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)
        
        elif params[0] == "SEP":
            print("-------------------------")
    
if __name__ == "__main__":
    main()