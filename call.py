#
# SIP call sample.
#
# Copyright (C) Gowtham Bavireddy<gowtham.bavireddy@philips.com>

#
import sys
import pjsua as pj
import time

LOG_LEVEL = 3
current_call = None


# Logging callback
def log_cb(level, str, len):
    print(str, end=' ')


# Callback to receive events from account
class MyAccountCallback(pj.AccountCallback):

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    # Notification on incoming call
    def on_incoming_call(self, call):
        global current_call
        if current_call:
            call.answer(486, "Busy")
            return

        print("Incoming call from ", call.info().remote_uri)
        print("Press 'a' to answer")

        current_call = call

        call_cb = MyCallCallback(current_call)
        current_call.set_callback(call_cb)

        current_call.answer(180)


# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        print("Call with", self.call.info().remote_uri, end=' ')
        print("is", self.call.info().state_text, end=' ')
        print("last code =", self.call.info().last_code, end=' ')
        print("(" + self.call.info().last_reason + ")")

        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print('Current call is', current_call)

    # Notification when call's media state has changed.
    def on_media_state(self):
        print("############")
        print(self.call.info().media_state)
        print(pj.MediaState.ACTIVE)
        print("#################")
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 1)
            pj.Lib.instance().conf_connect(1, call_slot)
            print("Media is now active")
        else:
            print("Media is inactive")


# Function to make call
def make_call(name):
    try:
        uri = "sip:" + name + "@philly.sip.us1.twilio.com"
        print("Making call to", uri)
        return acc.make_call(uri, cb=MyCallCallback())
    except pj.Error as e:
        print("Exception: " + str(e))
        return None


# Create library instance
lib = pj.Lib()

try:
    # # Init library with default config and some customized
    # # logging config.
    # lib.init(log_cfg=pj.LogConfig(level=LOG_LEVEL, callback=log_cb))
    #
    # trans_conf = pj.TransportConfig()
    # trans_conf.port = 5060
    # trans_conf.bound_addr = "192.168.0.50"
    #
    # # Create UDP transport which listens to any available port
    # transport = lib.create_transport(pj.TransportType.UDP, trans_conf)
    # print("\nListening on", transport.info().host, end=' ')
    # print("port", transport.info().port, "\n")
    #
    # # Start the library
    # lib.start()
    #
    # # Create local account
    # acc = lib.create_account_for_transport(transport, cb=MyAccountCallback())
    # time.sleep(10)
    # print("Registration Status-------------")
    # print(acc.info().reg_status)
    # Start of the Main Class

    # Instantiate library with default config

    lib.init(log_cfg=pj.LogConfig(level=3, callback=log_cb))

    # Configuring one Transport Object and setting it to listen at 5060 port and UDP protocol

    trans_conf = pj.TransportConfig()

    print("-------------------------LETS START THE REGISTRATION PROCESS----------------------")
    print("\n\n")

    trans_conf.port = 5060  # 5060 is default port for SIP

    # a=input("Please Enter the IP address of the Client: ")
    a = "192.168.0.50"  # Local VM IP
    print("Using the default port number for SIP: 5060")

    trans_conf.bound_addr = a

    transport = lib.create_transport(pj.TransportType.UDP, trans_conf)

    # Starting the instance of Lib class

    lib.start()

    lib.set_null_snd_dev()

    # Configuring Account class to register with Registrar server

    # Giving information to create header of REGISTER SIP message

    # ab4=input("Enter IP address of the Server: ")
    ab4 = "philly.sip.us1.twilio.com"  # Asteriek server IP
    # ab=input("Enter Username: ")
    ab = "gowtham"
    # ab1=input("Enter Password: ")
    ab1 = "Gowtham_password123"
    # ab2=input("Do you want to use the display name same as the username  Y/N ??")
    ab2 = "Y"
    if ab2 == "y" or ab2 == "Y":
        ab3 = ab
    else:
        ab3 = input("Enter Display Name: ")

    acc_conf = pj.AccountConfig(ab4, ab, ab1)

    # registrar = 'sip:'+ab4+':5060', proxy = 'sip:'+ab4+':5060')

    # acc_conf.id ="sip:"+ab

    # acc_conf.reg_uri ='sip:'+ab4+':5060'

    acc_callback = MyAccountCallback(acc_conf)

    acc = lib.create_account(acc_conf)

    # creating instance of AccountCallback class

    acc.set_callback(acc_callback)

    time.sleep(10)
    print('\n')
    print("Registration Complete-----------")
    print(('Status= ', acc.info().reg_status, '(' + acc.info().reg_reason + ')'))

    # If argument is specified then make call to the URI
    if len(sys.argv) > 1:
        lck = lib.auto_lock()
        current_call = make_call(sys.argv[1])
        print('Current call is', current_call)
        del lck

    # # my_sip_uri = "sip:" + transport.info().host + \
    # #              ":" + str(transport.info().port)
    # my_sip_uri = "sip:" + "gowtham@philly.sip.twilio.com" + \
    #              ":" + str(transport.info().port)

    # Menu loop
    while True:
        # print("My SIP URI is", my_sip_uri)
        print("Menu:  m=make call, h=hangup call, a=answer call, q=quit")

        input = sys.stdin.readline().rstrip("\r\n")
        if input == "m":
            if current_call:
                print("Already have another call")
                continue
            print("Enter destination URI to call: ", end=' ')
            input = sys.stdin.readline().rstrip("\r\n")
            if input == "":
                continue
            lck = lib.auto_lock()
            current_call = make_call(input)
            del lck

        elif input == "h":
            if not current_call:
                print("There is no call")
                continue
            current_call.hangup()

        elif input == "a":
            if not current_call:
                print("There is no call")
                continue
            current_call.answer(200)

        elif input == "q":
            break

    # Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error as e:
    print("Exception: " + str(e))
    lib.destroy()
    lib = None
