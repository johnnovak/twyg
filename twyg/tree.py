import sys

from twyg.geom import Vector2, Rectangle


class Direction(object):
    Top, Right, Bottom, Left = range(4)


def opposite_dir(d):
    if d == Direction.Bottom:
        return Direction.Top
    if d == Direction.Right:
        return Direction.Left
    if d == Direction.Top:
        return Direction.Bottom
    if d == Direction.Left:
        return Direction.Right
    else:
        raise ValueError, 'Invalid direction: %s' % d


class Node(object):

    def __init__(self, label, parent=None):
        """
        Create a new node and associate it with a parent node. If
        ``parent`` is ``None``, a root node will be created.
        """
        self.label = label
        self.parent = parent
        if parent:
            parent.children.append(self)

        self.children = []
        self.x = 0
        self.y = 0

        # Property name (Python classes) to variable name (config expressions)
        # mappings
        self.property_mappings = {
            'x':               'x',
            'y':               'y',
            'fontsize':        'fontSize',
            'width':           'width',
            'height':          'height',
            'bboxwidth':       'bboxWidth',
            'bboxheight':      'bboxHeight',
            'textwidth':       'textWidth',
            'textheight':      'textHeight',
            'max_text_width':  'maxTextWidth',
            'bgcolor':         'bgColor',
            'basecolor':       'baseColor',
            'fillcolor':       'fillColor',
            'strokecolor':     'strokeColor',
            'connectioncolor': 'connectionColor',
            'fontcolor':       'fontColor',
            'lineheight':      'lineHeight'
        }

    def isleaf(self):
        return len(self.children) == 0

    def isroot(self):
        return self.parent == None

    def depth(self):
        depth = 0
        curr = self
        while curr.parent:
            curr = curr.parent
            depth += 1
        return depth

    def ancestor(self, n):
        """ Get the n-th ancestor of this node.

        If ``n`` is negative, the ancestor is counted from the root node.
        If ``n`` is 0, the root node is returned.
        """

        # If n is positive, get n-th ancestor from the node towards the root
        if n > 0:
            depth = 0
            curr = self
            while curr.parent:
                curr = curr.parent
                depth += 1
                if depth == n:
                    return curr
            raise ValueError, 'Node ancestor argument out of range: ' + n

        # If n is negative or zero, get n-th ancestor from the root
        # towards the node
        if n <= 0:
            curr = self
            ancestors = [curr]
            while curr.parent:
                curr = curr.parent
                ancestors.append(curr)

            if n == 0:
                return ancestors[-1]
            else:
                n -= 1
                if -n > len(ancestors):
                    raise (ValueError,
                          'Node ancestor argument out of range: ' + n)
                return ancestors[n]

    def direction(self):
        """ Get the position of the node in relation to its parent. """
        if self.isroot():
            return None
        if self.x - self.parent.x < 0:
            return Direction.Left
        else:
            return Direction.Right

    def getchildren(self, direction=None):
        if direction:
            return [c for c in self.children
                    if c.direction() == direction]
        else:
            return self.children

    def connection_point(self, direction):
        return self.nodedrawer.drawer.connection_point(self, direction)

    def shiftbranch(self, dx, dy):
        self.x += dx
        self.y += dy
        for child in self.children:
            child.shiftbranch(dx, dy)


class TreeBuilder(object):

    def build_tree(self, tree):
        #TODO proper error handling
        if type(tree) != dict:
            raise ValueError('Invalid JSON structure: Root element must be a dict')

        root = tree.iteritems().next()
        root_label = root[0]
        children = root[1]
        root_node = Node(root_label)
        self._build_tree(root_node, children)
        return root_node

    def _build_tree(self, node, children):
        if type(children) in (str, unicode):
            Node(children, parent=node)
        else:
            for c in children:
                if type(c) == dict:
                    child = Node(c.keys()[0], parent=node)
                    self._build_tree(child, c.values()[0])
                elif type(c) in (list, tuple):
                    #TODO proper error handling
                    raise ValueError('Invalid JSON structure: Dicts cannot have List siblings')
                else:
                    Node(c, parent=node)


class Tree(object):

    def __init__(self, layout, nodedrawers, conndrawers, colorizers, data):
        builder = TreeBuilder()
        self.root = builder.build_tree(data)

        self._nodelist = []
        self._collect_nodes(self.root, self._nodelist)

        self._layout = layout

        self._nodedrawers = nodedrawers
        self._conndrawers = conndrawers
        self._colorizers = colorizers

        # Precalculate the orientation of the nodes before assigning the
        # drawer objects to them. It is important to do this before the
        # assignment would occur, because the section level rules take
        # the nodes' orientation into consideration when determining the
        # correct drawer for them.
        self._layout.precalc_layout(self.root)
        self._assign_drawers()

    def print_tree(self):
        self._print_tree(self.root)

    def calclayout(self):
        for node in self._nodelist:
            node.nodedrawer.drawer.precalc_node(node)

        self._layout.calclayout(self.root)
        self._colorize_nodes(self.root)

        self.bbox = self._calcbbox()
        self.shiftnodes(-self.bbox.x, -self.bbox.y)

        return self.bbox.w, self.bbox.h

    def shiftnodes(self, dx, dy):
        self.root.shiftbranch(dx, dy)

    def draw(self):
        self._draw_connections(self.root)
        self._draw_nodes()

    def background_color(self):
        # The background color for the canvas is always taken from the first
        # colorizer instance.
        return  self._colorizers[0].drawer.background_color()

    def _assign_drawers(self):
        """ Assign the correct drawer objects for each node as specified
        by the section level configurations."""

        for node in self._nodelist:
            for nd in self._nodedrawers:
                if nd.level.selects(node, self._layout):
                    node.nodedrawer = nd

            for cd in self._conndrawers:
                if cd.level.selects(node, self._layout):
                    node.conndrawer = cd

            for c in self._colorizers:
                if c.level.selects(node, self._layout):
                    node.colorizer = c

    def _print_tree(self, node):
        print (" " * node.depth() * 2) + node.label
        for child in node.children:
            self._print_tree(child)

    def _collect_nodes(self, node, nodelist):
        for child in node.children:
            self._collect_nodes(child, nodelist)
        nodelist.append(node)

    def _draw_nodes(self):
        self._nodelist.sort(key=lambda x: x.y, reverse=False)
        for node in self._nodelist:
            node.nodedrawer.drawer.draw(node)
        pass

    def _draw_connections(self, node):
        for node in self._nodelist:
            node.conndrawer.drawer.draw(node)

    def _colorize_nodes(self, node):
        node.colorizer.drawer.colorize(node)
        for child in node.children:
            self._colorize_nodes(child)

    def _calcbbox(self):
        m = sys.maxint
        topleft = Vector2(m, m)
        bottomright = Vector2(-m, -m)
        self._calcbbox_recurse(self.root, topleft, bottomright)
        return Rectangle(topleft.x, topleft.y,
                         bottomright.x - topleft.x, bottomright.y - topleft.y)

    def _calcbbox_recurse(self, node, topleft, bottomright):
        if node.x < topleft.x:
            topleft.x = node.x
        if node.y < topleft.y:
            topleft.y = node.y

        x2 = node.x + node.bboxwidth
        y2 = node.y + node.bboxheight

        if x2 > bottomright.x:
            bottomright.x = x2
        if y2 > bottomright.y:
            bottomright.y = y2

        for child in node.children:
            self._calcbbox_recurse(child, topleft, bottomright)

