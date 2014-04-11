import nfc
import sys

def connected(tag):
  global id_num
  sp = nfc.ndef.TextRecord(str(id_num))
  sp.name = 'id'
  tag.ndef.message = nfc.ndef.Message(sp)
  print id_num
  return True

if len(sys.argv) != 2:
  print 'Usage : write_nfc.py [id]'
  exit(0)

id_num = int(sys.argv[1])
clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect': connected})

