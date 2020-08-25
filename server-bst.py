import socket                
from thread import *
import threading

ClientCount = 0
client_identities = {}
cl_id = 0
output_file = 'output3.txt'

class Node:
    def __init__(self,val,client_id):
        self.val = val
        self.client_id = client_id
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None
    def getRoot(self):
        return self.root
    # Add root into the tree
    def add(self,val,client_id):
        if self.root is None:
            self.root = Node(val,client_id)
        else:
            self.add_child(val,client_id,self.root)
    # Adding child for the root node
    def add_child(self,val,client_id,node):
        if val < node.val:
            if node.left is not None:
                self.add_child(val,client_id,node.left)
            else:
                node.left = Node(val,client_id)
        else:
            if node.right is not None:
                self.add_child(val,client_id,node.right)
            else:
                node.right = Node(val,client_id)
    # getting the nodes of data level by level
    def level_order_traversal(self, queue,depth,level_dict,level_count,data_click):
        queue_new = []
        data = []
        if not queue:
            return
        else:
            for node in queue:
                temp_dict = {}
                if node.left is not None:
                    queue_new.append(node.left)
                    node_data = str(node.left.val)+'['+str(node.left.client_id)+']'
                    temp_dict['left'] = node_data
                else:
                    temp_dict['left'] = None
                if node.right is not None:
                    queue_new.append(node.right)
                    node_data = str(node.right.val)+'['+str(node.right.client_id)+']'
                    temp_dict['right'] = node_data
                else:
                    temp_dict['right'] = None
                node_data = str(node.val)+'['+str(node.client_id)+']'
                data_click[node_data] = temp_dict
                data.append(node_data)
            if level_count not in level_dict:
                level_dict[level_count] = data
                level_count += 1
        self.level_order_traversal(queue_new,depth,level_dict,level_count,data_click)
    # Getting the Depth(height) of the tree
    def max_depth(self, this_node):
        if this_node is None:
            return 0
        left_subtree = self.max_depth(this_node.left)
        right_subtree = self.max_depth(this_node.right)
        return 1 + max(left_subtree, right_subtree)
    # getting a child node from the parent
    def childrenForParent(self,parent_data,data_click):
        children_list = []
        if parent_data is not None:
            temp_par_dict = data_click[parent_data]
            children_list.append(temp_par_dict['left'])
            children_list.append(temp_par_dict['right'])
        else:
            children_list.append(None)
            children_list.append(None)
        return children_list
    # getting a list -> contains the number of data's which are supposed to be in the level
    def get_node_list(self,depth,level,list_data,data_click,level_record):
        list_nodes = []
        if level == 0:
            list_nodes.append(str(self.root.val)+'['+str(self.root.client_id)+']')
            return list_nodes   
        if level in level_record:
            parent_list = level_record[level-1]
            for parent in parent_list:
                list_nodes.extend(self.childrenForParent(parent,data_click))
            return list_nodes
    def getWhiteSpaces(self,count):
        return " "*count
    # providing the string which is to be print into the output file 
    def give_tree(self,depth,level,level_record):
        value = depth - (level+1)
        firstSpaces = pow(2,value) - 1  
        betweenSpaces = pow(2,(value + 1)) - 1
        string_to_print = ""
        string_to_print += self.getWhiteSpaces(int(firstSpaces))
        data_from_level = level_record[level]
        for i in range(0,len(data_from_level)):
            if data_from_level[i] is not None:
                string_to_print += str(data_from_level[i])
            else:
                string_to_print += "   "
            if i != len(data_from_level) - 1:
                string_to_print += self.getWhiteSpaces(int(betweenSpaces))        
        return string_to_print
    # For writting the tree structure
    def print_treeStructure(self,depth,level_dict,data_click):
        with open(output_file, "w", buffering=0) as text_file:
            level_record = {}
            for i in range(0,depth):
                level_record[i] = []
            for level,list_data in level_dict.items():
                level_record[level] = self.get_node_list(depth,level,list_data,data_click,level_record)
                tree_data = self.give_tree(depth,level,level_record)
                text_file.write(tree_data)
                text_file.write('\n')
                text_file.write('\n')
            text_file.close()
    def find(self, val):
        return self.findNode(self.root, val)
    def findNode(self, currentNode, val):
        if(currentNode is None):
            return False
        elif(val == currentNode.val):
            return True
        elif(val < currentNode.val):
            return self.findNode(currentNode.left, val)
        else:
            return self.findNode(currentNode.right, val)

class startServer(threading.Thread):

    def __init__ (self, conn,address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.lock = threading.Lock()

    def run(self):
        self.threaded_client(self.conn,self.address,self.lock)

    def threaded_client(self,connection,addr,lock):
        connection.send(str.encode('Welcome to the Server\n'))
        global cl_id
        global client_identities
        while True:
            data = connection.recv(2048)
            if not data:
                break 
            lock.acquire()            
            key = addr[1]
            if key not in client_identities.keys():
                cl_id +=1
                client_identities[key] = cl_id
            else:
                cl_id = client_identities[key]
            if tree.find(int(data)):
                print int(data) ," is already exists in tree for the client id : ", cl_id
            else:
                tree.add(int(data),cl_id)
                depth = tree.max_depth(tree.root)
                level_dict_data = {}
                data_click = {}
                tree.level_order_traversal([tree.getRoot()],depth,level_dict_data,0,data_click)
                tree.print_treeStructure(depth,level_dict_data,data_click)
            lock.release()
        connection.close()

if __name__ == '__main__':
    ServerSocket = socket.socket()
    print "Socket successfully created"  
    host = socket.gethostname()
    port = 1234               
    ServerSocket.bind((host, port))         
    print "socket binded to %s" %(port) 
    ServerSocket.listen(5)      
    print "socket is listening" 
    threads = []
    tree = Tree()
    while True: 
        Client, addr = ServerSocket.accept()      
        Client.send('Thank you for connecting')
        thread = startServer(Client,addr)
        thread.start()
        threads.append(thread)
        ClientCount += 1
        # print('Client count: ' + str(ClientCount))
    for thread in threads:
        thread.join()
    ServerSocket.close()       
  