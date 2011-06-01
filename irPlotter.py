#!/usr/bin/env python
# -- encoding: utf-8 --

import wx
import math
import serial
import sys, glob


ID_TIMER = 1

def scan():
    """scan for available ports. return a list of tuples (num, name)"""
    if sys.platform == 'linux2':
        return  list(glob.glob('/dev/ttyUSB*'))
    else:
        available = []
        for i in range(256):
            try:
                s = serial.Serial("COM" + str(i))
                available.append( s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available




class IrPlotter(wx.Frame):
    def __init__(self, parent, id, title, port):
        wx.Frame.__init__(self, parent, id, title, size=(500, 300))
        
        self.irs = [1023, 1023, 1023, 1023, 1023, 1023, 1023]
        self.max = 0
        
        self.port = port

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show(True)
        
        self.sensorRead()
        self.timer = wx.Timer(self, ID_TIMER)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=ID_TIMER)
        self.timer.Start(300)

    def OnTimer(self, event):
        self.OnPaint()
        self.Refresh()

    def sensorRead(self):
        s = serial.Serial(port, 115200, timeout=1)
        
        # start the sensor output
        s.write(":s;")

        i = 0
        while 1:
            self.Refresh()
            line = s.readline().strip('\n')
            try:
                irs = line.split(' ')
                print self.irs
                if len(irs) == 8:
                    self.irs = irs[:-1]
                    self.max = int(irs[7])
            except:
                continue
            wx.Yield()

    def OnPaint(self, event = None):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#c56c00'))
        dc.SetTextForeground('#ffffff')
	
        k = 0
        for v in self.irs:
            if k == (self.max - 1):
                dc.SetBrush(wx.Brush('#004fc5'))
            else:
                dc.SetBrush(wx.Brush('#c56c00'))
            
            try:               
                dc.DrawRectangle(k*65 + 30, 20, 60,(int(v)/1023.0)*200)
                dc.DrawText(str(k+1) , k*65 + 40, 30)
                dc.DrawText(str(v), k*65 + 40, 240)
            except ValueError:
                pass

            k += 1

       
if __name__ == "__main__":
    print "Available ports: "
    s = scan()   
    for x,y in enumerate(s):
        print "[%d] %s" % (x,y)
    
    if len(s) == 0: print "nothing"

    port = s[input("Select port id: ")]

    app = wx.App(0)
    IrPlotter(None, -1, 'IrPlotter', port=port)
    app.MainLoop()

