"""

 ~ Neurorack project ~
 Audio : Class for the audio handling
 
 This class contains all audio-processing stuff in the Neurorack.
     - Instantiates the deep model
     - Provides callbacks for playing
         play_noise
         play_model
 
 Author               : Philippe Esling, Ninon Devis, Martin Vert
                        <{esling, devis}@ircam.fr>

"""

import numpy as np
import sounddevice as sd
from parallel import ProcessInput
from models.ddsp import DDSP

class Audio(ProcessInput):
    '''
        The Audio class handles every aspect related to audio generation.
        It is based on the ProcessInput system for multiprocessing
    '''

    def __init__(self, 
                 model: str = 'ddsp', 
                 sr: int = 22050):
        '''
            Constructor - Creates a new instance of the Audio class.
            Parameters:
                model:      [str], optional
                            Specify the audio model to load [default : 'ddsp']
                sr:         int, optional
                            Specify the sampling rate [default: 22050]
        '''
        super().__init__('audio')
        # Configure audio
        self.sr = sr
        # Set devices default
        self.set_defaults()
        self.model_name = model
        # Set model
        if (model == 'ddsp'):
            self.model = DDSP()
        else:
            raise NotImplementedError
    
    def set_defaults(self):
        """
            Sets default parameters for the soundevice library.
            See 
        """
        sd.default.samplerate = self.sr
        sd.default.device = 1
        sd.default.latency = 'low'
        sd.default.dtype = 'float32'
        sd.default.blocksize = 0
        sd.default.clip_off = False
        sd.default.dither_off = False
        sd.default.never_drop_input = False

    def play_noise(self, wait: bool = True, length: float = 4.0):
        '''
            Play some random noise of a given length for checkup.
            Parameters:
                wait:       [bool], optional
                            Wait on the end of the playback
                length:     [float], optional
                            Length of signal to generate (in seconds)
        '''
        audio = np.random.randn(length * self.sr)
        sd.play(audio, self.sr)
        if (wait):
            self.wait_playback()

    def play_model(self, wait: bool = True):
        '''
            Play some random noise of a given length for checkup.
            Parameters:
                wait:       [bool], optional
                            Wait on the end of the playback
        '''
        audio = self.model.generate_random()
        sd.play(audio, self.sr)
        if (wait):
            self.wait_playback()
            
    def input_through(self, length: float = 4.0):
        '''
            Play some random noise of a given length for checkup.
            Parameters:
                wait:       [bool], optional
                            Wait on the end of the playback
                length:     [int], optional
                            Length of signal to generate (in seconds)
        '''
        def callback(indata, outdata, frames, time, status):
            if status:
                print(status)
            outdata[:] = indata
        with sd.Stream(channels=2, callback=callback):
            sd.sleep(int(length * 1000))
            
    def play_sine_block(self, amplitude=1.0, frequency=440.0):
        '''
            Play a sinus signal 
            Parameters:
                amplitude:  [float], optional
                            Amplitude of the sinusoid
                length:     [int], optional
                            Length of signal to generate (in seconds)
        '''
        def callback(outdata, frames, time, status):
            if status:
                print(status)
            global start_idx
            t = (start_idx + np.arange(frames)) / self.sr
            t = t.reshape(-1, 1)
            outdata[:] = amplitude * np.sin(2 * np.pi * frequency * t)
            start_idx += frames
    
        with sd.OutputStream(device=sd.default.device, channels=1, callback=callback,
                             samplerate=self.sr):
            input()
            
    def plot_text_spectrogram(self, columns=6, block_duration=50, f_range=[100, 2000]):
        high, low = f_range
        delta_f = (high - low) / (columns - 1)
        fftsize = np.ceil(self.sr / delta_f)
        low_bin = np.floor(low / delta_f)
        def callback(indata, frames, time, status):
            if status:
                text = ' ' + str(status) + ' '
                print('\x1b[34;40m', text.center(columns, '#'),
                      '\x1b[0m', sep='')
            if any(indata):
                magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
                magnitude *= 1.0 / fftsize
                line = (';'
                        for x in magnitude[low_bin:low_bin + columns])
                print(*line, sep='', end='\x1b[0m\n')
            else:
                print('no input')

        with sd.InputStream(device=sd.default.device, channels=1, callback=callback,
                            blocksize=int(self.sr * block_duration / 1000),
                            samplerate=self.sr):
            while True:
                response = input()
                print(response)
        
    def stop_playback(self):
        ''' Stop any ongoing playback '''
        sd.stop()
        
    def wait_playback(self):
        ''' Wait on eventual playback '''
        sd.wait()
    
    def get_status(self):
        ''' Get info about over/underflows (play() or rec()) '''
        return sd.get_status()
    
    def get_stream(self):
        ''' Get a reference to the current stream (play() or rec()) '''
        return sd.get_stream()
    
    def query_devices(self):
        ''' Return information about available devices '''
        return sd.query_devices()
    
    def query_hostapis(self):
        ''' Return information about host APIs '''
        return sd.query_hostapis()
