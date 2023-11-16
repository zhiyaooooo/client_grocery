import os
import sys
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/yue/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field
import zmq   # we need this for additional constraints provided by the zmq serialization

## the following are our files
from custom_msg import VeggiesTable
from custom_msg import CansTable
from custom_msg import BottlesTable
from custom_msg import DrinksTable
from custom_msg import MilkTable
from custom_msg import BreadTable
from custom_msg import MeatTable
from custom_msg import OrderMessageTable
import OgTeam1PA1.VeggiesTable
import OgTeam1PA1.CansTable
import OgTeam1PA1.BottlesTable
import OgTeam1PA1.DrinksTable
import OgTeam1PA1.MilkTable
import OgTeam1PA1.BreadTable
import OgTeam1PA1.MeatTable
import OgTeam1PA1.OrderMessageTable

# This is the method we will invoke from our driver program
def serialize (cm):
    # first obtain the builder object
    builder = flatbuffers.Builder (0);
    
    #serialize veggies
    OgTeam1PA1.VeggiesTable.Start (builder)
    OgTeam1PA1.VeggiesTable.AddTomato (builder, cm.veggies.tomato)
    OgTeam1PA1.VeggiesTable.AddCucumber (builder, cm.veggies.cucumber)
    OgTeam1PA1.VeggiesTable.AddPotato (builder, cm.veggies.potato)   
    OgTeam1PA1.VeggiesTable.AddCarrot (builder, cm.veggies.carrot) 
    veggies = OgTeam1PA1.VeggiesTable.End (builder)
    
    #serialize cans
    OgTeam1PA1.CansTable.Start (builder)
    OgTeam1PA1.CansTable.AddCoke (builder, cm.drinks.cans.coke)
    OgTeam1PA1.CansTable.AddBeer (builder, cm.drinks.cans.beer)
    OgTeam1PA1.CansTable.AddPepsi (builder, cm.drinks.cans.pepsi)
    cans = OgTeam1PA1.CansTable.End (builder)
    
    #serialize bottles
    OgTeam1PA1.BottlesTable.Start (builder)
    OgTeam1PA1.BottlesTable.AddSprite (builder, cm.drinks.bottles.sprite)
    OgTeam1PA1.BottlesTable.AddGingerale (builder, cm.drinks.bottles.gingerale)
    OgTeam1PA1.BottlesTable.AddFanta (builder, cm.drinks.bottles.fanta)
    bottles = OgTeam1PA1.BottlesTable.End (builder)
    
    #add cans and bottles to get drinks
    OgTeam1PA1.DrinksTable.Start (builder)
    OgTeam1PA1.DrinksTable.AddCans (builder, cans)
    OgTeam1PA1.DrinksTable.AddBottles (builder, bottles)
    drinks = OgTeam1PA1.DrinksTable.End (builder)
    
    #serialize milk   
    ser_milk = []   # list of serialized individual milk
    for i in range (len (cm.milk.milk_items)):   # for that many items in the milk list
      OgTeam1PA1.MilkTable.Start (builder)
      OgTeam1PA1.MilkTable.AddType (builder, cm.milk.milk_items[i]["type"])
      OgTeam1PA1.MilkTable.AddQuantity (builder, cm.milk.milk_items[i]["quantity"])
      ser_milk.append (OgTeam1PA1.MilkTable.End (builder))
    # Now serialize the vector field inside milk order
    OgTeam1PA1.OrderMessageTable.OrderMessageTableStartMilkVector (builder, len (cm.milk.milk_items))  # number of elements of milk items
    for i in reversed (range (len (cm.milk.milk_items))):   # for that many items in the milk list
      builder.PrependUOffsetTRelative (ser_milk[i])
    ser__milk_vec = builder.EndVector ()  # get the serialized vector of milks
          
    #serialize bread  
    ser_bread = []   # list of serialized individual bread
    for i in range (len (cm.bread.bread_items)):   # for that many items in the bread list
      OgTeam1PA1.BreadTable.Start (builder)
      OgTeam1PA1.BreadTable.AddType (builder, cm.bread.bread_items[i]["type"])
      OgTeam1PA1.BreadTable.AddQuantity (builder, cm.bread.bread_items[i]["quantity"])
      ser_bread.append (OgTeam1PA1.BreadTable.End (builder))
    # Now serialize the vector field inside bread order
    OgTeam1PA1.OrderMessageTable.OrderMessageTableStartBreadVector (builder, len (cm.bread.bread_items))  # number of elements of bread items order
    for i in reversed (range (len (cm.bread.bread_items))):   # for that many items in the bread list
      builder.PrependUOffsetTRelative (ser_bread[i])
    ser__bread_vec = builder.EndVector ()  # get the serialized vector of bread
          
    #serialize meat   
    ser_meat = []   # list of serialized individual meat
    for i in range (len (cm.meat.meat_items)):   # for that many items in the meat list
      OgTeam1PA1.MeatTable.Start (builder)
      OgTeam1PA1.MeatTable.AddType (builder, cm.meat.meat_items[i]["type"])
      OgTeam1PA1.MeatTable.AddQuantity (builder, cm.meat.meat_items[i]["quantity"])
      ser_meat.append (OgTeam1PA1.MeatTable.End (builder))
    # Now serialize the vector field inside meat order
    OgTeam1PA1.OrderMessageTable.OrderMessageTableStartMeatVector (builder, len (cm.meat.meat_items))  # number of elements of meat items order
    for i in reversed (range (len (cm.meat.meat_items))):   # for that many items in the meat list
      builder.PrependUOffsetTRelative (ser_meat[i])
    ser__meat_vec = builder.EndVector ()  # get the serialized vector of meat      
 
    # let us create the serialized message by adding contents to it
    OgTeam1PA1.OrderMessageTable.Start (builder)  # serialization starts with the "Start" method 
    OgTeam1PA1.OrderMessageTable.AddVeggies (builder, veggies)   # serialize veggies
    OgTeam1PA1.OrderMessageTable.AddDrinks (builder, drinks)   # serialize drinks
    OgTeam1PA1.OrderMessageTable.AddMilk (builder, ser__milk_vec)   # serialize milk
    OgTeam1PA1.OrderMessageTable.AddBread (builder, ser__bread_vec)   # serialize bread
    OgTeam1PA1.OrderMessageTable.AddMeat (builder, ser__meat_vec)   # serialize meat
    serialized_msg = OgTeam1PA1.OrderMessageTable.End (builder)  # get the topic of all these fields

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
    
    # Create a FlatBuffers buffer from the serialized data
    buf = bytearray(buf)
    data = OgTeam1PA1.OrderMessageTable.OrderMessageTable.GetRootAsOrderMessageTable(buf, 0)

    # Create an instance of OrderMessageTable
    cm = OrderMessageTable()

    # Deserialize Veggies
    veggies = VeggiesTable()
    veggies.tomato = data.Veggies().Tomato()
    veggies.cucumber = data.Veggies().Cucumber()
    veggies.potato = data.Veggies().Potato()
    veggies.carrot = data.Veggies().Carrot()
    cm.veggies = veggies
    
    # Deserialize Drinks
    drinks = DrinksTable()
    cans = CansTable()
    cans.coke = data.Drinks().Cans().Coke()
    cans.beer = data.Drinks().Cans().Beer()
    cans.pepsi = data.Drinks().Cans().Pepsi()
    drinks.cans = cans
    bottles = BottlesTable()
    bottles.sprite = data.Drinks().Bottles().Sprite()
    bottles.gingerale = data.Drinks().Bottles().Gingerale()
    bottles.fanta = data.Drinks().Bottles().Fanta()
    drinks.bottles = bottles
    cm.drinks = drinks

    # Deserialize Milk
    milk_items = []
    for i in range(data.MilkLength()):
        milk_item = {
            "type": data.Milk(i).Type(),
            "quantity": data.Milk(i).Quantity(),
        }
        milk_items.append(milk_item)
    milk = MilkTable()
    milk.milk_items = milk_items
    cm.milk = milk

    # Deserialize Bread
    bread_items = []
    for i in range(data.BreadLength()):
        bread_item = {
            "type": data.Bread(i).Type(),
            "quantity": data.Bread(i).Quantity(),
        }
        bread_items.append(bread_item)
    bread = BreadTable()
    bread.bread_items = bread_items
    cm.bread = bread

    # Deserialize Meat
    meat_items = []
    for i in range(data.MeatLength()):
        meat_item = {
            "type": data.Meat(i).Type(),
            "quantity": data.Meat(i).Quantity(),
        }
        meat_items.append(meat_item)
    meat = MeatTable()
    meat.meat_items = meat_items
    cm.meat = meat

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
