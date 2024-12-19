VERSION_GPIO = RPI_REVISION = RPI_REVISION_HEX = OUT = IN = ALT0 = BOARD = BCM = PUD_OFF = RISING = FALLING = PUD_UP = PUD_DOWN = False
LOW = False
HIGH = True

instant_values = {}

def setmode(*useless):
    pass

def setwarnings(*useless):
    pass

def setup(channel, state, initial=None, pull_up_down=None):
    instant_values[channel] = state
    print(f"GPIO ---> Setup channel {channel} to state {state}")

def output(channel, value):
    print(f"GPIO ---> Output value {value} to channel #{channel}")
    instant_values[channel] = value

def input(channel):
    print(f"GPIO ---> Input - Return {instant_values[channel]} for channel #{channel} value")
    return instant_values[channel]

def wait_for_edge(channel, edge):
    pass 

def PWM(channel, frequency):
    return pwm_instance()

class pwm_instance():
    def start(*any):
        pass
    def ChangeDutyCycle(*v):
        print("GPIO ---> ChangeDutyCycle"+str(v))
        pass
    def stop(*any):
        pass
    
def cleanup():
    pass

def add_event_detect(*any, callback, bouncetime):
    pass

def event_detected(*any):
    pass

# raise NotImplementedError
