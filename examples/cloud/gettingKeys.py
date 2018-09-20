#!/usr/bin/env python3

"""An example that shows how to login to the cloud."""

import time

from BluenetLib import Bluenet, BluenetEventBus, Topics

bluenet = Bluenet(catchSIGINT=True)
cloud   = bluenet.getCloud()

# Insert your own Crownstone Account Settings here. You can also load from file if you'd like. Check the readme for more options.
cloud.setUserInformation('myEmailAddress@gmail.com', 'myPassword')

if not cloud.isLoggedIn():
    print("Could not log in...")
else:
    # show my spheres
    mySpheres = cloud.getSpheres()
    print(mySpheres)
    
    if len(mySpheres) == 0:
        print("No Spheres Available.")
    else:
        # select the first sphere and use it's id to get a SphereHandler
        sphereHandler = cloud.getSphereHandler(mySpheres[0]["id"])
        
        myKeys = sphereHandler.getKeys()
        print(myKeys)
        
        # these keys you can put into Bluenet with the setSettings command:
        # core = BluenetBle(hciIndex=0)
        # core.setSettings(myKeys["admin"], myKeys["member"], myKeys["guest"])

