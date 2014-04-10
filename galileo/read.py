import nfc
import time
import sys
import mosquitto

def connected(tag):
  try:
    id_vote = tag.ndef.message[0].data
    print tag
    mqttc = mosquitto.Mosquitto("pyt")
    mqttc.connect("127.0.0.1", 1883, 10000)
    global vote
    mqttc.publish('vote', id_vote[-4:] + ' ' + vote, 1)
    print 'Le vote'+vote+' a ete pris en compte'
    time.sleep(3)
    global clf
    clf.connect(rdwr={'on-connect': connected})
    return True
  except:
    print "Unexpected error:", sys.exc_info()[0]
    print 'Erreur dans la prise en compte du vote'
    return True

id1 = sys.argv[1]
vote = sys.argv[2]


clf = nfc.ContactlessFrontend('usb:'+id1)
clf.connect(rdwr={'on-connect': connected})


while True:
  pass
