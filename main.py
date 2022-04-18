from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import pyvisa
import csv


class HP4282A_data_retreive():
    '''
    Short program to retreive data off of the HP4294A Impedance Analyser using a GPIB to USB converter.

    May work on other machines or other interfaces - but that's more relevant to PyVisa than this GUI.
    '''

    def __init__(self):
        self.window = Tk()
        self.window.title(string = 'HP4942A Impedance Analyser - Data Exporter')
        self.window.geometry('400x200')
        # --------------Basic GUI layout -----------------

        # GPIB Instrument Selection
        self.padding0 = Label(text ='\n').grid(row=0)
        self.inst_combo_title = Label(text='Select GPIB Instrument:').grid(row=1,column = 0)
        self.inst_list = list([])
        self.availableInstCombo =ttk.Combobox(self.window, values = self.inst_list, state="readonly")
        self.availableInstCombo.set('Select...')
        self.availableInstCombo.grid(row=1, column = 1)
        self.inst_button = Button(text='Refresh', command = self.populate_avialable_inst)
        self.inst_button.grid(row=1, column = 2)
        self.availableInstCombo.bind('<<ComboboxSelected>>', self.instr_connect)

        # LED for connection
        self.led = Label(self.window, text="    ", bg="red")
        self.led.grid(row=1, column =3)

        # File Saving Interface
        self.padding1 = Label(text='\n').grid(row=2)
        self.combo_title = Label(text='Select File:').grid(row=3,column = 0)
        self.file_list = list([])
        self.availableFileCombo =ttk.Combobox(self.window, values = self.file_list, state="readonly")
        self.availableFileCombo.set('Select...')
        self.availableFileCombo.grid(row=3, column = 1)
        self.button = Button(text='Refresh', command=self.populate_available_files)
        self.button.grid(row=3, column=2)

        # Save Button etc
        self.browse_button = Button(text='Save as', command=self.browse_files).grid(row=4, column=3)
        Label(text='\n').grid(row=4)

        #self.transfer_title = Label(text='Transfer Instrument State:').grid(row=5,column = 1)
        #self.browse_button = Button(text='Select', command=self.write_file).grid(row=5, column=2)
        #Label(text='\n').grid(row=7)

        # PyVisa Controller
        self.rm = pyvisa.ResourceManager() #'@sim' <--- put this in resource manager to simulate PyVisa interface
        self.populate_avialable_inst()


    def populate_avialable_inst(self, *args):
        self.inst_list = self.rm.list_resources()
        self.availableInstCombo['values'] = self.inst_list
        self.availableInstCombo.set('Select...')
        self.availableInstCombo.grid(row=1, column=1)
        try:
            self.inst.close()
            self.led = Label(self.window, text="    ", bg="red")
            self.led.grid(row=1, column=3)
        except:
            pass


    def browse_files(self):
        desired_file = self.availableFileCombo.get()
        file = filedialog.asksaveasfilename(initialfile=desired_file[:-4],
                                        filetypes=[('ASCII, Touchstone file, *.csv', 'csv'),
                                                             ('Binary files *.STA, *.DAT', '.dat'),
                                                             ('Tiff Images, *.TIF', '.tif')])
        self.retrieve_and_save(self.inst, desired_file, file)

    def instr_connect(self, *args):
        desired_inst = self.availableInstCombo.get()
        try:
            self.inst = self.rm.open_resource(desired_inst)
            self.inst.timeout = 200
            self.inst.read_termination = '\n'
            self.inst.write_termination = '\n'
            self.led = Label(self.window, text="    ", bg="green")
            self.led.grid(row=1, column=3)
            self.populate_available_files()
        except:
            self.led = Label(self.window, text="    ", bg="red")
            self.led.grid(row=1, column=3)


    def populate_available_files(self):
        try:
            self.availableFileCombo.set('Select...')
            available_files = []
            file_number = int(self.inst.query('FNUM?'))
            for i in range(1, file_number+1):
                file_name = self.inst.query('FNAME? {}'.format(i))
                available_files.append(file_name)
            self.availableFileCombo['values'] = available_files
            self.availableFileCombo.grid(row=3, column=1)
        except:
            self.led = Label(self.window, text="    ", bg="red")
            self.led.grid(row=1, column=3)

    def retrieve_data(self, inst):
        save_to = []
        file_size = 16384
        while file_size == 16384:
            inst.write('READ?')
            inst.read_bytes(2)
            file_size = int(inst.read_bytes(6))
            new_data = inst.read_bytes(file_size+1)
            save_to.append(new_data[:-1])

        output = b"".join(save_to)
        return output


    def in_memory(self, file):
        try:
            existence = False
            available_files = []
            file_number = int(self.inst.query('FNUM?'))
            for i in range(1, file_number+1):
                file_name = self.inst.query('FNAME? {}'.format(i))
                available_files.append(file_name)

            if file in available_files:
                existence = True

            return existence

        except:
            self.led = Label(self.window, text="    ", bg="red")
            self.led.grid(row=1, column=3)

    def write_file(self):
        '''
        Sends a file to the HP4294a instrument
        '''
        file = filedialog.askopenfilename(filetypes=[('Binary files *.STA, *.DAT', '.dat')])
        name = file.split('/')[-1]
        prefix = name[:-4]
        suffix = name[-4:]
        if len(prefix) > 8:
            prefix = prefix[:8]

        name = prefix+suffix
        write_confirmation = True
        # Check if the desired file exist in memory already and ask the user to confirm overwrite access
        if self.in_memory(name):
            write_confirmation = messagebox.askyesno("File already exists",
                                                         "This file name exist on the 4294a internal memory. Do you want to overwrite?")

        if write_confirmation:
            self.inst.write('STOD {FLASH}')
            self.inst.write('PURG \'{}\''.format(name)) # if user confirms overwrite, delete the file,# and create another
            self.inst.write('WOPEN \'{}\''.format(name)) # and then create another file with write privaledges
            f = open(file, 'rb')
            complete_data = f.read()

            # this code breaks a file bigger than 16 kB up and sends it as packets
            chunk_size = 16384
            while chunk_size == 16384:
                chunk_size = len(complete_data)
                if chunk_size > 16384:
                    chunk_size = 16384
                    chunk = bytearray(complete_data[:16384])
                    complete_data = complete_data[16384:]
                else:
                    chunk = bytearray(complete_data)
                chunk_str = str(chunk_size)
                while len(chunk_str) < 5:
                    chunk_str = '0' + chunk_str

                #chunk = str(int.from_bytes(chunk, 'big'))
                header = '#60' + chunk_str
                #self.inst.write('WRITE {}'.format(header))
                #print(help(self.inst.write_binary_values))
                self.inst.write_binary_values(header, chunk, datatype='s')

            self.inst.write('CLOSE')

    def retrieve_and_save(self, instr, desired_file, file_target):
        # opens the desired data file and downloads it into a list
        self.inst.write('ROPEN \'{}\''.format(desired_file))
        data = self.retrieve_data(instr)
        self.inst.write('CLOSE')
    
        if desired_file[-4:] == '.TXT' or desired_file[-4:] == '.S1P':
            data = data.decode('UTF-8')
            data = data.split('\n')
            # Writes that data structure into a csv file
            suffix = desired_file[-4:]
            file = open(file_target+suffix, 'w', newline = '')
            writer = csv.writer(file, delimiter = ',')
            for line in data:
                l2 = line.replace('\"','').replace("\r",'')
                writer.writerow(l2.split('\t'))
            file.close()

        elif desired_file[-4:] == '.DAT' or desired_file[-4:] == '.STA' or desired_file[-4:] == '.TIF':
            suffix = desired_file[-4:]
            file = open(file_target+suffix, 'wb')
            file.write(data)
            file.close()

            

# -------------------running the GUI--------------------
GUI = HP4282A_data_retreive()
GUI.window.mainloop()
