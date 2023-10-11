from smbus2 import SMBus

class I2CBridge():

    def __init__(self):

        # SMBus
        self.DEVICE_BUS = 1
        self.DEVICE_ADDR = 0x08
        self.bus = SMBus(self.DEVICE_BUS)

        # Movement constants
        self.MOVEMENT = 0x00
        self.FORWARD = 0x01
        self.BACKWARD = 0x02
        self.LEFT = 0x03
        self.RIGHT = 0x04
        self.STOP = 0x05

        # Auger constants
        self.AUGER = 0x10
        self.CLOCKWISE = 0x11
        self.COUNTERCLOCKWISE = 0x12
        self.STOP_SPIN = 0x13
        self.STOP_MOVE = 0x14
        
        # Tilt constants
        self.TILT = 0x20
        self.BODY_FORWARD = 0x21
        self.BODY_BACKWARD = 0x22
        self.AUGER_FORWARD = 0x23
        self.AUGER_BACKWARD = 0x24
        self.BODY_STOP = 0x25
        self.AUGER_STOP = 0x26
        
        # Autonomy constants
        self.AUTO = 0x30
        self.ENABLE_DRIVE = 0x31
        self.DISABLE_DRIVE = 0x32
        self.ENABLE_DIG = 0x33
        self.DISABLE_DIG = 0x34
        
        self.TYPES = {
            "movement": self.MOVEMENT,
            "auger": self.AUGER,
            "tilt": self.TILT,
            "auto": self.AUTO
        }
        
        self.COMMANDS = {
            # movement
            "forward": self.FORWARD,
            "backward": self.BACKWARD,
            "left": self.LEFT,
            "right": self.RIGHT,
            "stop": self.STOP,
            
            # auger
            "clockwise": self.CLOCKWISE,
            "counterclockwise": self.COUNTERCLOCKWISE,
            "stopspin": self.STOP_SPIN,
            "stopmove": self.STOP_MOVE,
            
            # tilt
            "bodyforward": self.BODY_FORWARD,
            "bodybackward": self.BODY_BACKWARD,
            "augerforward": self.AUGER_FORWARD,
            "augerbackward": self.AUGER_BACKWARD,
            "bodystop": self.BODY_STOP,
            "augerstop": self.AUGER_STOP,
            
            # auto
            "enabledrive": self.ENABLE_DRIVE,
            "disabledrive": self.DISABLE_DRIVE,
            "enabledig": self.ENABLE_DIG,
            "disabledig": self.DISABLE_DIG,
        
        }

    def status(self):
        self.bus.read_byte(self.DEVICE_ADDR)

    def move_speed(self, type, command, speed):
            
        if speed < 0:
            raise Exception("Invalid speed")

        self.bus.write_i2c_block_data(self.DEVICE_ADDR, self.TYPES[type], [self.COMMANDS[command], speed])
        
    def move(self, type, command):

        self.bus.write_i2c_block_data(self.DEVICE_ADDR, self.TYPES[type], [self.COMMANDS[command]])
