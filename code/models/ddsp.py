import time
import torch

class DDSP():
    m_path = "/home/martin/Desktop/ddsp_pytorch/models/ddsp_demo_pretrained.ts"
    f_pass = 3

    def __init__(self):
        # Testing DDSP
        print('Creating empty DDSP')
        self.model = None

    def preload(self):
        self.model = torch.jit.load(self.m_path)
        self.model = self.model.cuda()
        pitch = torch.randn(1, 2, 1).cuda()
        loudness = torch.randn(1, 2, 1).cuda()
        for p in range(self.f_pass):
            with torch.no_grad():
                audio = self.model(pitch, loudness)
                
    def generate_random(self, length=200):
        pitch = torch.randn(1, 200, 1).cuda()
        loudness = torch.randn(1, 200, 1).cuda()
        with torch.no_grad():
            audio = model(pitch, loudness)
        return audio

    def generate(self, pitch, loudness):
        pitch = pitch.cuda()
        loudness = loudness.cuda()
        with torch.no_grad():
            audio = model(pitch, loudness)
        return audio

        