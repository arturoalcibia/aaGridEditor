import node

class AAGrid(object):

    # Width and Height of Node.
    # type: int
    NODE_SIZE_INT = 20

    # Width of grid.
    # type: int
    WIDTH_INT = 1280

    # Height of grid.
    # type: int
    HEIGHT_INT = 720

    def __init__( self ):
        '''
        Grid Class that will handle the creation and
        accessing of nodes among other methods.
        '''
        # Nodes with their hashes
        # type: dict[node.AANode, str]
        self.nodeHashesMapping = {}

        # Hashes with their nodes.
        # type: dict[str, node.AANode]
        self.hashNodesMapping  = {}

        # Complete set of nodes.
        # type: dict[str, node.AANode]
        self.gridNodes         = set()

        # List of Nodes set as Start and destination
        # type: list[node.AANode]
        self.goalNodes = []

    def createNode( self       ,
                    inPosX     ,
                    inPosY     ,
                    inNodeSize ):
        '''
        Create a node with provided coordinates and size
        and add it into our dictionaries.

        Args:
            inPosX (int): Position in X axis to put the node at.

            inPosY (int): Position in Y axis to put the node at.

            inNodeSize (int): Size for the Node for width and height.

        Returns:
            node.AANode: created Node.
        '''
        aaNode = node.AANode( inPosX     ,
                              inPosY     ,
                              inNodeSize )

        hashCode = '{0}{1}'.format( inPosX , inPosY )

        self.nodeHashesMapping[ aaNode ]  = hashCode
        self.hashNodesMapping[ hashCode ] = aaNode
        self.gridNodes.add( aaNode )

        return aaNode

    def getNeighbours( self   ,
                       inNode ):
        '''
        Get neighboring nodes from inNode

        Args:
            inNode (node.AANode): Node to get neighbours from.

        Yields:
            node.AANode: neighbour node.
        '''
        nodePosX = inNode.posX
        nodePosY = inNode.posY

        surroundingHashes = ( '{0}{1}'.format(nodePosX + self.NODE_SIZE_INT ,
                                              nodePosY                      ) ,
                              '{0}{1}'.format(nodePosX - self.NODE_SIZE_INT ,
                                              nodePosY                      ) ,
                              '{0}{1}'.format(nodePosX                      ,
                                              nodePosY + self.NODE_SIZE_INT ) ,
                              '{0}{1}'.format(nodePosX                      ,
                                              nodePosY - self.NODE_SIZE_INT ) ,
                              '{0}{1}'.format(nodePosX + self.NODE_SIZE_INT ,
                                              nodePosY + self.NODE_SIZE_INT ) ,
                              '{0}{1}'.format(nodePosX - self.NODE_SIZE_INT ,
                                              nodePosY + self.NODE_SIZE_INT ) ,
                              '{0}{1}'.format(nodePosX + self.NODE_SIZE_INT ,
                                              nodePosY - self.NODE_SIZE_INT ) ,
                              '{0}{1}'.format(nodePosX - self.NODE_SIZE_INT ,
                                              nodePosY - self.NODE_SIZE_INT ) )

        for nodeHash in surroundingHashes:

            currentNode = self.hashNodesMapping.get( nodeHash )

            if not currentNode:
                continue

            yield currentNode

    def reset( self ):
        '''
        Reset all Nodes to start finding a path again,
        Will retain the nodes with walls and goal states.

        Returns:
            None: No return value.
        '''
        for aaNode in self.gridNodes:
            aaNode.reset()


    def setGoalNode( self   ,
                     inNode ):
        '''
        Set inNode as Goal node state,
        will delete a previous goal Node if there are two already.

        Args:
            inNode (node.AANode): Node to set as Goal state.

        Returns:
            None: No return value.
        '''
        if inNode.currentState == node.AANode.GOAL_POINT_STATE:
                return

        inNode.switchGoalPointState()

        if len( self.goalNodes ) == 2:

            nodeToRemove = self.goalNodes[ 0 ]

            nodeToRemove.currentState = node.AANode.BLANK_STATE

            self.goalNodes.remove( nodeToRemove )

        self.goalNodes.append( inNode )
