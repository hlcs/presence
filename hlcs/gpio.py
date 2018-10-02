'''
    Created on 08/nov/2014
    @author: spax

    Classe epr la gestione delle gpio
'''
import logging

import RPi.GPIO as GPIO
from time import sleep
from django.conf import settings


# riferimento ai pin come Broadcom SOC channel (e non riferimenti numerici)
GPIO.setmode(GPIO.BCM)

# inizializzazione pin
LOCK_PIN = getattr(settings, 'LOCK_PIN', 4)
MAGNET_PIN = getattr(settings, 'MAGNET_PIN', 17)

PULSE_SLEEP = getattr(settings, 'PULSE_SLEEP', 1)
PULSE_ON = getattr(settings, 'PULSE_ON', 0)
PULSE_OFF = getattr(settings, 'PULSE_OFF', 1)


# setup delle gpio
def setup():
    GPIO.setup(LOCK_PIN, GPIO.OUT, initial=PULSE_OFF)
    GPIO.setup(MAGNET_PIN, GPIO.IN)

# restituisce il magnet_input
def magnet_input():
    return GPIO.input(MAGNET_PIN)


# apertura
def send_open_pulse():
    GPIO.output(LOCK_PIN, PULSE_ON)
    sleep(PULSE_SLEEP)
    GPIO.output(LOCK_PIN, PULSE_OFF)
