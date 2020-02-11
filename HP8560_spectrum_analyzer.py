import time

class spectrum_analyzer_hp8560(object):
    '''Class deffinition for HP8560A Spectrum Analyzer'''
    def __init__(self, visa_address):
        self.rm = visa.ResourceManager()
        self.spectrum_analyzer_hp8560 = self.rm.open_resource(visa_address)
        instrument_id = self.spectrum_analyzer_hp8560.query('ID?').encode("utf-8").rstrip()
        print "Communicating with: " + instrument_id
        
        return

    def default_setup(self):
        '''Reset spectrum_analyzer_hp8560 to default'''
        self.spectrum_analyzer_hp8560.clear()

    def read_freq_ctrl(self,code):
        '''
        See page 5-9 in the Operation and Programming Manual for more ...
        
        Code:
        FA: Start Frequency
        FB: Stop Frequency
        CF: Center frequency
        SS: Center Frequency Step
        SP: Span
        '''
        return float(self.spectrum_analyzer_hp8560.query(code+'?').encode("utf-8").rstrip())

    def set_measurement_range(self, startFreq = None, stopFreq = None, centerFreq=None, 
                                  centerFreqStep = None, span=None, verbose=True):
        '''Set measurement frequency range'''
        time.sleep(1)
        if not(startFreq == None):
            self.spectrum_analyzer_hp8560.write('FA '+str(int(startFreq))+'HZ');
        if not(stopFreq == None):
            self.spectrum_analyzer_hp8560.write('FB '+str(int(stopFreq))+'HZ');            
        if not(centerFreq == None):
            self.spectrum_analyzer_hp8560.write('CF '+str(int(centerFreq))+'HZ');
        if not(centerFreqStep == None):
            self.spectrum_analyzer_hp8560.write('SS '+str(int(centerFreqStep))+'HZ');
        if not(span == None):
            self.spectrum_analyzer_hp8560.write('SP '+str(int(span))+'HZ');
        
        if verbose:
            print ("Start Frequency = {} Hz".format(self.read_freq_ctrl('FA')))
            print ("Stop Frequency = {} Hz".format(self.read_freq_ctrl('FB')))
            print ("Center Frequency = {} Hz".format(self.read_freq_ctrl('CF')))
            print ("Center Frequency Step = {} Hz".format(self.read_freq_ctrl('SS')))
            print ("Span = {} Hz".format(self.read_freq_ctrl('SP')))

    def read_spectrum(self,frequency):
        '''
        Inputs:  Frequency:  value on the frequency axis
        Returns: Amplitude (dB) of the spectrum at the specified frequency
        '''
        self.spectrum_analyzer_hp8560.write('MKN '+str(frequency))
        return float(self.spectrum_analyzer_hp8560.query('MKA?').encode("utf-8").rstrip())

    def center_around_peak(self, verbose=True):
        '''Comment'''
        for i in range(2):
            self.spectrum_analyzer_hp8560.write('MKPK')
            time.sleep(1.5)
            self.spectrum_analyzer_hp8560.write('MKCF')
            time.sleep(1.5)
        if verbose: 
            print ("Maximum peak detected at {} Hz with amplitude of {} dBm".format(self.read_freq_ctrl('CF'),(self.read_marker_amplitude())))
        CF = (self.read_freq_ctrl('CF')+self.read_freq_ctrl('CF')+self.read_freq_ctrl('CF'))/3
        AMP= (self.read_marker_amplitude()+self.read_marker_amplitude()+self.read_marker_amplitude())/3
        return [CF,AMP]

    def set_marker_freq(self,frequency):
        '''Comment'''
        self.spectrum_analyzer_hp8560.write('MKN '+str(frequency))

    def read_marker_amplitude(self):
        '''Comment'''
        return float(self.spectrum_analyzer_hp8560.query('MKA?').encode("utf-8").rstrip())

    def set_marker_avg(self,state=0):
        '''Turns On/Off video averaging (0/1)'''
        self.spectrum_analyzer_hp8560.write('MKNOISE {};'.format(state))

    def toggle_v_avg(self):
        '''Turns On/Off video averaging'''
        self.spectrum_analyzer_hp8560.write('VAVG')

    def check_if_done(self):
        while (int(self.spectrum_analyzer_hp8560.query('DONE?').encode("utf-8").rstrip())==0):
            continue

        
