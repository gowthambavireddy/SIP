import sys

import pjsua as pj

import threading

import time



# Method to print Log of callback class

def log_cb(level, str, len):

    print((str), end=' ')



# Account Callback class to get notifications of Account registration

class MyAccountCallback(pj.AccountCallback):

    def __init__(self, acc):

        pj.AccountCallback.__init__(self, acc)



# Call Callback to receive events from Call

class SRCallCallback(pj.CallCallback):

    def __init__(self, call=None):

        pj.CallCallback.__init__(self, call)

    

    

    def on_state(self):

        print(("Call is :", self.call.info().state_text), end=' ')

        print(("last code :", self.call.info().last_code), end=' ')

        print(("(" + self.call.info().last_reason + ")"))

        

    # This is the notification when call's media state is changed

    def on_media_state(self):

        global lib

        if self.call.info().media_state == pj.MediaState.ACTIVE:

            # Connect the call to sound device

            call_slot = self.call.info().conf_slot

            lib.conf_connect(call_slot, 0)

            lib.conf_connect(0, call_slot)

            print("Hey !!!!! Hope you are doing GOOD !!!!!!!!!!")

            print (lib)


# Lets start our main loop here

try:

    # Start of the Main Class

    # Create library instance of Lib class

    lib = pj.Lib()



    # Instantiate library with default config

    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))



    # Configuring one Transport Object and setting it to listen at 5060 port and UDP protocol

    trans_conf = pj.TransportConfig()

    print("-------------------------LETS START THE REGISTRATION PROCESS----------------------")
    print("\n\n")


    trans_conf.port = 5060       # 5060 is default port for SIP

   # a=input("Please Enter the IP address of the Client: ")
    a="192.168.0.50" # Local VM IP
    print("Using the default port number for SIP: 5060")

    trans_conf.bound_addr = a

    transport = lib.create_transport(pj.TransportType.UDP,trans_conf)



    # Starting the instance of Lib class

    lib.start()

    lib.set_null_snd_dev()



    # Configuring Account class to register with Registrar server

    # Giving information to create header of REGISTER SIP message

    

    # ab4=input("Enter IP address of the Server: ")
    ab4="philly.sip.us1.twilio.com" # Asteriek server IP
    # ab=input("Enter Username: ")
    ab = "gowtham"
    # ab1=input("Enter Password: ")
    ab1 = "Gowtham_password123"
    # ab2=input("Do you want to use the display name same as the username  Y/N ??")
    ab2 = "Y"
    if ab2=="y" or ab2=="Y":
        ab3=ab
    else:
        ab3=input("Enter Display Name: ")

    acc_conf = pj.AccountConfig(ab4, ab, ab1)

                              # registrar = 'sip:'+ab4+':5060', proxy = 'sip:'+ab4+':5060')

   # acc_conf.id ="sip:"+ab

   # acc_conf.reg_uri ='sip:'+ab4+':5060'

    acc_callback = MyAccountCallback(acc_conf)

    acc = lib.create_account(acc_conf)



    # creating instance of AccountCallback class

    acc.set_callback(acc_callback)


    time.sleep(20)
    print('\n')
    print("Registration Complete-----------")
    print(('Status= ',acc.info().reg_status, \

         '(' + acc.info().reg_reason + ')'))



    ab5=input("Do you want to make a call right now ??   Y/N\n")
    print("\n")

    if ab5=="y" or ab5=="Y":

    # Starting Calling process.
        b=input("Enter the destination URI: ")
        # c="sip:"+ b + "@192.168.0.34:5060"
        call = acc.make_call(b, SRCallCallback())

        

        

        # Waiting Client side for ENTER command to exit

        print('Press <ENTER> to exit and destroy library')

        input = sys.stdin.readline().rstrip('\r\n')



        # We're done, shutdown the library

        lib.destroy()

        lib = None

    else:

        print(" Unregistering ---------------------------")
        time.sleep(2)
        print("Destroying Libraries --------------")
        time.sleep(2)
        lib.destroy()
        lib = None
        sys.exit(1)


except pj.Error as e:

    print(("Exception: " + str(e)))

    lib.destroy()

    lib = None

    sys.exit(1)
