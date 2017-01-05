#!/usr/bin/python
# Needs a command line argument in following format getCertInfo.py www.example.com 
import sys
import socket
import string
import os
import commands
from M2Crypto import SSL

def reportIP(IPaddress):
   ctx = SSL.Context()
   ctx.set_allow_unknown_ca(True)
   ctx.set_verify(SSL.verify_none, 1)
   conn = SSL.Connection(ctx)
   conn.postConnectionCheck = None
   timeout = SSL.timeout(15)
   conn.set_socket_read_timeout(timeout)
   conn.set_socket_write_timeout(timeout)
   try:
      sys.stderr.write('Connecting '+IPaddress+'. ')
      sys.stderr.flush()
      conn.connect((IPaddress, 443))
   except:
      print IPaddress+"|{SSL_HANDSHAKE_FAILED}|"+"|"+"|"+"|"
      sys.stderr.write('failed.\n')
      sys.stderr.flush()
      return
   sys.stderr.write('Getting cert info. ')
   sys.stderr.flush()

   cert = conn.get_peer_cert()
   try:
      cissuer = cert.get_issuer().as_text()
   except:
      sys.stderr.write("Error:  No Valid Cert Presented\n");
      print IPaddress+"|{NO_CERT_PRESENTED}|"+"|"+"|"+"|"
      sys.stderr.flush
      conn.close
      return

   sys.stderr.write('done\n')
   sys.stderr.flush()
      
   csubject = cert.get_subject().as_text()
   try:
      cAltName = cert.get_ext('subjectAltName').get_value()
   except LookupError:
      cAltName = ""
   try:
      cCN = cert.get_subject().CN
   except AttributeError:
      cCN = ""
   try:
      cExpiry = str(cert.get_not_after())
   except AttributeError:
      cExpiry = ""
   conn.close
   pubkey = cert.get_pubkey()
   print '***********Report**********'
   print 'Cert Hostname: '+ cCN
   print 'Expiry Date: '+cExpiry
   print 'Public Key Size:' + str(pubkey.size())
   cmd='openssl s_client -connect ' + sys.argv[1] +':443 < /dev/null 2>/dev/null | openssl x509 -text -in /dev/stdin | grep \"Signature Algorithm\"| uniq -c|awk -F\' \' \'{print $4}\''
   status, output = commands.getstatusoutput(cmd)
   print 'Encrypttion: ' + output
reportIP(sys.argv[1])

