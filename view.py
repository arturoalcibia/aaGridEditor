from PyQt5 import QtCore, QtWidgets, QtGui

import node
import pathfinding
import grid

class View(QtWidgets.QGraphicsView):

    MOUSE_DRAG_STATE = 0

    def __init__( self          ,
                  parent = None ):
        '''
        View Widget to display the nodes and handle all mouse and key events.
        '''

        super( View , self ).__init__( parent )

        # State to store between mousePress and mouseDrag event.
        # type: None|int
        self.currentMouseState  = None

        # Variable to store between mousePress and mouseDrag event,
        # False will paint blank nodes, True will paint walls.
        # type: bool
        self.dragPaintWallsBool = False

        # Set to store nodes to avoid multiple switching in
        # same mouseDrag event.
        # type: set(node.AANode)
        self.nodeHashesToSwitch = set()

        # Functions to execute with a delay using QTimer.
        # type: list(function)
        self.functionsToExecute = []

        self.timer = QtCore.QTimer()

        self.timer.timeout.connect( self.doWithDelay )

        self.setRenderHint( QtGui.QPainter.Antialiasing  ,
                            True                         )
        self.setRenderHint( QtGui.QPainter.HighQualityAntialiasing ,
                            True           )
        self.setRenderHint( QtGui.QPainter.SmoothPixmapTransform ,
                            True                                )

        self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )

        self.grid = grid.AAGrid()

        currentScene = QtWidgets.QGraphicsScene( self )
        currentScene.setSceneRect( 0                    ,
                                   0                    ,
                                   self.grid.WIDTH_INT  ,
                                   self.grid.HEIGHT_INT )
        self.setScene( currentScene )

        for gridX in xrange( int( self.scene().sceneRect().left()  ) ,
                             int( self.scene().sceneRect().right() ) ,
                             self.grid.NODE_SIZE_INT                 ):

            for gridY in xrange( int( self.scene().sceneRect().top()    ) ,
                                 int( self.scene().sceneRect().bottom() ) ,
                                 self.grid.NODE_SIZE_INT                  ):

                self.createNode( gridX                   ,
                                 gridY                   ,
                                 self.grid.NODE_SIZE_INT )

    def doWithDelay( self ):
        '''
        Execute from a list of functions with a delay.
        It will stop after the list is empty.

        Returns:
            None: No return value.
        '''
        if self.functionsToExecute:
            func = self.functionsToExecute[ 0 ]
            self.functionsToExecute.remove(func)
            func()
            return

        self.timer.stop()

    def startTimer( self        ,
                    inFunctions ):
        '''
        Start the timer to trigger the signal timeOut and start executing from
        a list of functions with a delay,

        Args:
            inFunctions (list(function)): List of functions to add to list.

        Returns:
             None: No return value.
        '''
        self.functionsToExecute.extend( inFunctions )
        self.timer.start( 1 )

    def createNode( self       ,
                    posX       ,
                    posY       ,
                    inGridSize ):
        '''
        Create a Node and add it to the qScene widget.

        Args:
            inPosX (int): Position in X axis to put the node at.

            inPosY (int): Position in Y axis to put the node at.

            inNodeSize (int): Size for the Node for width and height.

        Returns:
            None: No return value.
        '''
        aaNode = self.grid.createNode( posX       ,
                                       posY       ,
                                       inGridSize )

        self.scene().addItem( aaNode )

    def mousePressEvent( self  ,
                         event ):
        '''
        Event to execute when any mouse button is pressed.
        Will handle the setting of walls, removal and goal Nodes.

        Args:
            event (QTCore.QEvent).

        Returns:
            None: No return value.
        '''
        selectedNode  = self.scene().itemAt( self.mapToScene( event.pos() )      ,
                                                              QtGui.QTransform() )

        if not isinstance( selectedNode , node.AANode ):
            return

        if ( event.button()    == QtCore.Qt.LeftButton and
             event.modifiers() == QtCore.Qt.NoModifier     ):

            self.currentMouseState = self.MOUSE_DRAG_STATE

            selectedNode.switchWallState()

            self.dragPaintWallsBool = bool( selectedNode.currentState )

        elif ( event.button() == QtCore.Qt.LeftButton  and
               event.modifiers() == QtCore.Qt.AltModifier ):

            self.grid.setGoalNode( selectedNode )

    def mouseMoveEvent( self  ,
                        event ):
        '''
        Event to execute when mouse is moved with a mouse button pressed.
        Will handle the setting of walls, removal and goal Nodes.

        If clicked node was set as wall, it will start setting as walls
        where the mouse passes. same behaviour with blank nodes.

        Args:
            event (QTCore.QEvent).

        Returns:
            None: No return value.
        '''
        if self.currentMouseState == self.MOUSE_DRAG_STATE:

            selectedNode = self.scene().itemAt( self.mapToScene( event.pos() )  ,
                                                QtGui.QTransform()              )

            if not isinstance( selectedNode , node.AANode ):
                return

            if selectedNode in self.nodeHashesToSwitch:
                return

            if selectedNode.currentState == self.dragPaintWallsBool:
                return

            selectedNode.switchWallState()

            self.nodeHashesToSwitch.add( selectedNode )

    def mouseReleaseEvent( self  ,
                           event ):
        '''
        Event to execute when mouse button is released.
        Will handle the setting of walls, removal and goal Nodes.

        If clicked node was set as wall, it will start setting as walls
        where the mouse passes. same behaviour with blank nodes.

        Args:
            event (QTCore.QEvent).

        Returns:
            None: No return value.
        '''
        self.currentMouseState = None

        self.nodeHashesToSwitch.clear()

    def keyPressEvent( self  ,
                       event ):
        '''
        Event to execute when any key is pressed.
        Will handle the start and reset of the pathfinding.

        Args:
            event (QTCore.QEvent).

        Returns:
            None: No return value.
        '''
        if event.key() == QtCore.Qt.Key_Control:
            self.grid.reset()
            pathfinding.AAPathFinder( self.grid ,
                                      self      )

        if event.key() == QtCore.Qt.Key_Shift:
            self.grid.reset()
