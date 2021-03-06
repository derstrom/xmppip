#!/usr/bin/python
# -*- coding: utf-8 -*-

'''ipbot- IP address to jabber bot.      
licence GPL v.3'''

import xmpp
import urllib2
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/xmppip.conf')

# work with cfg
user=(config.get('account', 'login'))
password=(config.get('account', 'password'))
presence=(config.get('presence','presence'))

jid=xmpp.protocol.JID(user)
client=xmpp.Client(jid.getDomain())
client.connect()
client.auth(jid.getNode(),password)

# recieving internet ip-address
strURL='http://api.wipmania.com/'
f = urllib2.urlopen(urllib2.Request(strURL))
response = f.read()
ipget = response.split()
f.close()

def status(xstatus):
    status=xmpp.Presence(status=xstatus,show=presence,priority='1')
    client.send(msging)

def message(conn,mess):
    global client
    if ( mess.getBody() == "ip" ):
        client.send(xmpp.Message(mess.getFrom(),ipget))

client.RegisterHandler('message',message)
client.RegisterDisconnectHandler(client.reconnectAndReauth())
client.sendInitPresence()

while True:
    client.Process(1)
