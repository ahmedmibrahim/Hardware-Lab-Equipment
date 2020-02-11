# Necessary packages
import visa, time

class Tektronix(object):

    def __init__(self, visa_address="USB::0x0000::0x0000::B000000::INSTR"):
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(visa_address)
        print("Talking to " + str(self.scope.query('*idn?')))
        self.scope.timeout = 10000

    def default(self):
        self.scope.write('*rst')                # reset
        self.scope.query('*opc?')               # sync
        self.scope.write("CLS")                 # clear
        self.scope.query('*opc?')               # sync
        self.scope.write('autoset EXECUTE')     # autoset
        self.scope.query('*opc?')               # sync

        return

    def clear(self):
        self.scope.write('CLEAR ALL')     # clear

        return

    def recall_setup(self, setup_file=r"TEK00000.SET", setup_dir=r"C:\SetupFile"):
        self.scope.write("RECALL:SETUP \'{}\'".format(setup_dir + "\\" + setup_file))
        self.scope.query('*opc?')               # sync
        print ('Scope Setup File Loaded')

        return

    def set_acquisition_state(self, state="RUN"):
        '''Sets the acquistion state of the scope: RUN, STOP'''
        self.scope.write("ACQ:STATE {}".format(state))

        return

    def aquire(self, state="run_stop"):
        '''Equivilant to pressing scope button:: RUN/STOP, SINGLE'''
        if state.lower() == "run_stop":
            self.scope.write("ACQUIRE:STOPAFTER RUNSTOP")
        elif state.lower() == "single":
            self.scope.write("ACQUIRE:STOPAFTER SEQUENCE")

        return

    def set_sampling_rate(self, rate=50E9):
        self.scope.write(":HOR:MODE:SAMPLER {}".format(rate))

        return

    def set_record_length(self, length=100000):
        '''Set record length'''
        self.scope.write("HORizontal:RECOrdlength {}".format(length))

        return

    def set_average_count(self, count):
        '''Set number of waves to use per average'''
        self.scope.write("ACQuire:NUMAVg {}".format(count))
        self.scope.write("ACQuire:MODe AVErage")

        return

    def read_measurment(self):
        self.scope.write("MEASUrement:STATIstics:COUNt {RESET}")
        self.scope.write("ACQ:STOPAFTER {}".format("SEQ"))
        self.set_acquisition_state(state=1)
        self.scope.write("MEASUrement:STATIstics:COUNt {RESET}")

        return

        return measurment

    def dpojet_read_measurment(self, index):
        min = float(self.scope.query('DPOJET:MEAS{}:RESULTS:ALLAcqs:MIN?'.format(index)))
        mean = float(self.scope.query('DPOJET:MEAS{}:RESULTS:ALLAcqs:MEAN?'.format(index)))
        max = float(self.scope.query('DPOJET:MEAS{}:RESULTS:ALLAcqs:MAX?'.format(index)))

        return {'min': min, 'mean': mean, 'max': max}

    def dpojet_state(self, state):
        """ DPOJET:STATE {RUN | SINGLE | RECALC | CLEAR | STOP} """
        self.scope.write('DPOJET:STATE {}'.format(state))

        return

    def dpojet_meas_start(self, state):
        """ DPOJET:STATE {RUN | SINGLE} """
        self.scope.write('DPOJET:STATE CLEAR')
        time.sleep(2)
        self.scope.write('DPOJET:STATE {}'.format(state))
        if state == "SINGLE":
            while self.scope.query('DPOJET:STATE?')[:-1] == "RUN":
                time.sleep(2)

        return
