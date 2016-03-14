import math, os, sys

from twyg.config import Properties, NumberProperty, BooleanProperty

from twyg.tree import Direction, opposite_dir
from twyg.geomutils import halfcircle


class Layout(object):

    def __init__(self, config):
        properties = {
            'horizontalBalance':       (NumberProperty,  {}),
            'verticalAlignFactor':     (NumberProperty,  {'min': 0.0,
                                                          'max': 1.0}),
            'rootPadX':                (NumberProperty,  {}),
            'nodePadX':                (NumberProperty,  {}),
            'nodePadY':                (NumberProperty,  {}),
            'branchPadY':              (NumberProperty,  {}),
            'sameWidthSiblings':       (BooleanProperty, {}),
            'snapParentToChildren':    (BooleanProperty, {}),
            'snapToHalfPositions':     (BooleanProperty, {}),
            'radialMinNodes':          (NumberProperty,  {'min': 0.0}),
            'radialFactor':            (NumberProperty,  {})
        }

        self._props = Properties(properties, self._defaults_path('layout'),
                                 config)

        self._leftnodes = ()
        self._rightnodes = ()

    # TODO util function in common?
    def _defaults_path(self, conf):
        return os.path.join('layout', conf)

    def _eval_func(self, node=None, direction=None):
        if node:
            vars = {
                'childrenHeight': self.childrenheight(node, direction)
            }
        else:
            vars = {}
        return lambda name: self._props.eval(name, node, vars)

    def precalc_layout(self, root):
        self.root = root
        self._splitnodes()

    def node_orientation(self, node):
        if node.isroot():
            return None
        elif node.ancestor(-1) in self._leftnodes:
            return Direction.Left
        elif node.ancestor(-1) in self._rightnodes:
            return Direction.Right

    def _splitnodes(self):
        """
        Split the first level nodes into left and right directed nodes.
        """

        E = self._eval_func()

        children = self.root.children
        n = int((len(children) + 1) * E('horizontalBalance'))

        self._leftnodes = children[:n]
        self._rightnodes = children[n:]

    def calclayout(self, root):
        self.root = root

        # Vertical layout
        self._leaf_y = 0
        self._branch_pad = False
        self._calc_y(self.root, Direction.Left)

        oy = self.root.y

        self._leaf_y = 0
        self._branch_pad = False
        self._calc_y(self.root, Direction.Right)

        dy = oy - self.root.y

        # Align right side to the left
        self.root.y += dy
        for node in self._rightnodes:
            node.shiftbranch(0, dy)

        # Horizontal layout
        self._calc_child_maxwidth(self.root, Direction.Left)
        self._calc_child_maxwidth(self.root, Direction.Right)
        self._calc_x(self.root, Direction.Left, 0)
        self._calc_x(self.root, Direction.Right, self.root.x)

    def _getchildren(self, node, direction):
        if node.isroot():
            return (self._leftnodes if direction == Direction.Left
                    else self._rightnodes)
        return node.children

    def _calc_child_maxwidth(self, node, direction):
        for child in self._getchildren(node, direction):
            self._calc_child_maxwidth(child, direction)

        p = node.parent
        if not p:
            return
        if not hasattr(p, 'child_bboxwidth_max'):
            p.child_bboxwidth_max = node.bboxwidth
        else:
            p.child_bboxwidth_max = max(p.child_bboxwidth_max, node.bboxwidth)

    def _calc_x(self, node, direction, x):
        E = self._eval_func(node, direction)

        children = self._getchildren(node, direction)

        xpad = E('rootPadX') if node.isroot() else E('nodePadX')

        if E('sameWidthSiblings'):
            if not node.isroot() and not node.isleaf():
                maxwidth = node.parent.child_bboxwidth_max
            else:
                maxwidth = node.bboxwidth
        else:
            maxwidth = node.bboxwidth

        xoffs = 0
        if not node.isroot():
            siblings = self._getchildren(node.parent, direction)
            if len(siblings) >= E('radialMinNodes'):
                _dir = -1 if direction == Direction.Left else 1
                xoffs = halfcircle(0, siblings[0].y, siblings[-1].y,
                                   E('radialFactor'), _dir, node.y)

        if direction == Direction.Left:
            width = node.bboxwidth
            x += xoffs - width
            node.x = x
            x -= xpad + maxwidth - width
        else:
            x += xoffs
            node.x = x
            x += maxwidth + xpad

        for child in children:
            self._calc_x(child, direction, x)

    def _calc_y(self, node, direction):
        E = self._eval_func(node)

        # Initialise branch bounding box
        node._branch_bboxtop = node.y
        node._branch_bboxbottom = node.y + node.bboxheight

        node_pady = E('nodePadY')

        if node.isleaf():
            # Set the position of a leaf node node a calculate the y
            # position for the next leaf. Because of the way we traverse
            # the tree, all leaf nodes are positioned consecutively on
            # the y axis, separated by the node and branch paddings.
            node.y = self._leaf_y
            self._leaf_y += node.bboxheight + node_pady
            self._branch_pad = False
        else:
            # Depth-first traversal: we are going to calculate the
            # layout starting from the leaf nodes, progressing upwards
            # in the tree, and from top to bottom (from lower to higher
            # y coordinates) in terms of vertical positioning
            children = self._getchildren(node, direction)
            if not children:
                return

            branch_pad_y = E('branchPadY')

            if not self._branch_pad:
                self._leaf_y += branch_pad_y - node_pady
                self._branch_pad = True

            for child in children:
                self._calc_y(child, direction)

            if not self._branch_pad:
                self._leaf_y += branch_pad_y - node_pady
                self._branch_pad = True

            # At this point the whole subtree under 'node' has been
            # positioned correctly. The only remainig thing is to
            # calculate the y position of 'node' (the parent).
            node_dir = direction
            child_dir = opposite_dir(node_dir)

            # Calculate the y coord of the connection point for the
            # children
            firstchild = children[0]
            lastchild = children[-1]

            child_conn_ytop = firstchild.connection_point(child_dir)[1]
            child_conn_ybottom = lastchild.connection_point(child_dir)[1]

            # The actual connection point will be in between 
            child_conn_y = (child_conn_ytop
                           + (child_conn_ybottom - child_conn_ytop)
                           * E('verticalAlignFactor'))

            # Snap parent connection position to children connection
            # positions vertically
            if E('snapParentToChildren'):
                children_conn_y = [c.connection_point(child_dir)[1]
                                   for c in children]

                # Enable snapping to half-positions 50% inbetween two
                # child connections
                if E('snapToHalfPositions'):
                    l = []
                    for i in range(len(children_conn_y) - 1):
                        y1 = children_conn_y[i]
                        y2 = children_conn_y[i + 1]
                        l.append(y1)
                        l.append((y1 + y2) / 2.)

                    l.append(children_conn_y[-1])
                    children_conn_y = l

                # Get closest connection point index
                d = [abs(child_conn_y - y) for y in children_conn_y]
                closest = d.index(min(d))

                child_conn_y = children_conn_y[closest]

            # Calculate the y offset of the parent node in relation to
            # it's connection point
            node_conn_y = node.connection_point(node_dir)[1]
            node_yoffs = node_conn_y - node.y

            # Calculate the top and bottom y coords of the parent
            node_ytop = child_conn_y - node_yoffs
            node_ybottom = child_conn_y + (node.bboxheight - node_yoffs)

            # Set the position of the parent node
            node.y = node_ytop

            # Calculate the top and bottom y coords of the children
            children_ytop = firstchild.y
            children_ybottom = lastchild.y + lastchild.bboxheight

            # If the parent extends above the topmost child node, shift
            # the whole branch downwards by the same amount 
            dy_top = children_ytop - node_ytop

            if dy_top > 0:
                if node.isroot():
                    node.y += dy_top
                    for n in self._getchildren(node, direction):
                        n.shiftbranch(0, dy_top)
                else:
                    node.shiftbranch(0, dy_top)
            else:
                dy_top = 0

            # If the parent extends below the bottommost child node,
            # offset the y start the next leaf node by the same amount
            if node_ybottom > children_ybottom:
                y = node_ybottom + branch_pad_y
                if y > self._leaf_y:
                    self._leaf_y = y

            # Adjust y coordinates if the branch has been shifted
            # downwards
            self._leaf_y += dy_top

            node_ytop += dy_top
            node_ybottom += dy_top
            children_bboxtop = firstchild._branch_bboxtop + dy_top
            children_bboxbottom = lastchild._branch_bboxbottom + dy_top

            # Calculate the bounding box of the branch
            node._branch_bboxtop = min(children_bboxtop, node_ytop)
            node._branch_bboxbottom = max(children_bboxbottom, node_ybottom)

    def childrenheight(self, node, direction):
        # direction is None for leaf nodes
        if direction == None:
            return 0

        children = self._getchildren(node, direction)
        if not children or node.isleaf():
            return 0

        firstchild = children[0]
        lastchild = children[-1]

        child_dir = opposite_dir(direction)
        child_conn_ytop = firstchild.connection_point(child_dir)[1]
        child_conn_ybottom = lastchild.connection_point(child_dir)[1]

        return child_conn_ybottom - child_conn_ytop


_layout_map = {
    'layout': Layout
}


def layout_by_name(name):
    if name in _layout_map:
        return _layout_map[name]
    else:
        raise ValueError, 'Unrecognized layout name: %s' % name

