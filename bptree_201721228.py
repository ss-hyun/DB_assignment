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
        sp = btree.min
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
                par.split(btree)
        else:
            n_root = Node([ key ], [ self, n_right ], None, False, None, None)
            btree.root = n_root
            self.parent = n_root
            n_right.parent = n_root

    def merge(self, btree):
        if len(self.keys) < btree.min:
            par = self.parent
            if par is None: # self is root node
                if not self.keys:   # is empty node
                    if self.isLeaf: btree.root = None
                    else:
                        btree.root = self.subTrees[0]
                        btree.root.parent = None
                return
            idx = par.subTrees.index(self)
            if  idx:    # left sibling exist
                if len(par.subTrees[idx-1].keys) > btree.min:      # borrow from left sibling
                    if self.isLeaf: self.values.insert(0, par.subTrees[idx-1].values.pop())
                    else:
                        self.subTrees.insert(0, par.subTrees[idx-1].subTrees.pop())
                        self.subTrees[0].parent = self
                    self.keys.insert(0, par.subTrees[idx-1].keys.pop())
                    par.keys[idx-1] = self.keys[0]
                    return
            if idx+1 < len(par.subTrees): # right sibling exist, can't borrow from left sibling
                if len(par.subTrees[idx+1].keys) > btree.min: # borrow from right sibling
                    if self.isLeaf: self.values.append(par.subTrees[idx+1].values.pop(0))
                    else:
                        par.subTrees[idx+1].subTrees[0].parent = self
                        self.subTrees.append(par.subTrees[idx+1].subTrees.pop(0))
                    self.keys.append(par.subTrees[idx+1].keys.pop(0))
                    par.keys[idx] = par.subTrees[idx+1].keys[0]
                    return
            # can't borrow anything
            if idx: # left sibling exist, merge with left sibling
                if self.isLeaf:
                    par.subTrees[idx-1].values.extend(self.values)
                    par.subTrees[idx-1].nextNode = self.nextNode
                    del par.keys[idx-1]
                else:
                    for sn in self.subTrees:
                        sn.parent = par.subTrees[idx-1]
                    par.subTrees[idx-1].keys.append(par.keys.pop(idx-1))
                    par.subTrees[idx-1].subTrees.extend(self.subTrees)
                par.subTrees[idx-1].keys.extend(self.keys)
                del par.subTrees[idx]
                # key field merge
                par.merge(btree)
                return
            # left sibling doesn't exist, merge with right sibling
            if idx+1 < len(par.subTrees):
                if self.isLeaf:
                    self.values.extend(par.subTrees[idx+1].values)
                    self.nextNode = par.subTrees[idx+1].nextNode
                    del par.keys[idx]
                else:
                    for sn in par.subTrees[idx+1].subTrees:
                        sn.parent = self
                    self.subTrees.extend(par.subTrees[idx+1].subTrees)
                    self.keys.append(par.keys.pop(idx))
                self.keys.extend(par.subTrees[idx+1].keys)
                del par.subTrees[idx+1]
                # key field merge
                par.merge(btree)
                return

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
        self.min = order // 2  # leaf data(key=value) number min, inner key number min, inner tree pointer number min - 1
        self.root  = None
        
    def insert(self, k):
        if self.root is None: 
            n = Node([ k ], None, None, True, None, [ k ])
            self.root = n
            return

        if self.isExist(k):
            print("{} already exists in the btree".format(k))
            return

        n = self.root

        while not n.isLeaf:
            i = 0
            while i < len(n.keys):
                if k < n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]
        
        i = 0
        l = len(n.keys)
        while i < l:
            if k < n.keys[i]:
                break
            i += 1
        
        n.keys.insert(i, k)
        n.values.insert(i, k)
        if l + 1 == self.order:
            n.split(self)
    
    def delete(self, k):
        n = self.root
        while not n.isLeaf:
            i = 0
            while i < len(n.keys) and k >= n.keys[i]:
                i += 1
            n = n.subTrees[i]
        i = 0
        while i < len(n.keys):
            if k == n.keys[i]:  # delete node if found 
                del n.keys[i]
                del n.values[i]
                n.merge(self)
            i += 1

        if not i:   # key field updated
            while par:
                if k in par.keys:
                    par.keys[par.keys.index(k)] = n.keys[0]
                    break
                par = par.parent

    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self):
        curr = self.root
        ndList = []
        while curr:
            curr.print_node()
            if not curr.isLeaf: ndList.extend(curr.subTrees)
            if not ndList: break
            curr = ndList.pop(0)
            if curr.isLeaf: break
        
    def find_range(self, k_from, k_to):
        n = self.root
        while not n.isLeaf:
            i = 0
            while i < len(n.keys):
                if k_from < n.keys[i]:
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
        str = ''
        while not n.isLeaf:
            str += '{}-'.format(n.keys)
            i = 0
            while i < len(n.keys):
                if k < n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]
        for key in n.keys:
            if k == key:
                print(str+'{}'.format(n.keys))
                return
        print("NONE")


    def isExist(self, k):
        n = self.root
        while not n.isLeaf:
            i = 0
            while i < len(n.keys):
                if k < n.keys[i]:
                    break
                i += 1
            n = n.subTrees[i]
        for key in n.keys:
            if k == key:
                return True
        return False


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