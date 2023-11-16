# import the needed packages
import os
import sys
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/yue/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time  # needed for timing measurements and sleep
import random  # random number generator
import argparse  # argument parser
import zmq   # for ZeroMQ

## the following are our files
from OgTeam1PA1.BottlesTable import BottlesTable
from OgTeam1PA1.BreadTable import BreadTable
from OgTeam1PA1.BreadType import BreadType
from OgTeam1PA1.CansTable import CansTable
from OgTeam1PA1.DispenserStatus import DispenserStatus
from OgTeam1PA1.DoorStatus import DoorStatus
from OgTeam1PA1.DrinksTable import DrinksTable
from OgTeam1PA1.GoodBadStatus import GoodBadStatus
from OgTeam1PA1.HealthMessageTable import HealthMessageTable
from OgTeam1PA1.MeatTable import MeatTable
from OgTeam1PA1.MeatType import MeatType
from OgTeam1PA1.MilkTable import MilkTable
from OgTeam1PA1.MilkType import MilkType
from OgTeam1PA1.OrderMessageTable import OrderMessageTable
from OgTeam1PA1.ReplyCode import ReplyCode
from OgTeam1PA1.ResponseMessageTable import ResponseMessageTable
from OgTeam1PA1.ThreeTypeMessage import ThreeTypeMessage
from OgTeam1PA1.VeggiesTable import VeggiesTable

from custom_msg import ResponseMessageTable  # our custom message in native format
from custom_msg import ThreeTypeMessage  # our custom message in native format
import serialize_order  # this is from the file serialize_order.py in the same directory
import serialize_health  # this is from the file serialize_health.py in the same directory
import serialize_response  # this is from the file serialize_response.py in the same directory
##################################
# Driver program
##################################
def driver (args):
  try:
    # every ZMQ session requires a context
    print ("Obtain the ZMQ context")
    context = zmq.Context ()   # returns a singleton object
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining context: {}".format (err))
    return
  except:
    print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
    return

  try:
    # obtain REP socket
    print ("Obtain the REP type socket")
    socket = context.socket (zmq.REP)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining REP socket: {}".format (err))
    return
  except:
    print ("Some exception occurred getting REP socket {}".format (sys.exc_info()[0]))
    return

  try:
    # bind
    bind_string = "tcp://" + args.intf + ":" + str (args.port)
    print ("TCP server will be binding on {}".format (bind_string))
    socket.bind (bind_string)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error binding REP socket: {}".format (err))
    socket.close ()
    return
  except:
    print ("Some exception occurred binding REP socket {}".format (sys.exc_info()[0]))
    socket.close ()
    return

  # Use the ZMQ's recv_serialized method to send the custom message
  def recv_request ():
    """ receive serialized request"""
    try:
      # receive deserialized message
      print ("ZMQ receiving serialized order message")
      cm = socket.recv_serialized (serialize_order.deserialize_from_frames, copy=True)
      return cm
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving serialized message: {}".format (err))
      raise
    except:
      print ("Some exception occurred with recv_serialized {}".format (sys.exc_info()[0]))
      raise
      
  # Use the ZMQ's send_serialized method to send the custom message
  def send_reply (cm):
    """ Send serialized reply"""
    try:
      # send serialized message
      print ("ZMQ sending response message via ZMQ's send_serialized method")
      socket.send_serialized (cm, serialize_response.serialize_to_frames)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error serializing reply: {}".format (err))
      raise
    except:
      print ("Some exception occurred with send_serialized {}".format (sys.exc_info()[0]))
      raise

  # since we are a server, we service incoming clients forever
  print ("Server now waiting to receive something")
  while True:
    try:
      # receive serialized message
      print ("\nReceiving the serialized message")
      start_time = time.time ()
      cm = recv_request ()
      end_time = time.time ()
      print ("Deserialization took {} secs".format (end_time-start_time))
      print ("------ contents of message after deserializing ----------")
      print (cm)
      print ("\nreceiving complete\n")
    except:
      return
    
    cm = ResponseMessageTable()
    cm.code = 0
    cm.contents = "Order Placed"
    
    # send serialized reply to client.
    try:
      # send serialized message
      print ("------ contents of response message before serializing ----------")
      print(cm)
      print ("\nServer sending the serialized message to client")
      start_time = time.time ()
      send_reply (cm)   
      end_time = time.time ()   
      print ("Serialization took {} secs".format (end_time-start_time))
      print ("sending complete\n")
    except:
      return

    #  Do some 'work'. In this case we just sleep.
    time.sleep (0.05)



##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-i", "--intf", default="*", help="Interface to bind to (default: *)")
  parser.add_argument ("-p", "--port", type=int, default=5555, help="Port to bind to (default: 5555)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Grocery Server")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
