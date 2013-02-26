from __future__ import print_function  # need print func in lambda

"""Hypid - geometry generation and machine control

Hypid is library for generating geometry in FreeCAD and Rhino,
and deriving fabrication instruction for machine control.

[...]

Adding python files to the search path
---------------------------------------
* FreeCAD
  * import sys
  * sys.path.append("path/to/scripts")
* Rhino
  * import rhinoscriptsyntax as rs
  * rs.AddSearchPath("C:\\My Python Scripts")

Running FreeCAD standalone in Ubuntu
------------------------------------
* import sys
* sys.path.append("/usr/lib/freecad/lib/")
* import FreeCAD


"""

import transformations as xf


__author__  = 'Stefan Hechenberger <stefan@nortd.com>'
__version__ = '2013.02'
__license__ = 'GPL3'
__docformat__ = 'restructuredtext en'
__all__ = ['clear_selection', 'get_selected', 'make_line', 'make_circle']



# ############################################################################
# General Implementation

class BaseApp():
    def __init__(self):
        BaseApp.__init__(self)

    # ###########################################
    # implemented in FreeCadApp, and RhinoApp
    def clear_selection(self): pass


class BaseForm():

    def __init__(self):
        self.obj = None

    # ###########################################
    # implemented in FreeCadForm, and RhinoForm
    # Factories
    def get_selected(cls): pass
    def make_line(cls, p1, p2): pass
    def make_circle(cls, p1, p2): pass
    # Document Methods
    def get_active_view(self): pass
    def refresh_view(self): pass
    def view_all(self): pass
    def view_selected(self): pass
    # Selection
    def select(self, ): pass
    def unselect(self): pass
    def is_selected(self): pass
    # Geometry Classification
    def is_line(self): pass
    def is_curve(self): pass
    # Curve Methods
    def length(self): pass
    def value_at(self, param): pass
    def normal_at(self, param): pass
    def tangent_at(self, param): pass
    def curvature_at(self, param): pass
    def center_of_curvature_at(self, param): pass
    def derivative1_at(self, param): pass
    def derivative2_at(self, param): pass
    def derivative3_at(self, param): pass



# ############################################################################
# FreeCAD Implementation

class FreeCadApp(BaseApp):
    def __init(self):
        BaseApp.__init__(self)

    @classmethod
    def clear_selection(self):
        FreeCAD.Gui.Selection.clearSelection()


class FreeCadForm(BaseForm):
    def __init__(self):
        BaseForm.__init__(self)
        self.error = FreeCAD.Console.PrintError
        self.warn = FreeCAD.Console.PrintWarning
        self.log = FreeCAD.Console.PrintLog
        self.message = FreeCAD.Console.PrintMessage


    # ###########################################
    # Factories

    @classmethod
    def get_selected(cls):
        objs = FreeCAD.Gui.Selection.getSelection()
        if objs:
            self = cls()
            self.obj = objs[0]
            return self
        else:
            return None

    @classmethod
    def make_line(cls, p1, p2):
        if type(p1) == list:
            p1 = tuple(p1)
        if type(p2) == list:
            p2 = tuple(p2)
        self = cls()
        self.obj = FreeCAD.ActiveDocument.addObject("Part::Feature","hyLine")
        shape = Part.makeLine(p1, p2)  # Part.TopoShape
        self.obj.Shape = shape
        # self.obj = Part.makeLine(p1, p2)
        # Part.show(self.obj)
        self.message("line made")
        # FreeCAD.Console.PrintMessage("line made")
        return self

    @classmethod
    def make_circle(cls, r):
        self = cls()
        self.obj = FreeCAD.ActiveDocument.addObject("Part::Feature","hyCircle")
        circ = Part.Circle()  # Part.GeomCircle
        circ.Radius = float(r)
        self.obj.Shape = circ.toShape()
        # shape = Part.makeCircle(r)
        # obj.Shape = shape
        return self


    # ###########################################
    # Document Methods

    def get_active_document(self):
        return FreeCAD.ActiveDocument

    def get_object(self, name):
        return FreeCAD.ActiveDocument.getObject(name)

    def get_view_object(self, name):
        """Get the view representation part of the object."""
        return FreeCAD.ActiveDocument.getObject(name).ViewObject

    def get_active_view(self):
        return FreeCAD.Gui.ActiveDocument.ActiveView

    def refresh_view(self):
        FreeCAD.ActiveDocument.recompute()

    def view_all(self):
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")

    def view_selected(self):
        self.error("not implemented")


    # ###########################################
    # Selection

    def select(self, clear_first=False):
        if clear_first:
            clear_selection()
        FreeCAD.Gui.Selection.addSelection(self.obj)

    def unselect(self):
        FreeCAD.Gui.Selection.removeSelection(self.obj)

    def is_selected(self):
        return FreeCAD.Gui.Selection.isSelected(self.obj)


    # ###########################################
    # Geometry Classification

    # def is_line(self):
    #     return self.obj.isDerivedFrom("Part::Feature") and \
    #            self.obj.Shape and self.obj.Shape.isValid()

    def is_curve(self):
        """Is this a single curve."""
        return self.obj.isDerivedFrom("Part::Feature") and \
               self.obj.Shape and self.obj.Shape.isValid() and \
               len(self.obj.Shape.Edges) == 1


    # ###########################################
    # Curve Methods

    def length(self):
        if self.is_curve():
            return self.obj.Shape.Length
        else:
            self.error("not a curve")
            return None

    def value_at(self, param):
        """param: 0 to 1.0"""
        if self.is_curve():
            return self.obj.Shape.Edges[0].valueAt(self.obj.Shape.Length*param)
        else:
            self.error("not a curve")
            return None

    def normal_at(self, param):
        if self.is_curve():
            return self.obj.Shape.Edges[0].normalAt(param)
        else:
            self.error("not a curve")
            return None

    def tangent_at(self, param):
        if self.is_curve():
            return self.obj.Shape.tangentAt(param)
        else:
            self.error("not a curve")
            return None

    def curvature_at(self, param):
        if self.is_curve():
            return self.obj.Shape.curvatureAt(param)
        else:
            self.error("not a curve")
            return None

    def center_of_curvature_at(self, param):
        if self.is_curve():
            return self.obj.Shape.centerOfCurvatureAt(param)
        else:
            self.error("not a curve")
            return None

    def derivative1_at(self, param):
        if self.is_curve():
            return self.obj.Shape.derivative1At(param)
        else:
            self.error("not a curve")
            return None

    def derivative2_at(self, param):
        if self.is_curve():
            return self.obj.Shape.derivative2At(param)
        else:
            self.error("not a curve")
            return None

    def derivative3_at(self, param):
        if self.is_curve():
            return self.obj.Shape.derivative3At(param)
        else:
            self.error("not a curve")
            return None
    

    # ###########################################
    # Transformations

    def transform_shape(self, matrix):
        pass




# ############################################################################
# Rhino Implementation

class RhinoApp(BaseApp):
    def __init__(self):
        BaseApp.__init__(self)

    @classmethod
    def clear_selection(self):
        rs.UnselectAllObjects()


class RhinoForm(BaseForm):
    def __init__(self):
        BaseForm.__init__(self)
        self.error = lambda msg: print("ERROR: " + msg)
        self.warn = lambda msg: print("WARNING: " + msg)
        self.log = lambda msg: print("LOG: " + msg)
        self.message = lambda msg: print("MESSAGE: " + msg)


    # ###########################################
    # Factories

    @classmethod
    def get_selected(cls):
        objs = rs.SelectedObjects()
        if objs:
            self = cls()
            self.obj = objs[0]  # get the first
            return self
        else:
            return None

    @classmethod
    def make_line(cls, p1, p2):
        self = cls()
        self.obj = rs.AddLine(p1, p2)
        return self

    @classmethod
    def make_circle(cls, r):
        self = cls()
        self.obj = rs.AddCircle(rs.WorldXYPlane(), r)
        return self


    # ###########################################
    # Document Methods

    def get_active_view(self):
        return rs.CurrentView()

    def refresh_view(self):
        rs.Redraw()

    def view_all(self):
        rs.ZoomExtents()

    def view_selected(self):
        rs.ZoomSelected()


    # ###########################################
    # Selection

    def select(self, clear_first=False):
        if clear_first:
            clear_selection()
        rs.SelectObjects([self.obj])

    def unselect(self):
        rs.UnselectObjects([self.obj])

    def is_selected(self):
        return rs.IsObjectSelected(self.obj)


    # ###########################################
    # Geometry Classification

    def is_line(self):
        return rs.IsLine(self.obj)

    def is_curve(self):
        return rs.IsCurve(self.obj)


    # ###########################################
    # Curve Methods

    def length(self):
        if self.is_curve():
            return rs.CurveLength(self.obj)
        else:
            self.error("not a curve")
            return None

    def value_at(self, param):
        """param: 0 to 1.0"""
        if self.is_curve():
            domain = rs.CurveDomain(self.obj)
            return rs.EvaluateCurve(obj, domain[1]*param)
        else:
            self.error("not a curve")
            return None

    def normal_at(self, param):
        if self.is_curve() and self.is_planar():
            return rs.CurveNormal(self.obj)
            return self.obj.normalAt(param)
        else:
            self.error("not a curve")
            return None

    def tangent_at(self, param):
        if self.is_curve():
            return self.obj.tangentAt(param)
        else:
            self.error("not a curve")
            return None

    def curvature_at(self, param):
        if self.is_curve():
            return self.obj.curvatureAt(param)
        else:
            self.error("not a curve")
            return None

    def center_of_curvature_at(self, param):
        if self.is_curve():
            return self.obj.centerOfCurvatureAt(param)
        else:
            self.error("not a curve")
            return None

    def derivative1_at(self, param):
        if self.is_curve():
            return self.obj.derivative1At(param)
        else:
            self.error("not a curve")
            return None

    def derivative2_at(self, param):
        if self.is_curve():
            return self.obj.derivative2At(param)
        else:
            self.error("not a curve")
            return None

    def derivative3_at(self, param):
        if self.is_curve():
            return self.obj.derivative3At(param)
        else:
            self.error("not a curve")
            return None




# ############################################################################
# Selecting Implementation (FreeCAD or Rhino)
try:
    import FreeCAD
    import Part
    App = FreeCadApp
    Form = FreeCadForm
except ImportError:
    try:
        import rhinoscript
        import rhinoscriptsyntax as rs
        App = RhinoApp
        Form = RhinoForm
    except ImportError:
        print("Error: wrong context, run in FreeCAD or Rhino")



# ############################################################################
# Aliases of classmethods
# App-level
clear_selection = App.clear_selection
# Factories
get_selected = Form.get_selected
make_line = Form.make_line
make_circle = Form.make_circle