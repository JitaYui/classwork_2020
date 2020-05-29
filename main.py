from tkinter import *
from tkinter import StringVar
from tkinter.ttk import *
import time
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md



tk = Tk()
ip = StringVar()
slaid = IntVar()
addr = IntVar()
quan = IntVar()
#rate = IntVar()
port = IntVar()
timeout = IntVar()
"""reset"""


def createFuctionWindow():
    nw = Toplevel(tk)
    frame1 = Frame(nw, padding=10)
    frame1.pack()
    l1 = Label(frame1, text="Slave ID")
    t1 = Entry(frame1, textvariable=slaid)
    b1 = Button(frame1, text="OK")
    b1.grid(row=0, column=2, padx=5, pady=2)
    l2 = Label(frame1, text="Function")
    text1 = "03 Read Holding Registers(4x)"
    c2 = Combobox(frame1, state="disabled", value=(text1,), width=len(text1))
    c2.current(0)
    b2 = Button(frame1, text="Cancel", command=lambda: nw.destroy())
    b2.grid(row=1, column=2, padx=5, pady=2)
    l3 = Label(frame1, text="Address")
    t3 = Entry(frame1, textvariable=addr)
    l4 = Label(frame1, text="Quantity")
    t4 = Entry(frame1, textvariable=quan)
    #l5 = Label(frame1, text="Scan Rate")
    #t5 = Entry(frame1, textvariable=rate)
    b5 = Button(frame1, text="Apply")
    b5.grid(row=4, column=2, padx=5, pady=2)
    labels = [l1, l2, l3, l4]
    inputs = [t1, c2, t3, t4]
    for l in labels:
        l.grid(row=labels.index(l), column=0, padx=5, pady=2)
    for i in inputs:
        i.grid(row=inputs.index(i), column=1, padx=5, pady=2, sticky=W)



def createConnectionWindow():
    nw = Toplevel(tk)
    f1 = Frame(nw)
    f1.pack()
    lf1 = LabelFrame(f1, text="Connection", padding=10)
    lf1.grid(row=0,column=0,rowspan=2)
    cb1 = Combobox(lf1, state="disabled", value=("Modbus TCP/IP",), )
    cb1.current(0)
    cb1.pack()
    b1 = Button(f1, text="OK", command= lambda: nw.destroy() )
    b1.grid(row=0,column=1,padx=10)
    b2 = Button(f1, text="Cancel", command= lambda: nw.destroy() )
    b2.grid(row=1,column=1,padx=10)
    lf2 = LabelFrame(nw, text="Remote Modbus Server", padding=10)
    lf2.pack(side=TOP)
    l1 = Label(lf2, text="IP Address or Node Name")
    l1.grid(row=0, column=0, columnspan=3, sticky=W)
    #cb2 = Entry(lf2)
    #cb2.grid(row=1, column=0, columspan=3, sticky=W)
    cb2 = Combobox(lf2, textvariable=ip)
    cb2.grid(row=1, column=0, columnspan=3, sticky=W)
    l2 = Label(lf2, text="Server Port")
    l2.grid(row=2, column=0)
    l3 = Label(lf2, text="Connect Timeout")
    l3.grid(row=2, column=1)
    t2 = Entry(lf2, textvariable=port)
    t2.grid(row=3, column=0)
    t3 = Entry(lf2, textvariable=timeout)
    t3.grid(row=3, column=1)
    rb1 = Radiobutton(lf2, text="IPv4", value=0)
    rb2 = Radiobutton(lf2, text="IPv6", value=1)
    rb1.grid(row=2, column=2)
    rb2.grid(row=3, column=2)

def Modbus():
    IP = ip.get()
    SLAID = slaid.get()
    ADDR = addr.get()
    QUAN = quan.get()
    # RATE = rate.get()
    PORT = port.get()
    TIMEOUT = timeout.get() / 1000
    # Modbus_polling
    master = mt.TcpMaster(IP, PORT)
    master.set_timeout(TIMEOUT)
    if SLAID=="" or IP == "" or ADDR == "" or QUAN == "" or PORT== "" or TIMEOUT == "":

        print("error")
        F1 = "error"
    else:
        while True:
            F1 = master.execute(slave=SLAID, function_code=md.READ_HOLDING_REGISTERS, starting_address=ADDR,
                                quantity_of_x=QUAN)
            print(F1)  # 取到的所有寄存器的值
            time.sleep(1)


#Function



frame1 = Frame(tk)
frame1.pack()
t = Text(frame1, height=20)
t.pack(side='bottom')
btn1 = Button(frame1, text="START", command=Modbus)
btn1.pack(side="left", pady=40, padx=60)
btn2 = Button(frame1, text="CONNECT", command=createConnectionWindow)
btn2.pack(side="left", padx=40)
btn3 = Button(frame1, text="FUNCTION", command=createFuctionWindow)
btn3.pack(side="left", padx=40)

tk.wm_title("MODBUS POLLING")
tk.geometry("800x600")
tk.mainloop()






