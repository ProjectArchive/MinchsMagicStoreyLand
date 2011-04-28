"""UML diagrams for Python

Lumpy generates UML diagrams (currently object and class diagrams)
from a running Python program. It is similar to a graphical debugger
in the sense that it generates a visualization of the state of a
running program, but it is different from a debugger in the sense that
it tries to generate high-level visualizations that are compliant (at
least in spirit) with standard UML.

There are three target audiences for this module: teachers, students
and software engineers. Teachers can use Lumpy to generate figures
that demonstrate a model of the execution of a Python
program. Students can use Lumpy to explore the behavior of the Python
interpreter. Software engineers can use Lumpy to extract the structure
of existing programs by diagramming the relationships among the
classes, including classes defined in libraries and the Python
interpreter.


  Copyright 2005 Allen B. Downey

    This file contains wrapper classes I use with tkinter.  It is
    mostly for my own use; I don't support it, and it is not very
    well documented.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see
    http://www.gnu.org/licenses/gpl.html or write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
    02110-1301 USA
    
"""



import inspect, traceback
from Gui import *
from string import lower

# most text uses the font specified below; some labels
# in object diagrams use smallfont.  Lumpy uses the size
# of the fonts to define a length unit, so
# changing the font sizes will cause the whole diagram to
# scale up or down.
font = ("Helvetica", 8)
smallfont = ("Helvetica", 6)

def underride(d, **kwds):
    """Add kwds to the dictionary only if they are not already set"""
    for key, val in kwds.iteritems():
        if key not in d:
            d[key] = val

def append_elt(obj, attr, elt):
    """append elt to obj[attr] if it exists, otherwise create it"""
    obj.__dict__.setdefault(attr, []).append(elt)
    

class DiagCanvas(GuiCanvas):
    """a Canvas for displaying Diagrams
    """
    def box(self, box, padx=0.5, pady=0.3, **options):
        """draw a rectangle with the given bounding box, expanded
        by padx and pady.  box can be a Bbox object or a list of
        two coordinate pairs.
        """
        underride(options, outline='black')
        box.left -= padx
        box.top -= pady
        box.right += padx
        box.bottom += pady
        item = self.rectangle(box, **options)
        return item

    def arrow(self, start, end, **options):
        """draw an arrow: start and end can be a Pos object or
        a list of two coordinates
        """
        # Lumpy arrows used to really have arrows, but at the moment
        # they are just lines.  That's why the next line is commented out.
        # underride(options, arrow=LAST)
        return self.line([start, end], **options)

    def str(self, pos, text, dx=0, dy=0, **options):
        """draw the given text at the given position, with an offset
        specified by dx and dy
        """
        underride(options, fill='black', font=font, anchor=W)
        x, y = pos
        x += dx
        y += dy
        return self.text([x, y], text, **options)
        
    def dot(self, pos, r=0.2, **options):
        """draw a dot at the given position with radius r
        """
        underride(options, fill='white', outline='orange')
        x, y = pos
        return self.circle(x, y, r, **options)
        
    def measure(self, t, **options):
        """find the bounding box of the list of words by
        drawing them, measuring them, and then deleting them
        """
        pos = Pos([0,0])
        tags = 'temp'
        for s in t:
            self.str(pos, s, tags=tags, **options)
            pos.y += 1
        bbox = self.bbox(tags)
        self.delete(tags)
        return bbox
    

nextid = 0
def make_tags(prefix='Tag'):
    """return a tuple with a single element: a tag string with
    with the given prefix and a unique id as a suffix
    """
    global nextid
    nextid += 1
    id = '%s%d' % (prefix, nextid)
    return id,


class Thing(object):
    """the parent class for objects that have a graphical
    representation.  Each Thing object corresponds to an item
    or set of items in a diagram.  A thing can only be drawn in
    one Diagram at a time.
    """
    things_created = 0
    things_drawn = 0

    def __new__(cls, *args, **kwds):
        Thing.things_created += 1
        return object.__new__(cls, *args, **kwds)
    
    def bbox(self):
        """return the bounding box of this object if it is drawn
        """
        return self.canvas.bbox(self.tags)
    
    def set_offset(self, pos):
        """the offset attribute keeps track of the offset between
        the bounding box of the Thing and its nominal position, so
        that if the Thing is moved later, we can compute its new
        nominal position.
        """
        self.offset = self.bbox().offset(pos)

    def pos(self):
        """Compute the nominal position of a Thing by getting the
        current bounding box and adding the offset.
        """
        return self.bbox().pos(self.offset)

    def draw(self, diag, pos, flip, tags=tuple()):
        """draw this Thing at the given position on the given
        diagram with the given tags (in addition to the specific
        tag for this thing).  flip=1 means draw left to right;
        flip=-1 means right to left.  Return True if the Thing
        was already drawn, False otherwise.

        draw and drawme are not allowed to mofify pos
        """
        if isdrawn(self):
            return True
        self.drawn = True
        self.diag = diag
        self.canvas = diag.canvas

        # keep track of how many things have been drawn.
        # Simple values can get drawn more than once, so the
        # total number of things drawn can be greater than
        # the number of things.
        Thing.things_drawn += 1
        if Thing.things_drawn % 100 == 0:
            print Thing.things_drawn

        # each thing has a list of tags: its own tag plus
        # the tag of each thing it belongs to.  This convention
        # makes it possible to move entire structures with one
        # move command.
        self.tags = make_tags(self.__class__.__name__)
        tags += self.tags

        # invoke drawme in the child class
        self.drawme(diag, pos, flip, tags)
        self.set_offset(pos)
        return False

    def bind(self, tags=None):
        """create bindings for each of the items with the given tags
        """
        tags = tags or self.tags
        items = self.canvas.find_withtag(tags)
        for item in items:
            self.canvas.tag_bind(item, "<Button-1>", self.down)

    def down(self, event):
        """this callback is invoked when the user clicks on an item
        """
        self.dragpos = self.canvas.invert([event.x, event.y])
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<ButtonRelease-1>", self.up)
        return True

    def motion(self, event):
        """this callback is invoked when the user drags an item"""
        newpos = self.canvas.invert([event.x, event.y])
        dx = newpos.x - self.dragpos.x
        dy = newpos.y - self.dragpos.y
        self.canvas.move(self.tags, dx, dy)
        self.dragpos = newpos
        self.diag.update_arrows()
  
    def up(self, event):
        """this callback is invoked when the user releases the button"""
        event.widget.unbind ("<B1-Motion>")
        event.widget.unbind ("<ButtonRelease-1>")
        self.diag.update_arrows()


def isdrawn(thing):
    """return True if the object has been drawn"""
    return hasattr(thing, 'drawn')

class Dot(Thing):
    """the Thing that represents a dot in a diagram"""
    def drawme(self, diag, pos, flip, tags=tuple()):
        self.canvas.dot(pos, tags=tags)



class Simple(Thing):
    """the graphical representation of a simple value like a number
    or a string"""
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        self.val = str(val)

    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()
        p.x += 0.3 * flip        
        anchor = {1:W, -1:E}
        self.canvas.str(p, self.val, tags=tags, anchor=anchor[flip])
        self.bind()


class Mapping(list, Thing):
    """the graphical representation of a mapping type,
    imlemented as a list of Bindings
    """
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        seq = make_bindings(lumpy, val.items())
        list.__init__(self, seq)
        self.label = ''
        self.boxoptions = dict(outline='purple')

    def bbox(self):
        """the bbox of a Mapping is the bbox of its box item.
        This is different from other Things.
        """
        return self.canvas.bbox(self.boxitem)

    def drawme(self, diag, pos, flip, tags=tuple()):
        """drawme is the middle part of the way objects are drawn.
        Thing.draw does some prep work, invokes drawme, and then
        does some cleanup.  draw and drawme are not allowed to
        modify pos.
        """
        p = pos.copy()

        # intag is attached to items that should be considered
        # inside the box
        intag = self.tags[0] + 'inside'

        # draw the bindings
        for binding in self:
            # check whether the key was already drawn
            drawn = isdrawn(binding.key)

            # draw the binding
            binding.draw(diag, p, flip, tags=tags)

            # apply intag to the dots 
            self.canvas.addtag_withtag(intag, binding.dot.tags)
            if drawn:
                # if the key was already drawn, then the binding
                # contains two dots, so we should add intag to the
                # second one.
                self.canvas.addtag_withtag(intag, binding.dot2.tags)
            else:
                # if the key wasn't drawn yet, it should be
                # considered inside this mapping
                self.canvas.addtag_withtag(intag, binding.key.tags)

            # move down to the position for the next binding
            p.y = binding.bbox().bottom + 1.8

        if len(self):
            # if there are any bindings, draw a box around them
            bbox = self.canvas.bbox(intag)
            item = self.canvas.box(bbox, tags=tags, **self.boxoptions)
        else:
            # otherwise just draw a box
            bbox = BBox([p.copy(), p.copy()])
            item = self.canvas.box(bbox, padx=0.4, pady=0.4, tags=tags,
                              **self.boxoptions)

        # make the box clickable
        self.bind(item)
        self.boxitem = item

        # put the label above the box
        if self.label:
            p = bbox.upperleft()
            item = self.canvas.str(p, self.label, anchor=SW,
                              font=smallfont, tags=tags)
            # make the label clickable
            self.bind(item)

        # if the whole mapping is not in the right position, shift it.
        if flip == 1:
            dx = pos.x - self.bbox().left
        else:
            dx = pos.x - self.bbox().right
        self.canvas.move(self.tags, dx, 0)

def addtag(canvas, oldtag, newtag):
    """for each item on the canvas with oldtag, apply newtag
    """
    canvas.addtag_withtag(newtag, oldtag)



class Sequence(Mapping):
    """the graphical representation of a sequence type,
    implemented as a list of Bindings"""
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        seq = make_bindings(lumpy, enumerate(val))
        list.__init__(self, seq)
        self.label = ''

        # color code lists, tuples, and other sequences
        if isinstance(val, list):
            self.boxoptions = dict(outline='green1')
        elif isinstance(val, tuple):
            self.boxoptions = dict(outline='green3')
        else:
            self.boxoptions = dict(outline='green2')
            

def iscallable(obj):
    """Teturn true if this object as a __call__ method
    """
    return hasattr(obj, '__call__')


class Class(Thing):
    """a graphical representation of a Class as it appears
    in a Class Diagram (which is different from the way class
    objects appear in Object Diagrams.
    """
    def __new__(cls, lumpy, classobj, *args, **kwds):
        """cls is the class we are instantiating (Class),
        classobj is the class object we are creating a Class
        to represent.  If there is already a Class for
        classobj, return the existing Class object.  Otherwise
        instantiate a new one.
        """
        if not classobj in lumpy.classes:
            lumpy.classes[classobj] = object.__new__(cls)
        return lumpy.classes[classobj]
    
    def __init__(self, lumpy, classobj):
        """initialize a new Class object to represent classobj.
        """
        if hasattr(self, 'classobj'):
            return
        
        self.classobj = classobj
        self.lumpy = lumpy
        self.name = classobj.__name__
        self.bases = classobj.__bases__

        # childs is the list of classes that inherit directly
        # from this one; parents is the list of base classes
        # for this one
        self.childs = []
        self.parents = [Class(lumpy, base) for base in self.bases]
        for parent in self.parents:
            parent.register(self)

        # methods is the list of methods defined in this class.
        # attrs is the list of attributes a member of this class
        # has, including members that are initialized in parent
        # classes.

        # note: the attributes for a given class are based on
        # a single instance of the class.  If not all members
        # of the class have the same attributes, this list might
        # be incomplete.

        try:
            vars = lumpy.instance_vars[classobj]
        except KeyError:
            vars = None
        
        self.methods = []
        self.attrs = []
        for key, val in classobj.__dict__.items():
            if vars != None and key not in vars: continue
            
            if iscallable(val):
                self.methods.append(val)
            else:
                self.attrs.append(key)

        self.methods.sort()
        self.attrs.sort()

        # height and depth are used to lay out the tree
        self.height = None
        self.depth = None
        
        self.boxoptions = dict(outline='blue')
        self.lineoptions = dict(fill='blue')

    def register(self, child):
        """when a subclass is created, it notifies its parent
        classes, who update their list of children"""
        self.childs.append(child)

    def set_height(self):
        """compute the maximum height between this class and
        a leaf class (one with no children)
        """
        if self.height != None:
            return
        if not self.childs:
            self.height = 0
            return
        for child in self.childs:
            child.set_height()
            
        heights = [child.height for child in self.childs]
        self.height = max(heights) + 1

    def set_depth(self):
        """compute the maximum depth between this class and
        a root class (one with no parents)
        """
        if self.depth != None:
            return
        if not self.parents:
            self.depth = 0
            return
        for parent in self.parents:
            parent.set_depth()
            
        depths = [parent.depth for parent in self.parents]
        self.depth = max(depths) + 1

    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()

        # draw the name of the class
        item = self.canvas.str(p, self.name, tags=tags)
        p.y += 0.8

        # in order to draw lines between segments, we have
        # to store the locations and draw the lines, later,
        # when we know the location of the box
        lines = []

        # draw a line between the name and the methods
        if self.methods:
            lines.append(p.y)
            p.y += 1

        # draw the methods
        for f in self.methods:
            item = self.canvas.str(p, f.__name__, tags=tags)
            p.y += 1

        # draw a line between the methods and the attributes
        if self.attrs:
            lines.append(p.y)
            p.y += 1

        # draw the attributes
        for a in self.attrs:
            item = self.canvas.str(p, a, tags=tags)
            p.y += 1

        # draw the box
        bbox = self.bbox()
        item = self.canvas.box(bbox, tags=tags, **self.boxoptions)
        self.boxitem = item

        # draw the lines
        for y in lines:
            coords = [[bbox.left, y], [bbox.right, y]]
            item = self.canvas.line(coords, tags=tags, **self.lineoptions)

        # only the things we have drawn so far should be bound
        self.bind()

        # draw the descendents of this class
        if self.childs:
            q = pos.copy()
            q.x = bbox.right + 16
            self.diag.draw_classes(self.childs, q, tags)
            self.head = self.arrow_head(diag, bbox, tags)

            # connect this class to its children
            for child in self.childs:
                a = ParentArrow(self.lumpy, self, child)
                self.diag.add_arrow(a)

        # if the class is not in the right position, shift it.
        dx = pos.x - self.bbox().left
        self.canvas.move(self.tags, dx, 0)

    def arrow_head(self, diag, bbox, tags, size=0.5):
        """draw the hollow arrow head that connects this class
        to its children.
        """
        x, y = bbox.midright()
        x += 0.1
        coords = [[x, y], [x+size, y+size], [x+size, y-size], [x, y]]
        item = self.canvas.line(coords, tags=tags, **self.lineoptions)
        return item


class Instance(Mapping):
    """The graphical representation of a frame,
    implemented as a list of Bindings.  Anything with a __dict__
    is treated as an Instance.
    """
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        try:
            class_or_type = val.__class__
            Class(lumpy, class_or_type)
        except AttributeError:
            class_or_type = type(val)

        self.label = class_or_type.__name__

        # if this class is from an opaque module, it's opaque
        if class_or_type.__module__ in lumpy.opaque_modules:
            seq = []

        elif class_or_type in lumpy.instance_vars:
            # if the class is in the list, only display the
            # unrestricted instance variables
            ks = lumpy.instance_vars[class_or_type]
            seq = [Binding(lumpy, Simple(lumpy, k), getattr(val, k))
                   for k in ks]
        else:
            # otherwise, display the instance variables
            if hasdict(val):
                iter = val.__dict__.items()
            elif hasslots(val):
                iter = [(k, getattr(v, k)) for k in val.__slots__]
            else:
                raise Error, "this shouldn't happen"
            
            seq = [Binding(lumpy, Simple(lumpy, k), v)
                       for k, v in iter]

            # and if the object extends list, tuple or dict,
            # append the items
            if isinstance(val, (list, tuple)):
                seq += make_bindings(lumpy, enumerate(val))

            if isinstance(val, dict):
                seq += make_bindings(lumpy, val.items())

        attr = '__name__'
        if hasattr(val, attr):
            seq += [Binding(lumpy, Simple(lumpy, attr), val.__name__)]

        list.__init__(self, seq)
        self.boxoptions = dict(outline='red')


def hasdict(obj): return hasattr(obj, '__dict__')
def hasslots(obj): return hasattr(obj, '__slots__')

class Frame(Mapping):
    """The graphical representation of a frame,
    implemented as a list of Bindings"""
    def __init__(self, lumpy, frame):
        seq = [Binding(lumpy, Simple(lumpy, k), v)
               for k, v in frame.iteritems()]
        list.__init__(self, seq)
        self.label = frame.func
        self.boxoptions = dict(outline='blue')
    

def make_thing(lumpy, val):
    """Return a Thing object corresponding to this value
    """
    # if we're being pedantic, then we always show aliased
    # values
    if lumpy.pedantic:
        thing = lumpy.lookup(val)
        if thing != None: return thing

    # otherwise for simple immutable types, ignore aliasing and
    # just draw
    simple = (bool, int, long, float, complex, NoneType)
    if isinstance(val, simple):
        thing = Simple(lumpy, val)
        return thing
    if isinstance(val, str):
        thing = Simple(lumpy, "'%s'" % val[:20])
        return thing

    # now check for aliasing even if we're not pedantic
    thing = lumpy.lookup(val)
    if thing != None: return thing

    # check the type of the value and dispatch accordingly
    if hasattr(val, '__dict__') or hasattr(val, '__slots__'):
        thing = Instance(lumpy, val)
    elif isinstance(val, (list, tuple)):
        thing = Sequence(lumpy, val)
    elif isinstance(val, dict):
        thing = Mapping(lumpy, val)
    else:
        # print "Couldn't classify", val
        thing = Simple(lumpy, val)

    return thing



class Binding(Thing):
    """the graphical representation of the binding between a
    key and a value.
    """
    def __init__(self, lumpy, key, val):
        lumpy.register(self, (key, val))
        if isinstance(key, Simple):
            self.key = key
        else:
            self.key = make_thing(lumpy, key)
        self.vals = [make_thing(lumpy, val)]

    def rebind(self, val):
        self.val.append(val)

    def drawme(self, diag, pos, flip, tags=tuple()):
        self.dot = Dot()
        self.dot.draw(diag, pos, flip, tags=tags)
        
        p = pos.copy()
        p.x -= 0.3 * flip

        if isinstance(self.key, Simple):
            self.key.draw(diag, p, -flip, tags=tags)
            self.bind()
        else:
            p.x -= 0.5 * flip
            self.dot2 = Dot()
            self.dot2.draw(diag, p, -flip, tags=tags)

            # only the things we have drawn so far should
            # be handles for this binding
            self.bind()
            
            drawn = isdrawn(self.key)
            if not drawn:
                p.x -= 2.5 * flip
                self.key.draw(diag, p, -flip, tags=tags)
            a = Arrow(self.lumpy, self.dot2, self.key, fill='orange')
            diag.add_arrow(a)

        p = pos.copy()
        p.x += 2.5 * flip

        for val in self.vals:
            val.draw(diag, p, flip, tags=tags)
            a = Arrow(self.lumpy, self.dot, val, fill='orange')
            diag.add_arrow(a)
            p.y += 1

#        bbox = self.bbox()
#        d = pos.y - bbox.top
#        if d > 1.5:
#            dy = d - 1.0
#            self.canvas.move(self.tags, 0, dy)

class Arrow(Thing):
    def __init__(self, lumpy, key, val, **options):
        self.lumpy = lumpy
        self.key = key
        self.val = val
        self.options = options
        
    def draw(self, diag):
        self.canvas = diag.canvas
        self.item = self.canvas.arrow(self.key.pos(), self.val.pos(),
                                 **self.options)
        self.canvas.lower(self.item)

    def update(self):
        if not hasattr(self, 'canvas'): return
        self.canvas.coords(self.item, [self.key.pos(), self.val.pos()])


class ParentArrow(Arrow):
    def __init__(self, lumpy, parent, child, **options):
        self.lumpy = lumpy
        self.parent = parent
        self.child = child
        self.options = options
        
    def draw(self, diag):
        self.diag = diag
        parent, child = self.parent, self.child
        
        canvas = diag.canvas
        bbox = canvas.bbox(parent.head)
        p = bbox.midright()
        q = canvas.bbox(child.boxitem).midleft()
        midx = (p.x + q.x) / 2.0
        m1 = [midx, p.y]
        m2 = [midx, q.y]
        coords = [p, m1, m2, q]
        self.item = canvas.line(coords, **self.options)
        canvas.lower(self.item)

    def update(self):
        if not hasattr(self, 'diag'): return
        self.diag.canvas.delete(self.item)
        self.draw(self.diag)



def make_bindings(lumpy, iterator):
    """return alist of bindings, one for each key-value pair
    in iterator
    """
    seq = [Binding(lumpy, k, v) for k, v in iterator]
    return seq


class Stack(Thing):
    """The graphical representation of a stack,
    implemented as a list of Frames
    """
    def __init__(self, lumpy, snapshot):
        self.lumpy = lumpy
        self.seq = [Frame(lumpy, frame) for frame in snapshot]
    
    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()
        
        for frame in self.seq:
            frame.draw(diag, p, flip, tags=tags)
            bbox = self.bbox()
            #p.y = bbox.bottom + 3
            p.x = bbox.right + 3

        
class Snapframe(dict):
    """the data structure that represents a frame"""
    def __init__(self, tup):
        frame, filename, lineno, self.func, lines, index = tup
        (self.arg_names,
         self.args,
         self.kwds,
         locals) = inspect.getargvalues(frame)
        if self.func == '?':
            self.func = '__main__'
        dict.__init__(self, locals)

    def subtract(self, other):
        for key in other:
            try:
                del self[key]
            except KeyError:
                print key

class Snapshot(list):
    """the data structure that represents a stack"""

    def __init__(self):
        """convert from the format returned by inspect
        to a list of frames
        """
        st = inspect.stack()
        frames = [Snapframe(tup) for tup in st[2:]]
        frames.reverse()
        list.__init__(self, frames)

    def spew(self):
        """print the frames in this snapshot"""
        for frame in self:
            print frame.func, frame

    def clean(self, ref):
        """Remove all the variables in the reference stack from self"""
        f1 = self[0]
        f2 = ref[0]
        f1.subtract(f2)
                    

class Lumpy(Gui):
    """the Lumpy object represents the GUI window.
    """
    def __init__(self, debug=False, pedantic=False):
        Gui.__init__(self, debug)
        self.pedantic = pedantic
        self.withdraw()
        self.od = None
        self.cd = None
        self.stack = None

        self.instance_vars = {}

        # when lumpy is traversing the
        # object graph, it will treat any object from an opaque
        # module as opaque
        self.opaque_modules = []

        # an instance of an opaque class is shown with a small empty box;
        # the contents are not shown.
        self.opaque_class(Lumpy)
        self.opaque_class(Gui)
        self.opaque_class(Tk)
        self.opaque_class(Misc)
        self.opaque_class(Wm)
        self.opaque_class(DiagCanvas)
        self.opaque_class(ObjectDiagram)
        self.opaque_class(ClassDiagram)
        self.opaque_class(Snapframe)

        # by default, class objects and module objects are opaque
        clsobj = type(Lumpy)
        self.opaque_class(clsobj)
        modtype = type(inspect)
        self.opaque_class(modtype)

        # the __class__ of a new-style object is a type object.
        # when type objects are drawn, show only the __name__
        self.opaque_class(type)

        # any object that belongs to a class in the Tkinter module
        # is opaque
        self.opaque_module('Tkinter')
 
    def restrict_class(self, class_or_type, vars=None):
        if vars == None: vars = []
        self.instance_vars[class_or_type] = vars

    opaque_class = restrict_class

    def transparent_class(self, class_or_type):
        """remove the given type or class from the dictionary, which
        means that it's attributes will be shown.  If it is not in
        the dictionary, raise an exception."""
        del self.instance_vars[class_or_type]
        
    def opaque_module(self, module_name):
        self.opaque_modules.append(module_name)

    def make_reference(self):
        self.ref = Snapshot()

    def register(self, thing, val):
        thing.lumpy = self
        self.values[id(val)] = thing
    
    def lookup(self, val):
        vid = id(val)
        return self.values.get(vid, None)

    def object_diagram(self, obj=None):
        self.values = {}
        self.classes = {}
        if obj:
            thing = make_thing(self, obj)
        else:
            self.snapshot = Snapshot()
            self.snapshot.clean(self.ref)
            self.stack = Stack(self, self.snapshot)
            thing = self.stack
        #print Thing.things_created
        
        if self.od:
            self.od.clear()
        else:
            self.od = ObjectDiagram(self)

        self.od.draw(thing)
        self.od.draw_arrows()
        
        self.mainloop()

    def class_diagram(self, classes=None):
        if self.stack == None:
            self.make_stack()
        
        if self.cd:
            self.cd.clear()
        else:
            self.cd = ClassDiagram(self, classes)
        self.cd.draw()
        self.mainloop()

class Diagram(object):
    """the class that encapsulates a diag window."""

    def __init__(self, lumpy, ref=None):
        """create a new Diagram.
        If a Gui object is provided, use it to create a new Toplevel
        window.  Otherwise create a Gui.  If ref is true, take a
        reference snapshot of the program state.
        """
        self.lumpy = lumpy
        self.tl = lumpy.tl()
        self.tl.title(self.title)
        self.tl.geometry('+0+400')
        self.tl.protocol("WM_DELETE_WINDOW", self.close)
        self.setup()

        self.stack = None
        self.ref = ref or Snapshot()

    def ca(self, *args, **options):
        """make a canvas for the self"""
        underride(options, fill=BOTH, expand=1, sticky=N+S+E+W)
        return self.lumpy.widget(DiagCanvas, *args, **options)
        
    def setup(self):
        """create the gui for the diagram"""

        # push the frame for the toplevel window
        self.lumpy.pushfr(self.tl)

        # the frame at the top contains buttons
        self.lumpy.fr(expand=0, bg='white')
        self.lumpy.bu(LEFT, text='Close', command=self.close)
        self.lumpy.bu(LEFT, text='Print to file:', command=self.printfile)
        self.en = self.lumpy.en(LEFT, width=10, text='lumpy.ps')
        self.lumpy.endfr()

        # the grid contains the canvas and scrollbars
        self.lumpy.gr(2)
        
        self.ca_width = 1000
        self.ca_height = 500
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white', transforms=[])

        yb = self.lumpy.sb(command=self.canvas.yview, sticky=N+S)
        xb = self.lumpy.sb(command=self.canvas.xview, orient=HORIZONTAL,
                         sticky=E+W)
        self.canvas.configure(xscrollcommand=xb.set, yscrollcommand=yb.set,
                              scrollregion=(0, 0, 800, 800))
        
        self.lumpy.endgr()

        # measure some sample letters to get the text height
        # and set the scale factor for the canvas accordingly
        bbox = self.canvas.measure(['bdfhklgjpqy'])
        self.unit = 1.0 * bbox.height()
        transform = ScaleTransform([self.unit, self.unit])
        self.canvas.add_transform(transform)
        
        self.lumpy.popfr()

    def printfile(self):
        filename = self.en.get()
        bbox = self.canvas.bbox(ALL)
        width=bbox.right*self.unit
        height=bbox.bottom*self.unit
        self.canvas.config(width=width, height=height)
        self.canvas.dump(filename)
        self.canvas.config(width=self.ca_width, height=self.ca_height)

    def close(self):
        self.tl.withdraw()
        self.lumpy.quit()

    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    def draw_arrows(self):
        for arrow in self.arrows:
            arrow.draw(self)

    def update_arrows(self, n=None):
        i = 0
        for arrow in self.arrows:
            arrow.update()
            i += 1
            if n and i>n: break





class ObjectDiagram(Diagram):
    """the class that encapsulates a diag window."""

    """instance_vars maps from a class to the list of attribute
    names that will be drawn for that class.  An opaque class
    is one that maps to an empty list.
    """
    def __init__(self, lumpy=None, ref=None):
        self.title = 'Object Diagram'
        Diagram.__init__(self, lumpy, ref)
        self.arrows = []
        self.stack = None

    def draw(self, thing):
        """draw the given snapshot, if provided, or make
        one if necessary.
        """
        # draw the current stack
        thing.draw(self, Pos([2,2]), flip=1)

        # configure the scroll region
        bbox = Canvas.bbox(self.canvas, ALL)
        self.canvas.configure(scrollregion=bbox)
        #self.canvas.configure(scrollregion=(0, 0, bbox[2], bbox[3]))

    def clear(self):
        self.arrows = []
        self.tl.deiconify()
        self.canvas.delete(ALL)

    def update_snapshot(self, snapshot):
        pass


class ClassDiagram(Diagram):
    """the class that encapsulates a diag window."""

    def __init__(self, lumpy=None, classes=None, ref=None):
        """create a new ClassDiagram.
        """
        self.title = 'Object Diagram'
        Diagram.__init__(self, lumpy, ref)
        self.classes = classes
        self.arrows = []


    def draw(self):
        pos = Pos([2,2])
        
        if self.classes == None:
            classes = self.lumpy.classes.values()
        else:
            classes = [Class(self.lumpy, cls) for cls in self.classes]

        roots = [c for c in classes if c.parents == []]
        for root in roots:
            root.set_height()

        leafs = [c for c in classes if c.childs == []]
        for leaf in leafs:
            leaf.set_depth()

        self.draw_classes(roots, pos)
        self.draw_arrows()

        # configure the scroll region
        bbox = Canvas.bbox(self.canvas, ALL)
        self.canvas.configure(scrollregion=bbox)

        
    def draw_classes(self, classes, pos, tags=tuple()):
        p = pos.copy()
        for c in classes:
            c.draw(self, p, tags)
            bbox = c.bbox()
            p.y = bbox.bottom + 2


    def draw_arrows(self):
        for arrow in self.arrows:
            arrow.draw(self)
            continue
        

###########################
# test code below this line
###########################

def main(script, *args, **kwds):
    class Cell:
        def __init__(self, car=None, cdr=None):
            self.car = car
            self.cdr = cdr

        def __hash__(self):
            return hash(self.car) ^ hash(self.cdr)

    def func_a(x):
        t = [1, 2, 3]
        t.append(t)
        y = None
        z = 1L
        long_name = 'allen'
        d = dict(a=1, b=2)

        func_b(x, y, t, long_name)

    def func_b(a, b, s, name):
        d = dict(a=1, b=(1,2,3))
        cell = Cell()
        cell.car = 1
        cell.cdr = cell
        func_c()

    def func_c():
        t = (1, 2)
        c = Cell(1, Cell())
        d = {}
        d[c] = 7
        d[7] = t
        d[t] = c.cdr
        diag.draw_stack()

    diag = ClassDiagram()
    func_a(17)
    #func_c()
    #diag.draw_stack()
    diag.gui.mainloop()
    

if __name__ == '__main__':
    main(*sys.argv)
