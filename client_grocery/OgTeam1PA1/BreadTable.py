# automatically generated by the FlatBuffers compiler, do not modify

# namespace: OgTeam1PA1

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class BreadTable(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BreadTable()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsBreadTable(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # BreadTable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BreadTable
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # BreadTable
    def Quantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def BreadTableStart(builder):
    builder.StartObject(2)

def Start(builder):
    BreadTableStart(builder)

def BreadTableAddType(builder, type):
    builder.PrependInt32Slot(0, type, 0)

def AddType(builder, type):
    BreadTableAddType(builder, type)

def BreadTableAddQuantity(builder, quantity):
    builder.PrependFloat32Slot(1, quantity, 0.0)

def AddQuantity(builder, quantity):
    BreadTableAddQuantity(builder, quantity)

def BreadTableEnd(builder):
    return builder.EndObject()

def End(builder):
    return BreadTableEnd(builder)