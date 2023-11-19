# Define the classes based on schema

from typing import List
from dataclasses import dataclass
from enum import IntEnum

class BreadType(IntEnum):
  wholeWheat = 0
  pumpernickel = 1
  rye = 2

class MilkType(IntEnum):
  onePercent = 0
  twoPercent = 1
  fatFree = 2
  whole = 3
  almond = 4
  cashew = 5
  oat = 6

class MeatType(IntEnum):
  mutton = 0
  beef = 1
  chicken = 2
  pork = 3

class DispenserStatus(IntEnum):
  Optimal = 0
  Partial = 1
  Blockage = 2

class GoodBadStatus(IntEnum):
  Good = 0
  Bad = 1

class DoorStatus(IntEnum):
  Open = 0
  Close = 1

class ReplyCode(IntEnum):
  OK = 0
  BAD_REQUEST = 1

# veggies including four types
class VeggiesTable:
  def __init__(self):
    self.tomato = 0.0
    self.cucumber = 0.0
    self.potato = 0.0
    self.carrot = 0.0
  # define a string to print it
  def __str__(self):
    return f"tomato: {self.tomato}, cucumber: {self.cucumber}, potato: {self.potato}, carrot: {self.carrot}"

# cans including three types
class CansTable:
  def __init__(self):
    self.coke = 0
    self.beer = 0
    self.pepsi = 0
  # define a string to print it
  def __str__(self):
    return f"coke: {self.coke}, beer: {self.beer}, pepsi: {self.pepsi}"

# bottles including three types
class BottlesTable:
  def __init__(self):
    self.sprite = 0
    self.gingerale = 0
    self.fanta = 0
  # define a string to print it
  def __str__(self):
    return f"sprite: {self.sprite}, gingerale: {self.gingerale}, fanta: {self.fanta}"

# drinks including cans and bottles just defined
class DrinksTable:
  def __init__(self):
    self.cans = CansTable()
    self.bottles = BottlesTable()
  def __str__(self):
    return f"cans: {str(self.cans)}, \nbottles: {str(self.bottles)}"

# milk including a list
class MilkTable:
  def __init__(self):
    self.milk_items = []  # List to store milk items
  # add items to the list
  def add_milk(self, milk_type, quantity):
    # Create a dictionary to represent a milk item
    milk_item = {"type": milk_type, "quantity": quantity}
    self.milk_items.append(milk_item)
  # define a string to print it, mapping enum values to type names
  def __str__(self):
    milk_type_names = {
      MilkType.onePercent: "One Percent",
      MilkType.twoPercent: "Two Percent",
      MilkType.fatFree: "Fat-Free",
      MilkType.whole: "Whole",
      MilkType.almond: "Almond",
      MilkType.cashew: "Cashew",
      MilkType.oat: "Oat",
      }

    milk_items_str = ", ".join([f"{{type: {milk_type_names[item['type']]}, quantity: {item['quantity']}}}" for item in self.milk_items])
    return f"[{milk_items_str}]"
    
# bread including a list    
class BreadTable:
  def __init__(self):
    self.bread_items = []  # List to store bread items
  # add items to the list
  def add_bread(self, bread_type, quantity):
    # Create a dictionary to represent a bread item
    bread_item = {"type": bread_type, "quantity": quantity}
    self.bread_items.append(bread_item)
  # define a string to print it, mapping enum values to type names
  def __str__(self):
    # define a mapping from numbers to type name
    bread_type_names = {
      BreadType.wholeWheat: "Whole Wheat",
      BreadType.pumpernickel: "Pumpernickel",
      BreadType.rye: "Rye",
      }
    
    bread_items_str = ", ".join([f"{{type: {bread_type_names[item['type']]}, quantity: {item['quantity']}}}" for item in self.bread_items])
    return f"[{bread_items_str}]"

# meat including a list
class MeatTable:
  def __init__(self):
    self.meat_items = []  # List to store meat items
  # add items to the list
  def add_meat(self, meat_type, quantity):
    # Create a dictionary to represent a meat item
    meat_item = {"type": meat_type, "quantity": quantity}
    self.meat_items.append(meat_item)
  # define a string to print it, mapping enum values to type names
  def __str__(self):
    meat_type_names = {
      MeatType.mutton: "Mutton",
      MeatType.beef: "Beef",
      MeatType.chicken: "Chicken",
      MeatType.pork: "Pork",
      }
    meat_items_str = ", ".join([f"{{type: {meat_type_names[item['type']]}, quantity: {item['quantity']}}}" for item in self.meat_items])
    return f"[{meat_items_str}]"

# order message including tables just defined
class OrderMessageTable:
  def __init__(self):
    self.veggies = VeggiesTable()
    self.drinks = DrinksTable()
    self.milk = MilkTable()
    self.bread = BreadTable()
    self.meat = MeatTable()
    
  # define a string to print it
  def __str__(self):
    return f"veggies: {{\n{self.veggies}\n}},\n" \
           f"drinks: {{\n{self.drinks}\n}},\n" \
           f"milk: {self.milk},\n" \
           f"bread: {self.bread},\n" \
           f"meat: {self.meat},"

# health message 
class HealthMessageTable:
  def __init__(self):
    self.dispenser = DispenserStatus.Optimal
    self.icemaker = 0
    self.lightbulb = GoodBadStatus.Good
    self.fridge_temp = 0
    self.freezer_temp = 0
    self.sensor_status = GoodBadStatus.Good
    self.door_status = DoorStatus.Open
  # define a string to print it, mapping enum values to type names
  def __str__(self):
    # Create mappings from enum values to their names
    dispenser_status_names = {
      DispenserStatus.Optimal: "Optimal",
      DispenserStatus.Partial: "Partial",
      DispenserStatus.Blockage: "Blockage",
      }

    good_bad_status_names = {
      GoodBadStatus.Good: "Good",
      GoodBadStatus.Bad: "Bad",
      }

    door_status_names = {
      DoorStatus.Open: "Open",
      DoorStatus.Close: "Close",
      }

    # Convert status fields to their names
    dispenser_status_str = dispenser_status_names[self.dispenser]
    lightbulb_status_str = good_bad_status_names[self.lightbulb]
    sensor_status_str = good_bad_status_names[self.sensor_status]
    door_status_str = door_status_names[self.door_status]

    return f"dispenser: {dispenser_status_str}\nicemaker: {self.icemaker}\n" \
           f"lightbulb: {lightbulb_status_str}\nfridge_temp: {self.fridge_temp}\n" \
           f"freezer_temp: {self.freezer_temp}\nsensor_status: {sensor_status_str}\n" \
           f"door_status: {door_status_str}"

# response message
class ResponseMessageTable:
  def __init__(self):
    self.code = ReplyCode.OK
    self.contents = ""
  # define a string to print it, mapping enum values to type names
  def __str__(self):
    # Create a mapping from enum values to their names
    reply_code_names = {
    ReplyCode.OK: "OK",
    ReplyCode.BAD_REQUEST: "Bad Request",
    }

    # Convert code field to its name
    code_str = reply_code_names[self.code]

    return f"code: {code_str}\ncontents: {self.contents}"

# combine three types of message
class ThreeTypeMessage:
  def __init__(self):
    self.order = OrderMessageTable()
    self.health = HealthMessageTable()
    self.response = ResponseMessageTable()
  # define a string to print it
  def __str__(self):
    return f"order: {{\n{self.order}\n}},\n" \
           f"health: {{\n{self.health}\n}},\n" \
           f"response: {{\n{self.response}\n}}"

# test if we can instantiate an object of ThreeTypeMessage and assign values to it
def main():
  cm = ThreeTypeMessage ()
  cm.order.veggies.tomato = 123
  cm.order.veggies.carrot = 99
  cm.order.drinks.cans.pepsi = 114
  cm.order.drinks.bottles.sprite = 13
  cm.order.bread.add_bread(BreadType.pumpernickel, 13.5)  
  cm.order.bread.add_bread(BreadType.wholeWheat, 10.5)
  cm.order.meat.add_meat(MeatType.mutton, 0.78)
  cm.order.milk.add_milk(MilkType.almond, 0.11)
  cm.order.milk.add_milk(MilkType.oat, 1110.11)

  cm.health.dispenser = DispenserStatus.Partial
  cm.health.icemaker = 50
  cm.health.lightbulb = GoodBadStatus.Bad
  cm.health.fridge_temp = 40
  cm.health.freezer_temp = 20
  cm.health.sensor_status = GoodBadStatus.Good
  cm.health.sensor_status = 1
  cm.health.door_status = DoorStatus.Close

  cm.response.code = 1
  cm.response.contents = "Order Placed"
  cm.response.contents = "You are Healthy"
  cm.response.contents = "Bad Request"
  
  print(cm)
  print(cm.order.milk.milk_items[0]["type"])
  print(cm.health.dispenser)

# make sure test code won't be executed when imported to other files
if __name__ == '__main__':
  main ()
