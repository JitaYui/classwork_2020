from tkinter import *
from tkinter import StringVar
from tkinter.ttk import *
import time
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import pymysql
from threading import Thread

tk = Tk()
ip = StringVar()
slaid = IntVar()
slaid.set(1)
addr = IntVar()
addr.set(18176)
quan = IntVar()
quan.set(2)
# rate = IntVar()
port = IntVar()
port.set(502)
timeout = IntVar()
timeout.set(1000)
tvar = StringVar()

def createFunctionWindow():
    nw = Toplevel(tk)
    frame1 = Frame(nw, padding=10)
    frame1.pack()
    l1 = Label(frame1, text="Slave ID")
    t1 = Entry(frame1, textvariable=slaid)
    b1 = Button(frame1, text="OK", command=lambda: nw.destroy())
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
    # l5 = Label(frame1, text="Scan Rate")
    # t5 = Entry(frame1, textvariable=rate)
    #b5 = Button(frame1, text="Apply")
    #b5.grid(row=4, column=2, padx=5, pady=2)
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
    lf1.grid(row=0, column=0, rowspan=2)
    cb1 = Combobox(lf1, state="disabled", value=("Modbus TCP/IP",), )
    cb1.current(0)
    cb1.pack()
    b1 = Button(f1, text="OK", command=lambda: nw.destroy())
    b1.grid(row=0, column=1, padx=10)
    b2 = Button(f1, text="Cancel", command=lambda: nw.destroy())
    b2.grid(row=1, column=1, padx=10)
    lf2 = LabelFrame(nw, text="Remote Modbus Server", padding=10)
    lf2.pack(side=TOP)
    l1 = Label(lf2, text="IP Address or Node Name")
    l1.grid(row=0, column=0, columnspan=3, sticky=W)
    # cb2 = Entry(lf2)
    # cb2.grid(row=1, column=0, columspan=3, sticky=W)
    cb2 = Combobox(lf2, textvariable=ip, value=('172.20.10.3',))
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


class TModbus(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.IP = ip.get()
        self.SLAID = slaid.get()
        self.ADDR = addr.get()
        self.QUAN = quan.get()
        self.PORT = port.get()
        self.TIMEOUT = timeout.get() / 1000

        pass

    def run(self):
        master = mt.TcpMaster(self.IP, self.PORT)
        master.set_timeout(self.TIMEOUT)
        # if SLAID == "" or IP == "" or ADDR == "" or QUAN == "" or PORT == "" or TIMEOUT == "":
        #     print("error")
        #     F1 = "error"
        tTitle = "DATE        TIME        TEMP."
        Ttemp = [tTitle]
        while True:
            F1 = master.execute(slave=self.SLAID, function_code=md.READ_HOLDING_REGISTERS, starting_address=self.ADDR,
                                quantity_of_x=self.QUAN)
            print(F1)  # 取到的所有寄存器的值
            print(float(F1[0] / 10))
            tmp = float(F1[0] / 10)
            tt = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            x = tt.split(" ")
            date = x[0]
            Time = x[1]
            Ttemp.append(tt + '   ' + str(tmp) )
            if len(Ttemp) > 11:
                Ttemp.pop(1)
            s = ''
            for i in Ttemp:
                s += i
                s += '\n'
            tvar.set(s)

            db = pymysql.connect(host='172.20.10.4', user='userj', password='1qazXSW@', port=3306, db='temperature')

            with db.cursor() as cursor:

                sql = 'INSERT INTO temp01(date, Time, Temperature) values(%s, %s, %s)'
                try:
                    cursor.execute(sql, (date, Time, tmp))
                    db.commit()
                except Exception as e:
                    print(e)
                time.sleep(1)

def Modbus():
    tmodbus = TModbus()
    tmodbus.start()
# Function


def Test():
    db = pymysql.connect(host='172.20.10.4', user='userj', password='1qazXSW@', port=3306, db='temperature')
    with db.cursor() as cursor:
        sql = 'SELECT * from temp01'
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)


frame1 = Frame(tk)
frame1.pack()
t = Label(frame1, textvariable=tvar, background='white', relief=SUNKEN)
t.pack(side='bottom')
btn1 = Button(frame1, text="START", command=Modbus)
btn1.pack(side="left", pady=40, padx=40)
btntemp = Button(frame1, text="FETCH", command=Test)
btntemp.pack(side="left", padx=40)
btn2 = Button(frame1, text="CONNECT", command=createConnectionWindow)
btn2.pack(side="left", padx=40)
btn3 = Button(frame1, text="FUNCTION", command=createFunctionWindow)
btn3.pack(side="left", padx=40)

tk.wm_title("MODBUS POLLING")
tk.geometry("800x400")
tk.mainloop()

