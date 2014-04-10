import nfc
import sys

def connected(tag):
  global id_num
  sp = nfc.ndef.TextRecord(str(id_num))
  sp.name = 'id'
  tag.ndef.message = nfc.ndef.Message(sp)
  print id_num
  return True

'''
clf = nfc.ContactlessFrontend('usb')

tag = clf.connect(rdwr={'on-connect': connected})


#if tag.ndef
'''
id_num = int(sys.argv[1])
clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect': connected})

#sp = nfc.ndef.TextRecord('Antoine Gervail', language='fr')
#sp.name = 'name'
#sp = nfc.ndef.TextRecord(sys.argv[1])
#sp.name = 'id'
#import ipdb;ipdb.set_trace()
#sp2 = nfc.ndef.TextRecord('Grenoble', language='fr')

#tag.ndef.message = nfc.ndef.Message(sp)
#tag.ndef.message = nfc.ndef.Message(sp, sp2)
#print nfc.ndef.SmartPosterRecord(tag.ndef.message[0]).pretty()


