import node

class AAPathFinder(object):

    def __init__( self     ,
                  inAAGrid ,
                  inView   ):
        '''
        Class to handle finding the path between the start nodes using
        A* search algorithm.

        Args:
            inAAGrid (grid.AAGrid): Grid to explore nodes from.

            inView (view.View): View to handle delay displaying
                                of the algorithm progress
        '''
        self.view = inView

        self.grid = inAAGrid

        if len(self.grid.goalNodes) != 2:
            print 'Need at least start and end point.'
            return

        self.startNode , self.endNode = self.grid.goalNodes

        self.findPath()

    def findPath( self ):
        '''
        Find a path between the start and end Node through
        A* search algorithm.

        Returns:
            None: No return value.
        '''
        openNodes = []
        closedNodes = set()
        openNodes.append( self.startNode )

        while len(openNodes) > 0:

            currentNode = openNodes[ 0 ]

            for aaNode in openNodes:

                if aaNode is currentNode:
                    continue

                if aaNode.fCost <= currentNode.fCost:
                    if aaNode.hCost < currentNode.hCost:
                        currentNode = aaNode

            openNodes.remove(currentNode)
            closedNodes.add(currentNode)

            if currentNode == self.endNode:
                self.retracePath( self.endNode )
                return

            neighborsToExploreWithDelay = []

            for neighbourNode in self.grid.getNeighbours( currentNode ):

                if neighbourNode.currentState == node.AANode.WALL_STATE:
                    continue

                neighborsToExploreWithDelay.append( neighbourNode.setToExplored )

                if neighbourNode in closedNodes:
                    continue

                newCostToNeighbour = currentNode.gCost + currentNode.distanceTo( neighbourNode )

                if newCostToNeighbour < neighbourNode.gCost or neighbourNode not in openNodes:

                    neighbourNode.gCost = newCostToNeighbour
                    neighbourNode.hCost = neighbourNode.distanceTo( self.endNode )
                    neighbourNode.parentNode = currentNode

                    if neighbourNode not in openNodes:
                        openNodes.append( neighbourNode )

            self.view.startTimer( neighborsToExploreWithDelay )

    def retracePath( self   ,
                     inNode ):
        '''
        After a path has been found from the start to the end node
        a singly-linked list is accesible through starting from the end node,
        Display the path with a delay.

        Args:
            inNode (node.AANode): End Node to start retracing the found path.

        Returns:
            None: No return value.
        '''
        parentLinkedList = []

        while inNode:
            parentLinkedList.append( inNode )
            inNode = inNode.parentNode

        self.view.startTimer( [ aaNode.setToPath for aaNode in reversed( parentLinkedList ) ] )
