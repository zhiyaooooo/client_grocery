import os
import sys
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/yue/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field
import zmq   # we need this for additional constraints provided by the zmq serialization
from custom_msg import HealthMessageTable  # our health message in native format
import OgTeam1PA1.HealthMessageTable as msg   # this is the generated code by the flatc compiler

# This is the method we will invoke from our driver program
def serialize (cm):
    # first obtain the builder object
    builder = flatbuffers.Builder (0);
  
    # let us create the serialized msg by adding contents to it
    msg.Start (builder)  # serialization starts with the "Start" method
    msg.AddDispenser (builder, cm.dispenser)   # serialize dispenser
    msg.AddIcemaker (builder, cm.icemaker)   # serialize icemaker
    msg.AddLightbulb (builder, cm.lightbulb)   # serialize lightbulb
    msg.AddFridgeTemp (builder, cm.fridge_temp)   # serialize fridge_temp
    msg.AddFreezerTemp (builder, cm.freezer_temp)   # serialize freezer_temp
    msg.AddSensorStatus (builder, cm.sensor_status)   # serialize sensor_status
    msg.AddDoorStatus (builder, cm.door_status)   # serialize door_status
    serialized_msg = msg.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  print ("serialize custom message to iterable list")
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize (buf):
    
    # Create an instance of HealthMessageTable
    cm = HealthMessageTable ()    
    packet = msg.HealthMessageTable.GetRootAs (buf, 0)
    cm.dispenser = packet.Dispenser ()  # dispenser
    cm.icemaker = packet.Icemaker ()  # icemaker
    cm.lightbulb = packet.Lightbulb ()  # lightbulb
    cm.fridge_temp = packet.FridgeTemp ()  # fridge_temp
    cm.freezer_temp = packet.FreezerTemp ()  # freezer_temp
    cm.sensor_status = packet.SensorStatus ()  # sensor_status
    cm.door_status = packet.DoorStatus ()  # door_status

    return cm
    
# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm
