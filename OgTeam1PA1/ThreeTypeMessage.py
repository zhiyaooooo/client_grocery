# automatically generated by the FlatBuffers compiler, do not modify

# namespace: OgTeam1PA1

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class ThreeTypeMessage(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ThreeTypeMessage()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsThreeTypeMessage(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # ThreeTypeMessage
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ThreeTypeMessage
    def Order(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.OrderMessageTable import OrderMessageTable
            obj = OrderMessageTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # ThreeTypeMessage
    def Health(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.HealthMessageTable import HealthMessageTable
            obj = HealthMessageTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # ThreeTypeMessage
    def Response(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from OgTeam1PA1.ResponseMessageTable import ResponseMessageTable
            obj = ResponseMessageTable()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def ThreeTypeMessageStart(builder):
    builder.StartObject(3)

def Start(builder):
    ThreeTypeMessageStart(builder)

def ThreeTypeMessageAddOrder(builder, order):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(order), 0)

def AddOrder(builder, order):
    ThreeTypeMessageAddOrder(builder, order)

def ThreeTypeMessageAddHealth(builder, health):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(health), 0)

def AddHealth(builder, health):
    ThreeTypeMessageAddHealth(builder, health)

def ThreeTypeMessageAddResponse(builder, response):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(response), 0)

def AddResponse(builder, response):
    ThreeTypeMessageAddResponse(builder, response)

def ThreeTypeMessageEnd(builder):
    return builder.EndObject()

def End(builder):
    return ThreeTypeMessageEnd(builder)
