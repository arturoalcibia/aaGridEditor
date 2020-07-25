from PyQt5 import QtWidgets, QtCore, QtGui

class AANode(QtWidgets.QGraphicsItem):
    """
    A graphic representation of a node.
    """

    WALL_COLOR        = QtGui.QColor( 100 , 100 , 100 , 255 )

    BLANK_COLOR       = QtGui.QColor( 50 , 50 , 50 , 255 )

    BORDER_COLOR      = QtGui.QColor( 70 , 70 , 70 , 255 )

    GOAL_POINT_COLOR  = QtGui.QColor( 250 , 70 , 70 , 255 )

    EXPLORED_COLOR    = QtGui.QColor( 70 , 70 , 200 , 255 )

    PATH_COLOR        = QtGui.QColor( 0 , 150 , 0 , 255 )

    TEXT_COLOR        = QtGui.QColor( 0 , 200 , 200 , 255 )

    BLANK_STATE      = 0

    WALL_STATE       = 1

    GOAL_POINT_STATE = 2

    EXPLORED_STATE   = 3

    PATH_STATE       = 4

    STATE_MAPPING    = { BLANK_STATE      : BLANK_COLOR      ,
                         WALL_STATE       : WALL_COLOR       ,
                         GOAL_POINT_STATE : GOAL_POINT_COLOR ,
                         EXPLORED_STATE   : EXPLORED_COLOR   ,
                         PATH_STATE       : PATH_COLOR       }

    NON_EXPLORING_STATES = ( WALL_STATE       ,
                             GOAL_POINT_STATE )

    def __init__( self       ,
                  inPosX     ,
                  inPosY     ,
                  inGridSize ):
        '''
        Check if the current word corresponds to current class.

        Args:
            inAAString (string.AAString): AAString to check if it's the current type.

        Returns:
            bool: True if it matches the class, False otherwise.
        '''
        super( AANode , self ).__init__()

        self._gCost     = 0

        self._hCost     = 0

        self._fCost     = 0

        self.parentNode = None

        self._currentState = self.BLANK_STATE

        self.posX     = inPosX
        self.posY     = inPosY
        self.gridGize = inGridSize

        gridOffset = int( self.gridGize / 3 )

        self.textMapping = ( 0              ,
                             gridOffset     ,
                             gridOffset * 2 )

        self.setPos( self.posX ,
                     self.posY )

        self.brush = QtGui.QBrush()
        self.brush.setStyle( QtCore.Qt.SolidPattern )
        self.brush.setColor( self.BLANK_COLOR )

        self.pen = QtGui.QPen()
        self.pen.setStyle( QtCore.Qt.SolidLine )
        self.pen.setWidth( 1 )
        self.pen.setColor( self.BORDER_COLOR )

        self.textPen = QtGui.QPen()
        self.textPen.setStyle( QtCore.Qt.SolidLine )
        self.textPen.setColor( self.TEXT_COLOR )
        self.numberFont = QtGui.QFont( 'Arial'                  ,
                                       int( self.gridGize / 5 ) ,
                                       QtGui.QFont.Normal       )

    def __repr__( self ):
        '''
        String representation

        Returns:
            str: String representation of the node displaying coordinates.
        '''
        return 'AANode at [{0} , {1}]'.format( self.posX ,
                                               self.posY )

    def distanceTo( self   ,
                    inNode ):
        '''
        Calculates the distance to another node.

        Note:
            Based on the rule that diagonal moves are worth .14 * Distance
            while other directions are worth .10 * Distance.

        Args:
            inNode (int): Node to calculate distance to.

        Returns:
            int: Calculated distance value.
        '''

        xDistanceInt = abs( self.posX - inNode.posX )
        yDistanceInt = abs( self.posY - inNode.posY )

        if xDistanceInt > yDistanceInt:
            return int( .14 * yDistanceInt + ( ( xDistanceInt - yDistanceInt ) * .10 ) )
        return int( .14 * xDistanceInt + ( ( yDistanceInt - xDistanceInt ) * .10 ) )

    @property
    def fCost( self ):
        '''
        Calculates the fCost of the node

        Returns:
            int: fCost.
        '''
        if not self.gCost or not self.hCost:
            return 0

        return self.gCost + self.hCost

    @property
    def gCost( self ):
        '''
        Gets the gCost of the node.

        Returns:
            int: gCost.
        '''
        return self._gCost

    @gCost.setter
    def gCost( self        ,
               inCostFloat ):
        '''
        Sets the gCost of the Node

        Args:
            inCostFloat (int): Cost to set to.

        Returns:
            None.
        '''
        self._gCost = inCostFloat
        self.update()

    @property
    def hCost( self ):
        '''
        Gets the hCost of the node.

        Returns:
            int: gCost.
        '''
        return self._hCost

    @hCost.setter
    def hCost( self        ,
               inCostFloat ):
        '''
        Sets the hCost of the Node

        Args:
            inCostFloat (int): Cost to set to.

        Returns:
            None.
        '''
        self._hCost = inCostFloat
        self.update()

    def shape(self):
        '''
        Reimplementation of shape
        '''
        path = QtGui.QPainterPath()
        path.addRect( self.boundingRect() )
        return path

    def boundingRect(self):
        '''
        Reimplementation of boundingRect
        '''
        rect = QtCore.QRect( 0             ,
                             0             ,
                             self.gridGize ,
                             self.gridGize )
        rect = QtCore.QRectF( rect )
        return rect

    def paint(self, painter, option, widget):
        '''
        Reimplementation of the paint method, draw node depending of the current state.

        Returns:
            None: No return value.
        '''
        self.brush.setColor( self.STATE_MAPPING.get( self.currentState ) )

        painter.setBrush(self.brush)

        painter.setPen(self.pen)

        painter.drawRect( 0             ,
                          0             ,
                          self.gridGize ,
                          self.gridGize )

        if False:

            gCostStr = str( self.gCost )
            hCostStr = str( self.hCost )
            fCostStr = str( self.fCost )

            painter.setPen( self.textPen )

            painter.setFont( self.numberFont )

            metrics = QtGui.QFontMetrics(painter.font())
            textWidth = metrics.boundingRect( gCostStr ).width()
            textHeight = metrics.boundingRect( gCostStr ).height()

            xCenter = ( self.gridGize / 2 ) - ( textHeight / 2 )

            gCostRect = QtCore.QRect( xCenter               ,
                                      self.textMapping[ 0 ] ,
                                      textWidth             ,
                                      textHeight            )

            painter.drawText( gCostRect             ,
                              QtCore.Qt.AlignCenter ,
                              gCostStr              )

            metrics = QtGui.QFontMetrics(painter.font())
            textWidth = metrics.boundingRect( hCostStr ).width()
            textHeight = metrics.boundingRect( hCostStr ).height()

            hCostRect = QtCore.QRect( xCenter               ,
                                      self.textMapping[ 1 ] ,
                                      textWidth             ,
                                      textHeight            )


            painter.drawText( hCostRect             ,
                              QtCore.Qt.AlignCenter ,
                              hCostStr              )
            metrics = QtGui.QFontMetrics(painter.font())
            textWidth = metrics.boundingRect( fCostStr ).width()
            textHeight = metrics.boundingRect( fCostStr ).height()

            fCostRect = QtCore.QRect( xCenter               ,
                                      self.textMapping[ 2 ] ,
                                      textWidth             ,
                                      textHeight            )

            painter.drawText( fCostRect             ,
                              QtCore.Qt.AlignCenter ,
                              fCostStr              )

    @property
    def currentState( self ):
        '''
        Gets the current state of the node.

        Returns:
            None.
        '''
        return self._currentState

    @currentState.setter
    def currentState(self          ,
                     inNewStateInt ):
        '''
        Sets the current state of the node and repaints it.

        Args:
            inNewStateInt (int): New state to set to.

        Returns:
            None.
        '''
        self._currentState = inNewStateInt

        # to call paint.
        self.update()

    def switchWallState(self):
        '''
        Switch between a wall or blank node.

        Returns:
            None.
        '''
        if self.currentState == self.BLANK_STATE:
            self.currentState = self.WALL_STATE

        elif self.currentState == self.WALL_STATE:
            self.currentState = self.BLANK_STATE

    def switchGoalPointState(self):
        '''
        Switch between goal or blank state.

        Returns:
            None.
        '''
        if self.currentState == self.GOAL_POINT_STATE:
            self.currentState = self.BLANK_STATE
            return

        self.currentState = self.GOAL_POINT_STATE

    def setToExplored( self ):
        '''
        Set as explored state if not a wall or goal Node.

        Returns:
            None.
        '''
        if self.currentState not in self.NON_EXPLORING_STATES:
             self.currentState = self.EXPLORED_STATE

    def setToPath( self ):
        '''
        Set as path state if not a goal Node.

        Returns:
            None.
        '''
        if self.currentState != self.GOAL_POINT_STATE:
            self.currentState = self.PATH_STATE

    def reset( self ):
        '''
        Reset the attributes of the Node if node is not a wall or a goal.

        Returns:
            None.
        '''
        if self.currentState not in self.NON_EXPLORING_STATES:
            self.currentState = self.BLANK_STATE

        self.gCost        = 0
        self.hCost        = 0
        self.parentNode   = None
