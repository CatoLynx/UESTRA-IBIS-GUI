from pyfis.ibis import TCPIBISMaster
from tkinter import *


# Connection to Caracal IBIS WiFi Module
HOST = "192.168.4.1"
PORT = 5001


class UestraGui:
    def __init__(self, ibis_master):
        self.ibis = ibis_master
        self.window = Tk()
        self.window.title("UESTRA IBIS GUI")
        self.window.resizable(False, False)

        self.l_line = Label(self.window, text="Line:")
        self.l_line.grid(row=0, column=0, sticky="NE")

        self.e_line = Entry(self.window, width=32)
        self.e_line.grid(row=0, column=1, columnspan=3, sticky="NW")

        self.dest_entries = []
        for i in range(4):
            l_dest = Label(self.window, text=f"Destination {i+1}:")
            l_dest.grid(row=1+i*2, column=0, sticky="NE")

            t_dest = Text(self.window, height=2, width=32)
            t_dest.grid(row=1+i*2, column=1, rowspan=2, columnspan=3, sticky="NW")

            c_bold_l1_var = IntVar()
            c_bold_l1 = Checkbutton(self.window, text="Line 1 Bold", variable=c_bold_l1_var)
            c_bold_l1.grid(row=1+i*2, column=4, sticky="NW")

            c_bold_l2_var = IntVar()
            c_bold_l2 = Checkbutton(self.window, text="Line 2 Bold", variable=c_bold_l2_var)
            c_bold_l2.grid(row=2+i*2, column=4, sticky="NW")

            c_line_dest_var = IntVar()
            c_line_dest_var.set(1)
            c_line_dest = Checkbutton(self.window, text="Display Line", variable=c_line_dest_var)
            c_line_dest.grid(row=1+i*2, column=5, sticky="NW")

            self.dest_entries.append({
                'l_dest': l_dest,
                't_dest': t_dest,
                'c_bold_l1': c_bold_l1,
                'c_bold_l1_var': c_bold_l1_var,
                'c_bold_l2': c_bold_l2,
                'c_bold_l2_var': c_bold_l2_var,
                'c_line_dest': c_line_dest,
                'c_line_dest_var': c_line_dest_var
            })

        self.l_align = Label(self.window, text="Alignment:")
        self.l_align.grid(row=9, column=0, sticky="NE")

        self.r_align_var = StringVar()
        self.r_align_var.set('M')
        self.r_align_left = Radiobutton(self.window, text="Left", value='L', variable=self.r_align_var)
        self.r_align_left.grid(row=9, column=1, sticky="NW")
        self.r_align_center = Radiobutton(self.window, text="Center", value='M', variable=self.r_align_var)
        self.r_align_center.grid(row=9, column=2, sticky="NW")
        self.r_align_right = Radiobutton(self.window, text="Right", value='R', variable=self.r_align_var)
        self.r_align_right.grid(row=9, column=3, sticky="NW")

        self.l_interval = Label(self.window, text="Interval:")
        self.l_interval.grid(row=10, column=0, sticky="NE")

        self.e_interval = Entry(self.window, width=5)
        self.e_interval.insert(0, "3.0")
        self.e_interval.grid(row=10, column=1, sticky="NW")

        self.b_send = Button(self.window, text="Send", command=self.send)
        self.b_send.grid(row=11, column=0, columnspan=6, sticky="NESW")

    def send(self):
        line_text = self.e_line.get()
        front_text = []
        display_line_text_front = []
        bold_text_front = []
        for entry in self.dest_entries:
            t_dest = entry['t_dest']
            destination = t_dest.get("1.0", "end-1c") # Read from beginning to second to last char (last char would be a newline)
            if not destination:
                continue
            front_text.append(destination)
            display_line_text_front.append(bool(entry['c_line_dest_var'].get()))
            bold_text_front.append(bool(entry['c_bold_l1_var'].get()))
            bold_text_front.append(bool(entry['c_bold_l2_var'].get()))
        text_align_front = self.r_align_var.get()
        display_interval_front = float(self.e_interval.get())
        self.ibis.DS003aUESTRA(
            front_text=front_text,
            line_text=line_text,
            display_line_text_front=display_line_text_front,
            display_interval_front=display_interval_front,
            text_align_front=text_align_front,
            bold_text_front=bold_text_front
        )

    def run(self):
        self.window.mainloop()


def main():
    #master = TCPIBISMaster(HOST, PORT, debug=True)
    master = None
    gui = UestraGui(master)
    gui.run()


if __name__ == "__main__":
    main()
