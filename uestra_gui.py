import json

from pyfis.ibis import TCPIBISMaster
from tkinter import *


# Connection to Caracal IBIS WiFi Module
HOST = "192.168.4.1"
PORT = 5001

# Path to preset file
PRESET_FILE = "presets.json"


class UestraGui:
    def __init__(self, ibis_master):
        self.ibis = ibis_master
        self.presets = []

        self.window = Tk()
        self.window.title("UESTRA IBIS GUI")
        self.window.resizable(False, False)

        self.l_line = Label(self.window, text="Line:")
        self.l_line.grid(row=0, column=0, sticky="NE")

        self.e_line_var = StringVar()
        self.e_line = Entry(self.window, width=32, textvariable=self.e_line_var)
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

        self.e_interval_var = StringVar()
        self.e_interval_var.set("3.0")
        self.e_interval = Entry(self.window, width=5, textvariable=self.e_interval_var)
        self.e_interval.grid(row=10, column=1, sticky="NW")

        self.b_send = Button(self.window, text="Send", command=self.send)
        self.b_send.grid(row=11, column=0, columnspan=6, sticky="NESW")

        self.l_save_preset = Label(self.window, text="Save preset as:")
        self.l_save_preset.grid(row=12, column=0, sticky="NE")

        self.e_preset_name = Entry(self.window, width=32)
        self.e_preset_name.grid(row=12, column=1, columnspan=3, sticky="NW")

        self.b_save_preset = Button(self.window, text="Save", command=self.add_preset)
        self.b_save_preset.grid(row=12, column=4, sticky="NE")

        self.load_presets()

    def get_data(self):
        data = {}
        data['line_text'] = self.e_line_var.get()
        data['front_text'] = []
        data['display_line_text_front'] = []
        data['bold_text_front'] = []
        for entry in self.dest_entries:
            t_dest = entry['t_dest']
            destination = t_dest.get("1.0", "end-1c") # Read from beginning to second to last char (last char would be a newline)
            if not destination:
                continue
            data['front_text'].append(destination)
            data['display_line_text_front'].append(bool(entry['c_line_dest_var'].get()))
            data['bold_text_front'].append(bool(entry['c_bold_l1_var'].get()))
            data['bold_text_front'].append(bool(entry['c_bold_l2_var'].get()))
        data['text_align_front'] = self.r_align_var.get()
        data['display_interval_front'] = float(self.e_interval_var.get())
        return data

    def set_data(self, data):
        self.e_line_var.set(data['line_text'])
        data['front_text'] += [""] * (4 - len(data['front_text']))
        for i, text in enumerate(data['front_text']):
            self.dest_entries[i]['t_dest'].delete("1.0", END)
            self.dest_entries[i]['t_dest'].insert("1.0", text)
        data['display_line_text_front'] += [True] * (4 - len(data['display_line_text_front']))
        for i, display_line in enumerate(data['display_line_text_front']):
            self.dest_entries[i]['c_line_dest_var'].set(int(display_line))
        data['bold_text_front'] += [False] * (8 - len(data['bold_text_front']))
        for i in range(0, len(data['bold_text_front']), 2):
            self.dest_entries[i//2]['c_bold_l1_var'].set(int(data['bold_text_front'][i]))
            self.dest_entries[i//2]['c_bold_l2_var'].set(int(data['bold_text_front'][i+1]))
        self.r_align_var.set(data['text_align_front'])
        self.e_interval_var.set(str(data['display_interval_front']))

    def send(self):
        data = self.get_data()
        self.ibis.DS003aUESTRA(**data)

    def add_preset(self):
        preset = {'name': self.e_preset_name.get()}
        preset.update(self.get_data())
        self.presets.append({'b_apply': None, 'b_delete': None, 'data': preset})
        self.save_presets()
        self.load_presets()

    def apply_preset(self, index):
        self.set_data(self.presets[index]['data'])

    def delete_preset(self, index):
        if self.presets[index]['b_apply'] is not None:
            self.presets[index]['b_apply'].destroy()
        if self.presets[index]['b_delete'] is not None:
            self.presets[index]['b_delete'].destroy()
        self.presets.pop(index)
        self.save_presets()
        self.load_presets()

    def save_presets(self):
        data = {'presets': [preset['data'] for preset in self.presets]}
        with open(PRESET_FILE, 'w') as f:
                data = json.dump(data, f, sort_keys=True, indent=4)

    def load_presets(self):
        try:
            with open(PRESET_FILE, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        # Remove any existing buttons
        for preset in self.presets:
            if preset['b_apply'] is not None:
                preset['b_apply'].destroy()
            if preset['b_delete'] is not None:
                preset['b_delete'].destroy()

        self.presets = []
        for i, preset in enumerate(data['presets']):
            b_apply_preset = Button(self.window, text=preset['name'], command=lambda j=i:self.apply_preset(j))
            b_apply_preset.grid(row=13+i, column=0, columnspan=5, sticky="NESW")
            b_delete_preset = Button(self.window, text="Delete", command=lambda j=i:self.delete_preset(j))
            b_delete_preset.grid(row=13+i, column=5, sticky="NESW")
            self.presets.append({'b_apply': b_apply_preset, 'b_delete': b_delete_preset, 'data': preset.copy()})

    def run(self):
        self.window.mainloop()


def main():
    master = TCPIBISMaster(HOST, PORT, debug=True)
    gui = UestraGui(master)
    gui.run()


if __name__ == "__main__":
    main()
