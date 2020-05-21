from tkinter import *
from tkinter.ttk import *

tk = Tk()


def createFuctionWindow():
    nw = Toplevel(tk)
    frame1 = Frame(nw, padding=10)
    frame1.pack()
    l1 = Label(frame1, text="Slave ID")
    t1 = Text(frame1, height=1, width=10)
    b1 = Button(frame1, text="OK")
    b1.grid(row=0, column=2, padx=5, pady=2)
    l2 = Label(frame1, text="Function")
    text1 = "03 Read Holding Registers(4x)"
    c2 = Combobox(frame1, state="disabled", value=(text1,), width=len(text1))
    c2.current(0)
    b2 = Button(frame1, text="Cancel", command=lambda: nw.destroy())
    b2.grid(row=1, column=2, padx=5, pady=2)
    l3 = Label(frame1, text="Address")
    t3 = Text(frame1, height=1, width=10)
    l4 = Label(frame1, text="Quantity")
    t4 = Text(frame1, height=1, width=10)
    l5 = Label(frame1, text="Scan Rate")
    t5 = Text(frame1, height=1, width=10)
    b5 = Button(frame1, text="Apply")
    b5.grid(row=4, column=2, padx=5, pady=2)
    labels = [l1, l2, l3, l4, l5]
    inputs = [t1, c2, t3, t4, t5]
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
    b1 = Button(f1, text="OK")
    b1.grid(row=0,column=1,padx=10)
    b2 = Button(f1, text="Cancel")
    b2.grid(row=1,column=1,padx=10)
    lf2 = LabelFrame(nw, text="Remote Modbus Server", padding=10)
    lf2.pack(side=TOP)
    l1 = Label(lf2, text="IP Address or Node Name")
    l1.grid(row=0, column=0, columnspan=3, sticky=W)
    cb2 = Combobox(lf2)
    cb2.grid(row=1, column=0, columnspan=3, sticky=W)
    l2 = Label(lf2, text="Server Port")
    l2.grid(row=2, column=0)
    l3 = Label(lf2, text="Connect Timeout")
    l3.grid(row=2, column=1)
    t2 = Text(lf2, width=10, height=1)
    t2.grid(row=3, column=0)
    t3 = Text(lf2, width=10, height=1)
    t3.grid(row=3, column=1)
    rb1 = Radiobutton(lf2, text="IPv4", value=0)
    rb2 = Radiobutton(lf2, text="IPv6", value=1)
    rb1.grid(row=2, column=2)
    rb2.grid(row=3, column=2)


frame1 = Frame(tk)
frame1.pack()
btn1 = Button(frame1, text="START", command='')
btn1.pack(side="left", pady=30, padx=30)
btn2 = Button(frame1, text="CONNECT", command=createConnectionWindow)
btn2.pack(side="left", padx=30)
btn3 = Button(frame1, text="FUNCTION", command=createFuctionWindow)
btn3.pack(side="left", padx=30)
tk.wm_title("MODBUS POLLING")
tk.geometry("800x600")
tk.mainloop()
