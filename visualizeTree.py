"""
 png image name to a list for use with "showVideo" class         
"""

import pydot


class visualizeTree(object):
    def __init__(self, fileDir, fileName='bst_graph', fileExt='.png', vidFrames=1, fileCount=0):
        self.fileDir = fileDir      # string, full directory path to where image sequence files will be stored
        self.fileName = fileName    # string, base name of the file 
        self.fileExt = fileExt      # string, image file extension (currently ".png" is the only supported type)
        self.vidFrames = vidFrames  # integer, a counter used generate duplicate copies of the PNG image files,
                                    #   a way to stretch the video time line.
        self.fileCount = fileCount  # integer, first number to use with generate sequenced image files.                                    
        
        self.treeList = []       # storage for the DFS or BFS tree search as a queue or stack
        self.nodeNames = {}      # store each node name (key) with each node's pyDot object (value), used by draw() method to ensure each node is drawn once
        self.fullFileName = ""   # store the current full file name for png images
        
        self.visualizeList = []  # hold unique png files for Tkinter display
        
        self.initGraph(graph_type='digraph', nodesep=.5, pad=.3, size="19.2, 10.1")
        self.setNodeDefaults(style="filled", fillcolor="grey", shape="circle")
        self.setEdgeDefaults(color="blue", arrowhead="vee")
        
    def initGraph(self, **kwargs):           
        # Initialize a directional graph
        #     Dot attributes:
        #     graph_type = "graph" (edges drawn as lines)| "digraph" (edges drawn as arrows)
        #     rankdir= "TB", "LR", "BT", "RL", corresponding to directed graphs drawn from top to bottom, from left to right, from bottom to top, and from right to left, respectively.
        #     ranksep=float_value: rank separation in fraction of an inch 0.75 default, minimum vertical distance between nodes of equal rank
        #     nodesep=float_value: node separation in fraction of an inch 0.25 default, minimum horizontal distance between nodes of equal rank
        #     size = "string_value width, string_value height" in inches. Example: size="4, 8"
        #     dpi=300 for better image quality, or dpi=96 for default value
        #     optional layout="neato" | "sfpd" | "fpd" | "twopi" | "circo" to create a differently style for graph
        #     pad=float_value for both width and height of pad around graph margins, in inches (.3 seems to be a good value)
        #     bgcolor="red" set the background color
        #     label="hello" set a text label just below the graph
        self.graph = pydot.Dot(**kwargs)

    def setNodeDefaults(self, **kwargs):        
        # Set default node attributes
        #     Node attributes:
        #     style = 'filled' | 'invisible' 
        #           Many more options here: http://www.graphviz.org/doc/info/attrs.html#d:peripheries
        #     shape = 'box' | 'ellipse' | 'circle' | 'point' | 'triangle'
        #           Many more shapes here: http://www.graphviz.org/doc/info/shapes.html
        #     fillcolor = "grey" for example, the color of the shape inside
        #     color = "red" for example, the color of the shapes outer border (or borders with 'doublecircle')
        #     height and width float_value inches, for example: height=1.5, width=1.5
        #     text control: 'fontcolor', 'fontsize', 'label', 'fontname',  
        self.graph.set_node_defaults(**kwargs)    

    def setEdgeDefaults(self, **kwargs):        
        # Set edge attributes
        #     Edge attributes:
        #     style     = 'dashed' | 'dotted' | 'solid' | 'invis' | 'bold'
        #     arrowhead = 'box' | 'crow' | 'diamond' | 'dot' | 'inv' | 'none' | 'tee' | 'vee'
        #     place a label: label="and back we go again", labelfontcolor="#009933", fontsize="10.0"
        #     Adjust weighted flexibility in edge drawings: weight="0" for maximum flex, "3" for 
        #     minlen=2 minimum edge length in inches (default is 1
        #     weight="0" to "100"
        self.graph.set_edge_defaults(**kwargs)        
      
    def setVidFrames(self, vidFrames):
        # Method to control the number of duplicate png images to generate (ie stretch or shrink video time)          
        self.vidFrames = vidFrames

    def searchTree(self, root, searchMethod, find=None):
        # Method to search a binary tree
        # Input:
        #     searchMethod is a helper function that defines the type of search to perform, 
        #        current examples implemented: DFS, BFS, and DFSOrdered
        #     find is string representing the node to search and highlight, or None to display full binary tree 
        # Output:
        #     True if node is found, or False if node is not found, or False when drawing the full tree (not searching)          
        self.treeList = [root]
        while len(self.treeList) > 0:
            node = self.treeList.pop(0)
            if node!=None:
                #print str(node) # activate to display nodes searched when debug needed
                if find==str(node):
                    self.highlightNodeFound(str(node))
                    return True
                elif find!=None:
                    self.blinkNodeTraversed(str(node))            
                searchMethod(node, self.treeList, find, self.draw)    
        return False

    def draw(self, parent_name, child_name=None, fill_color="grey", style_type='filled'):
        # Method to draw a node and an edge of a Binary Tree
        # Input:
        #   parent_name is a string lable identifying the parent node to draw (if not drawn already)
        #   child_name is a string lable identifying the child node to draw (or None, for a one node tree)
        #   fill_color is the color to fill nodes drawn
        #   style_type is either "filled" for normal drawing of tree nodes, or "invisible" for drawing nodes not part of tree          
        if not child_name:
            # Draw a tree with only one node
            self.nodeNames[parent_name] = pydot.Node(parent_name, label=parent_name, fillcolor=fill_color, style=style_type)
            self.graph.add_node(self.nodeNames[parent_name]) 
            return            
                                      
        if style_type=="invisible":
            # save original edge defaults
            weight_ = "100"
            saveEdgeDefaults = self.graph.get_edge_defaults()[0]
            self.graph.set_edge_defaults(style=style_type, color="white", arrowhead="none")  # comment during debug
            ###fill_color="#6699cc"  # debug, display invisible edges and nodes as light blue
            ###style_type="filled"   # debug, display invisible edges and nodes as light blue  
        else:
            weight_ = "3"
        edge = pydot.Edge(parent_name, child_name, style=style_type, weight=weight_)
        self.graph.add_edge(edge)  
        if style_type=="invisible":
            # restore original edge defaults
            self.graph.set_edge_defaults(**saveEdgeDefaults)        

        if not self.nodeNames:
            # root node identified (the top most tree element)
            self.nodeNames[parent_name] = pydot.Node(parent_name, label=parent_name, fillcolor=fill_color, style=style_type)
            self.graph.add_node(self.nodeNames[parent_name]) 
        if (parent_name not in self.nodeNames):
            # node (a tree element with leaves) identified       
            self.nodeNames[parent_name] = pydot.Node(parent_name, label=parent_name, fillcolor=fill_color, style=style_type)
            self.graph.add_node(self.nodeNames[parent_name])
        if child_name not in self.nodeNames:
            # leaf element identified (a parent with no children) 
            self.nodeNames[child_name] = pydot.Node(child_name, label=child_name, fillcolor=fill_color, style=style_type)
            self.graph.add_node(self.nodeNames[child_name])
                     
    def highlightNodeFound(self, node):
        # Method to animate the found node in a search tree         
        self.graph.add_node(pydot.Node(node, fillcolor="green"))
        self.updateGraph() 
        self.appendVisualizeList()
        
    def appendVisualizeList(self):
        self.visualizeList.append(self.fullFileName)    
  
    def blinkNodeTraversed(self, node):
        # Method to animate a node being traversed in a search tree  
        self.graph.add_node(pydot.Node(node, fillcolor="red"))
        self.updateGraph()
        self.appendVisualizeList()
        # use a redish grey color #cc9999 to show a breadcrumb to searched nodes in tree
        self.graph.add_node(pydot.Node(node, fillcolor="#cc9999"))
        self.updateGraph()        
             
    def setFileName(self):
        # Method to set the file name based on:
        #    directory, name, count and extension in support of our ffmpeg png to video batch file  
        self.fullFileName = self.fileDir + self.fileName + '%05d' % self.fileCount + self.fileExt
    
    def getFileName(self, count=None):
        if count == None:
            # Method to get the current full file name         
            return self.fullFileName
        else:
            return self.fileDir + self.fileName + '%05d' % count + self.fileExt
    
    def getFileCount(self):
        # Method to return maximum file count: the number of png images created
        return self.fileCount
    
    def updateGraph(self):
        # Method to write multiple copies of the same png image in support of ffmpeg png to video batch file        
        for i in range(0, self.vidFrames):
            self.fileCount += 1
            self.setFileName()
            self.graph.write_png(self.fullFileName)   


# Helper search functions for use with visualizeTree's method named "searchTree()"
# --------------------------------------------------------------------------------

def DFS(node, queue, find=None, draw=None):
    # Depth First Search helper function for binaryTree.searchTree(): 
    #    Start at root followed by all nodes from top to bottom, then left to right,
    #       until key value found or queue exhausted.
    # Input:
    #     node: Current node in binary tree,
    #     queue: First in First out (FIFO) ,
    #     find and draw: Unused. 
    if node.getRightBranch():
        queue.insert(0, node.getRightBranch())
    if node.getLeftBranch():
        queue.insert(0, node.getLeftBranch())   
            
def DFSOrdered(node, queue, find, draw=None):
    # Ordered Depth First Search helper function for binaryTree.searchTree(): 
    #    Start at root followed by selected nodes from top to bottom, then left to right,
    #       that meet our find requirment, until key value found or leaf node examined.
    # Input:
    #     node: Current node in binary tree,
    #     queue: First in First out (FIFO) ,
    #     find: the string value we are searching for in a tree,
    #     draw: Unused.       
    if node:                                                        
        if node.getRightBranch() and find > str(node.getValue()):
            queue.insert(0, node.getRightBranch())
        if node.getLeftBranch() and find < str(node.getValue()):
            queue.insert(0, node.getLeftBranch())        

def BFS(node, stack, find=None, draw=None):
    # Breadth First Search helper function for binaryTree.searchTree(): 
    #    Start at root followed by all nodes from left to right, then top to bottom,
    #       until key value found or queue exhausted.
    # Input:
    #     node: Current node in binary tree,
    #     stack: Last in First out (LIFO) ,
    #     find and draw: Unused.     
    if node.getLeftBranch():
        stack.append(node.getLeftBranch())       
    if node.getRightBranch():
        stack.append(node.getRightBranch())          

# Sketch complete tree
# makes calls to visualizeTree's draw() method to graph edge and node elements
# Input: node in binary tree, stack for depth first drawing
# Unused: find
def sketchTree(node, stack, find=None, draw=None):
    if node.getLeftBranch():
        draw(str(node), str(node.getLeftBranch()))
        stack.append(node.getLeftBranch()) 
        if node.getRightBranch():
            # insert invisible third node in-between left and right nodes
            draw(str(node), ":"+str(node), style_type="invisible")
    elif node.getRightBranch():
        # draw any missing left branches as invisible nodes/edges with dummy unique labels 
        draw(str(node), ":"+str(node), style_type="invisible")
    if node.getRightBranch():
        draw(str(node), str(node.getRightBranch()))
        stack.append(node.getRightBranch())      
    elif node.getLeftBranch():
        # draw any missing right branches as invisible nodes/edges with dummy unique labels 
        draw(str(node), ";"+str(node), style_type="invisible")
    if not node.getLeftBranch() and not node.getRightBranch() and not node.getParent():
        # special case: draw a tree with only one node
        draw(str(node))
