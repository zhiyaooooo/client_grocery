# automatically generated by the FlatBuffers compiler, do not modify

# namespace: OgTeam1PA1

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class OrderMessageTable(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = OrderMessageTable()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsOrderMessageTable(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # OrderMessageTable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # OrderMessageTable
    def Veggies(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.VeggiesTable import VeggiesTable
            obj = VeggiesTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OrderMessageTable
    def Drinks(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.DrinksTable import DrinksTable
            obj = DrinksTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OrderMessageTable
    def Milk(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from OgTeam1PA1.MilkTable import MilkTable
            obj = MilkTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OrderMessageTable
    def MilkLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # OrderMessageTable
    def MilkIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # OrderMessageTable
    def Bread(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from OgTeam1PA1.BreadTable import BreadTable
            obj = BreadTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OrderMessageTable
    def BreadLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # OrderMessageTable
    def BreadIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

    # OrderMessageTable
    def Meat(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from OgTeam1PA1.MeatTable import MeatTable
            obj = MeatTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OrderMessageTable
    def MeatLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # OrderMessageTable
    def MeatIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

def OrderMessageTableStart(builder):
    builder.StartObject(5)

def Start(builder):
    OrderMessageTableStart(builder)

def OrderMessageTableAddVeggies(builder, veggies):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(veggies), 0)

def AddVeggies(builder, veggies):
    OrderMessageTableAddVeggies(builder, veggies)

def OrderMessageTableAddDrinks(builder, drinks):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(drinks), 0)

def AddDrinks(builder, drinks):
    OrderMessageTableAddDrinks(builder, drinks)

def OrderMessageTableAddMilk(builder, milk):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(milk), 0)

def AddMilk(builder, milk):
    OrderMessageTableAddMilk(builder, milk)

def OrderMessageTableStartMilkVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartMilkVector(builder, numElems: int) -> int:
    return OrderMessageTableStartMilkVector(builder, numElems)

def OrderMessageTableAddBread(builder, bread):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(bread), 0)

def AddBread(builder, bread):
    OrderMessageTableAddBread(builder, bread)

def OrderMessageTableStartBreadVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartBreadVector(builder, numElems: int) -> int:
    return OrderMessageTableStartBreadVector(builder, numElems)

def OrderMessageTableAddMeat(builder, meat):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(meat), 0)

def AddMeat(builder, meat):
    OrderMessageTableAddMeat(builder, meat)

def OrderMessageTableStartMeatVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartMeatVector(builder, numElems: int) -> int:
    return OrderMessageTableStartMeatVector(builder, numElems)

def OrderMessageTableEnd(builder):
    return builder.EndObject()

def End(builder):
    return OrderMessageTableEnd(builder)
