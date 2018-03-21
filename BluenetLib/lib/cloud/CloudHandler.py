from BluenetLib.lib.cloud.CloudBase import CloudBase
from BluenetLib.lib.cloud.CloudSphereHandler import CloudSphereHandler


class CloudHandler(CloudBase):
    
    def __init__(self):
        super().__init__()
        pass
    
    def getSphereHandler(self, sphereId):
        sphereHandler = CloudSphereHandler(sphereId)

        sphereHandler.email        = self.email
        sphereHandler.password     = self.password
        sphereHandler.sha1Password = self.sha1Password
        sphereHandler.accessToken  = self.accessToken
        sphereHandler.userId       = self.userId
        sphereHandler.initialized  = self.initialized
        
        return sphereHandler
    
    def getSphereHandlerByName(self, sphereName):
        pass
    
    def getStones(self, sphereId):
        pass

    def getLocations(self, sphereId):
        pass

    def getKeys(self, sphereId):
        pass
        
    def getPresence(self, sphereId):
        pass
    
    def pollPresence(self, sphereId):
        pass

    
    
    
            
    
    


            
    
    

    





       