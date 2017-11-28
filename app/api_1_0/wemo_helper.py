from ouimeaux.environment import Environment
import logging
from flask import json
import threading

switches = []

class WemoSwitch(object):
    def __init__(self,switch):
        self.label = switch.basicevent.GetFriendlyName()['FriendlyName']
        self.id = switch.basicevent.GetHomeId()['DeviceId']
        self.power = switch.basicevent.GetBinaryState()['BinaryState'] == '1'

def on_switch(switch):
    logging.info("Found Switch")
    switches.append(WemoSwitch(switch))

def get_all_switches():
    return switches

def run_discovery():
    env = Environment(on_switch)
    #env.start()
    #env.discover(seconds = 5)
