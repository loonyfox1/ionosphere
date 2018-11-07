import original_hotkeys as hotkeys
import time



def test_function(event,parameter):
    print(event)
    if(event.name=='SPACE'):
        parameter['running']=False
        #print("Space")


parameters={'running':True}

hotkeysdetector=hotkeys.HotKeysDetector(parameters=True)
hotkeysdetector.addhotkeys("CONTROL_L+f12",test_function,parameters)
hotkeysdetector.addhotkeys("SPACE",test_function,parameters)
hotkeysdetector.start()

while parameters['running']:
    time.sleep(0.1)

hotkeysdetector.cancel()
