# automatically generated by the FlatBuffers compiler, do not modify

# namespace: OgTeam1PA1

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class DrinksTable(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DrinksTable()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDrinksTable(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # DrinksTable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DrinksTable
    def Cans(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.CansTable import CansTable
            obj = CansTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DrinksTable
    def Bottles(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.BottlesTable import BottlesTable
            obj = BottlesTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def DrinksTableStart(builder):
    builder.StartObject(2)

def Start(builder):
    DrinksTableStart(builder)

def DrinksTableAddCans(builder, cans):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(cans), 0)

def AddCans(builder, cans):
    DrinksTableAddCans(builder, cans)

def DrinksTableAddBottles(builder, bottles):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(bottles), 0)

def AddBottles(builder, bottles):
    DrinksTableAddBottles(builder, bottles)

def DrinksTableEnd(builder):
    return builder.EndObject()

def End(builder):
    return DrinksTableEnd(builder)
