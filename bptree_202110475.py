import sys


class Node:
    def __init__(self, keys, subTrees, parent, isLeaf, nextNode, values):
        # each node can have |order - 1| keys
        self.keys = keys
        
        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = subTrees
        
        self.parent = parent
        self.isLeaf = isLeaf
        
        # leaf node has next node pointer
        self.nextNode = nextNode   
        self.values = values

    def split(self, btree):
        sp = btree.slice_point
        par = self.parent
        if self.isLeaf:
            n_right = Node(self.keys[sp:], None, par, True, self.nextNode, self.values[sp:])
            self.keys = self.keys[:sp]
            self.values = self.values[:sp]
            self.nextNode = n_right
            key = n_right.keys[0]
        else:
            n_right = Node(self.keys[sp+1:], self.subTrees[sp+1:], par, False, None, None)
            for sn in n_right.subTrees:
                sn.parent = n_right
            key = self.keys[sp]
            self.keys = self.keys[:sp]
            self.subTrees = self.subTrees[:sp+1]
        
        if par:
            i = 0
            l = len(par.keys)
            while i < l:
                if key < par.keys[i]:
                    break
                i += 1
            par.keys.insert(i, key)
            par.subTrees.insert(i+1, n_right)
            if l + 1 == btree.order:
                #btree.print_tree()
                par.split(btree)
                #btree.print_tree()
        else:
            n_root = Node([ key ], [ self, n_right ], None, False, None, None)
            btree.root = n_root
            self.parent = n_root
            n_right.parent = n_root

    def print_node(self):
        str = '{}-'.format(self.keys)
        if not self.isLeaf:
            for s in self.subTrees:
                str += '{},'.format(s.keys)
        str = str[:-1]
        print(str)


class B_PLUS_TREE:
    def __init__(self, order):
        self.order = order
        self.slice_point = order // 2
        self.root  = None
        pass      
        
    def insert(self, k):
        if self.root is None: 
            n = Node([ k ], None, None, True, None, [ k ])
            self.root = n
            return

        n = self.root

        while not n.isLeaf:
            i = 0
            while i < len(n.keys):
                if k <= n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]
        
        i = 0
        l = len(n.values)
        while i < l:
            if k < n.values[i]:
                break

            i += 1
        n.keys.insert(i, k)
        n.values.insert(i, k)
        if l + 1 == self.order:
            #self.print_tree()
            n.split(self)
            #self.print_tree()
    
    def delete(self, k):
        pass
    
    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self, n = None):
        if n is None:
            if self.root is None:   return
            n = self.root
        else:
            if n.isLeaf:    return
        n.print_node()
        if not n.isLeaf:
            for s in n.subTrees:
                self.print_tree(s)
            
        
    def find_range(self, k_from, k_to):
        n = self.root
        while not n.isLeaf:
            i = 0
            while i < len(n.keys):
                if k_from <= n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]

        i = 0
        str = ''
        while n and n.keys[i] <= k_to:
            if n.keys[i] >= k_from:
                str += ',{}'.format(n.values[i])
            i += 1
            if i == len(n.keys):
                i = 0
                n = n.nextNode
        print(str[1:])
        
    def find(self, k):
        n = self.root
        while not n.isLeaf:
            print(n.keys, end='-')
            i = 0
            while i < len(n.keys):
                if k <= n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]
        


def main():
    myTree = None
    
    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        comm = comm.upper()
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