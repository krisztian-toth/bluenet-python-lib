import time
from threading import Timer

AMOUNT_OF_REQUIRED_MATCHES = 3

class StoneTracker:
    rssiHistory = {}
    rssi = None
    name = ""
    address = None
    crownstoneId = 0
    lastUpdate = 0
    avgRssi = 0
    cleanupCallback = None
    uniqueIdentifier = 0
    verified = False
    dfu = False
    
    # config
    timeout = 20  # seconds
    rssiTimeout = 3  # seconds
    consecutiveMatches = 0
    
    timeoutTimers = {}
    rssiTimers = {}
    
    def __init__(self, cleanupCallback):
        self.cleanupCallback = cleanupCallback
    
    def update(self, advertisement):
        self.name = advertisement.name
        self.address = advertisement.address
        self.avgRssi = advertisement.rssi
        if advertisement.isCrownstoneFamily():
            self.handlePayload(advertisement)
                
                
    def handlePayload(self, advertisement):
        self.rssi = advertisement.rssi
    
        updateTime = time.time()
        self.lastUpdate = updateTime
    
        self.rssiHistory[self.lastUpdate] = self.rssi
    
        if advertisement.isInDFUMode():
            self.verified = True
            self.dfu = True
            self.consecutiveMatches = 0
        else:
            self.verify(advertisement.serviceData)
        
    
        self.calculateRssiAverage()
        
        self.timeoutTimers[updateTime] = Timer(self.timeout,     lambda: self.checkTimeout(updateTime), ())
        self.rssiTimers[updateTime]    = Timer(self.rssiTimeout, lambda: self.clearRSSI(   updateTime), ())

        self.timeoutTimers[updateTime].start()
        self.rssiTimers[updateTime].start()


    def cancelRunningTimers(self):
        for time, timer in self.timeoutTimers.items():
            timer.cancel()

        for time, timer in self.rssiTimers.items():
            timer.cancel()

    def checkTimeout(self, referenceTime):
        # if they are equal, no update has happened since the scheduling of this check.
        del self.timeoutTimers[referenceTime]
        if self.lastUpdate == referenceTime:
            self.cleanupCallback()


    def clearRSSI(self, referenceTime):
        del self.rssiHistory[referenceTime]
        del self.rssiTimers[referenceTime]
        self.calculateRssiAverage()


    # check if we consistently get the ID of this crownstone.
    def verify(self, serviceData):
        if serviceData.isInSetupMode():
            self.verified = True
            self.consecutiveMatches = 0
        else:
            if self.uniqueIdentifier != serviceData.uniqueIdentifier:
                if serviceData.validation != 0 and serviceData.opCode == 3:
                    if serviceData.validation == 0xFACE and serviceData.dataType != 1:
                        self.addValidMeasurement(serviceData)
                    elif serviceData.validation != 0xFACE and serviceData.dataType != 1:
                        self.invalidateDevice(serviceData)
            else:
                if not serviceData.stateOfExternalCrownstone:
                    if serviceData.crownstoneId == self.crownstoneId:
                        self.addValidMeasurement(serviceData)
                    else:
                        self.invalidateDevice(serviceData)
        
        self.uniqueIdentifier = serviceData.uniqueIdentifier
        

    
    def addValidMeasurement(self, serviceData):
        if self.consecutiveMatches >= AMOUNT_OF_REQUIRED_MATCHES:
            self.verified = True
            self.consecutiveMatches = 0
        else:
            self.consecutiveMatches += 1
        
        self.crownstoneId = serviceData.crownstoneId


    def invalidateDevice(self, serviceData):
        if not serviceData.stateOfExternalCrownstone:
            self.crownstoneId = serviceData.crownstoneId
        
        self.consecutiveMatches = 0
        self.verified = False


    def calculateRssiAverage(self):
        count = 0
        total = 0
        for key, rssi in self.rssiHistory.items():
            total = total + rssi
            count += 1
        
        if count > 0:
            self.avgRssi = total / float(count)
        else:
            self.avgRssi = 0
        
    def shutDown(self):
        self.cancelRunningTimers()
        
        
        