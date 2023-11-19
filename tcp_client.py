# import the needed packages
import os
import sys
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/yue/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time  # needed for timing measurements and sleep
import random  # random number generator
import argparse  # argument parser
import zmq   # for ZeroMQ
import csv
import pandas as pd

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

from custom_msg import ThreeTypeMessage  # our custom message in native format
from custom_msg import OrderMessageTable  # our custom message in native format
from custom_msg import HealthMessageTable  # our custom message in native format

import serialize_order  # this is from the file serialize_order.py in the same directory
import serialize_health  # this is from the file serialize_health.py in the same directory
import serialize_response  # this is from the file serialize_response.py in the same directory
##################################
# Driver program
##################################



grocery_latency_data = []
health_latency_data = []
#class about creating a socket and using a socket to send/receive messages
class ClientToServer:  
  def __init__ (self, addr, port, name):
    self.addr = addr  #IP address
    self.port = port  #port number
    self.name = name  #name of connection
    self.socket = None
  # create a REQ socket and connect with server
  def configure (self):
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
      # obtain REQ socket
      print ("Obtain the REQ type socket")
      self.socket = context.socket (zmq.REQ)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining REQ socket: {}".format (err))
      return
    except:
      print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
      return

    try:
      # connect
      connect_string = "tcp://" + self.addr + ":" + str (self.port)
      print ("TCP client will be connecting to server {}".format (connect_string))
      self.socket.connect (connect_string)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error connecting REQ socket: {}".format (err))
      self.socket.close ()
      return
    except:
      print ("Some exception occurred connecting REQ socket {}".format (sys.exc_info()[0]))
      self.socket.close ()
      return
    
  # Use the ZMQ's send_serialized method to send message
  def send_request (self, cm):
    """ Send serialized request"""
    try:
      # send serialized message
      print ("ZMQ sending message via ZMQ's send_serialized method")
      if isinstance(cm, OrderMessageTable):
        self.socket.send_serialized (cm, serialize_order.serialize_to_frames)
      elif isinstance(cm, HealthMessageTable):
        self.socket.send_serialized (cm, serialize_health.serialize_to_frames)
      else:
        print ("undefined message")
      
    except zmq.ZMQError as err:
      print ("ZeroMQ Error serializing request: {}".format (err))
      raise
    except:
      print ("Some exception occurred with send_serialized {}".format (sys.exc_info()[0]))
      raise
   
  # Use the ZMQ's recv_serialized method to receive response message
  def recv_reply (self):
    """ receive deserialized reply"""
    try:
      # receive deserialized message
      print ("ZMQ receiving serialized response message")
      cm = self.socket.recv_serialized (serialize_response.deserialize_from_frames, copy=True)
      return cm
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving serialized message: {}".format (err))
      raise
    except:
      print ("Some exception occurred with recv_serialized {}".format (sys.exc_info()[0]))
      raise




def save_latency_to_csv():
    # Save grocery latency data to CSV
    grocery_df = pd.DataFrame({'Latency (s)': grocery_latency_data})
    grocery_df.to_csv('grocery_latency_data.csv', index=False)
    print("Grocery latency data saved to grocery_latency_data.csv")

    # Save health latency data to CSV
    health_df = pd.DataFrame({'Latency (s)': health_latency_data})
    health_df.to_csv('health_latency_data.csv', index=False)
    print("Health latency data saved to health_latency_data.csv")



##################################
# Driver program
##################################
def driver (args):
    
    

    

  # a method to send one message and receive one response message 
  def SendAndReceive (ClientToServerObject, cm, message_type):
    # send serialized message to server and receive deserialized message.
    try:
      # send serialized message
      print ("\n-----Contents of custom message before serializing -----")
      print (cm)
      print ("\nClient sending the serialized message to a server")
      start_time1 = time.time ()
      ClientToServerObject.send_request (cm)
      end_time1 = time.time ()
      print ("Serialization took {} secs".format (end_time1-start_time1))
      print("sending complete")
    except:
      return
      
    try:
      # receive serialized message
      print ("\nReceiving the serialized response message")
      start_time2 = time.time ()
      cm = ClientToServerObject.recv_reply ()
      end_time2 = time.time ()
      print ("Deserialization took {} secs".format (end_time2-start_time2))
      print ("------ contents of response message after deserializing ----------")
      print (cm)      
      print ("\nreceiving complete\n")
    except:
      return
      
      
      
    try:
        # Calculate latency
        latency = end_time2 - start_time1

        # Append latency data to the respective accumulator
        if message_type == 'Health':
            health_latency_data.append(latency)
        elif message_type == 'Grocery':
            grocery_latency_data.append(latency)
    except:
      return
      
    

  # generate random order message
  def random_order ():
    try:
      cm = OrderMessageTable ()
      cm.veggies.tomato = random.randint (1, 100)
      cm.veggies.cucumber = random.randint (1, 100)
      cm.veggies.potato = random.randint (1, 100)
      cm.veggies.carrot = random.randint (1, 100)
      cm.drinks.cans.coke = random.randint (1, 100)
      cm.drinks.cans.beer = random.randint (1, 100)
      cm.drinks.cans.pepsi = random.randint (1, 100)
      cm.drinks.bottles.sprite = random.randint (1, 100)
      cm.drinks.bottles.gingerale = random.randint (1, 100)
      cm.drinks.bottles.fanta = random.randint (1, 100)
      cm.milk.add_milk(random.randint (0, 6), random.uniform (1, 100))
      cm.milk.add_milk(random.randint (0, 6), random.uniform (1, 100))
      cm.milk.add_milk(random.randint (0, 6), random.uniform (1, 100))
      cm.bread.add_bread(random.randint (0, 2), random.uniform (1, 100))
      cm.meat.add_meat(random.randint (0, 3), random.uniform (1, 100))
      cm.meat.add_meat(random.randint (0, 3), random.uniform (1, 100))
      return cm
    except:
      print ("Some exception occurred when generating random order message")
      
  # generate random health message
  def random_health ():
    try:
      cm = HealthMessageTable ()
      cm.dispenser = random.randint (0, 2)
      cm.icemaker = random.randint (0, 100)
      cm.lightbulb = random.randint (0, 1)
      cm.fridge_temp = random.randint (40, 50)
      cm.freezer_temp = random.randint (14, 23)
      cm.sensor_status = random.randint (0, 1)
      cm.door_status = random.randint (0, 1)
      return cm
    except:
      print ("Some exception occurred when generating random health message")
  
  # create sockets for two servers and configure them
  ClientToGrocery = ClientToServer (args.addrG, args.portG, args.nameG)
  # ClientToHealth = ClientToServer (args.addrH, args.portH, args.nameH)
  ClientToGrocery.configure ()
  # ClientToHealth.configure ()   
    
  # now send the serialized custom message for the number of desired iterations
  for i in range (args.iters):
    print ("\n-----Iteration: {} -----".format (i))
    #Send health message once every two order messages
    SendAndReceive (ClientToGrocery, random_order (), 'Grocery')
    SendAndReceive (ClientToGrocery, random_order (), 'Grocery')
    # SendAndReceive (ClientToHealth, random_health (), 'Health')
    # sleep a while before we send the next serialization so it is not extremely fast
    time.sleep (0.050)  # 50 msec
        
##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-aG", "--addrG", default="127.0.0.1", help="IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-aH", "--addrH", default="127.0.0.1", help="IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
  parser.add_argument ("-pG", "--portG", type=int, default=5555, help="Port that grocery server is listening on (default: 5555)")
  parser.add_argument ("-pH", "--portH", type=int, default=6666, help="Port that health server is listening on (default: 6666)")
  parser.add_argument ("-nG", "--nameG", default="FlatBuffer ZMQ Demo Client To Grocery", help="Name to include in each message")  
  parser.add_argument ("-nH", "--nameH", default="FlatBuffer ZMQ Demo Client To Health", help="Name to include in each message")  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Client")

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
  
  save_latency_to_csv()
