import os
import numpy as np
from torch.utils import data

from .utils import preprocess

class ValidSet(data.Dataset):
    def __init__(self, path, type_skim='im', half=False):
        self.type_skim = type_skim
        self.path = path
        self.half = half

        self.file_names = []
        self.cls = []

        for (path, dir, files) in os.walk(self.path) :
            for filename in files :
                ext = os.path.splitext(filename)[-1]
                if ext == '.jpg' :
                    self.file_names = np.append(self.file_names, path + '/' + filename)
                    self.cls = np.append(self.cls, path + '/' + filename)
                elif ext == '.png' :
                    self.file_names = np.append(self.file_names, path + '/' + filename)
                    self.cls = np.append(self.cls, path + '/' + filename)


    def __getitem__(self, index):
        label = self.cls[index]
        file_name = self.file_names[index]
        
        if self.half :
            image = preprocess(file_name, self.type_skim).half()
        else :
            image = preprocess(file_name, self.type_skim)

        return image, label
    
    def __len__(self):
        return len(self.file_names)
    
    def roll(self, shift) :
        self.file_names = np.roll(self.file_names, shift, axis=0)
        self.cls = np.roll(self.cls, shift, axis=0)
    
class ValidSeparately(data.Dataset) :
    def __init__(self, im_path_list, type_skim='im') :
        self.path_list = im_path_list
        self.type_skim = type_skim

        self.file_names = []
        self.cls = []

        for path in self.path_list :
            ext = os.path.splitext(path)[-1]
            if ext == '.jpg' or ext == '.png':
                self.file_names = np.append(self.file_names, path)
                self.cls = np.append(self.cls, path)
                
    def __getitem__(self, index):
        label = self.cls[index]
        file_name = self.file_names[index]

        image = preprocess(file_name, self.type_skim).half()

        return image, label

    def __len__(self):
        return len(self.file_names)

    def roll(self, shift) :
        self.file_names = np.roll(self.file_names, shift, axis=0)
        self.cls = np.roll(self.cls, shift, axis=0)