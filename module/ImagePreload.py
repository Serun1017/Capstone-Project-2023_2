import torch
import os
import numpy as np

from .data_utils.dataset import ValidSet, ValidSeparately
from torch.utils.data import DataLoader

class ImageLoader() :
    def __init__(self, model, im_path, args) :
        self.model = model
        self.im_path = im_path
        self.args = args
        self.im_dataload = None

        self.im_dictionary = dict() # im_labels: Tensors, im_labels are set of im_label sized by args.test_im. {('case1', 'case2') : Tensor([case1Tensor], [case2Tensor])}
        self.im_tokenized_label = set() # set of image labels that tokenized.
    

    ### LoadImage 수정할 것.
    # Load Image data and Call DataLoader to put in Model
    def LoadImage(self, image: ValidSet) :
        if image.file_names.__len__() == 0 :
            return
        
        # If image was already Tokenized, exclude the image
        if self.im_tokenized_label.intersection(image.file_names) :
            intersect_image = self.im_tokenized_label.intersection(image.file_names)
            for im in intersect_image :
                index = np.where(image.file_names == im)
                image.file_names = np.delete(image.file_names, index)
        
        # Image has been Loaded to im_dictionary
        self.im_dataload = DataLoader(image, batch_size=self.args.test_im, num_workers=self.args.num_workers, drop_last=False)
        
        return image.__len__()

    # Call this Method if the image has already tokenized and if you want to tokenize the image
    def LoadImageForcibly(self, im_path) :
        # If im_path is list of image list
        if isinstance(im_path, list) :
            already_tokenized_image = self.im_tokenized_label.intersection(im_path)
            new_image = [x for x in im_path if x not in already_tokenized_image]
            
            already_tokenized_image = ValidSeparately(already_tokenized_image, type_skim='im')
            new_image = ValidSeparately(new_image, type_skim='im')

            if new_image.__len__() > 0 :
                self.im_dataload = DataLoader(new_image, batch_size=self.args.test_im, num_workers=self.args.num_workers, drop_last=False)
                self.SelfAttention()

            if already_tokenized_image.__len__() > 0 :
                im_dataload = DataLoader(already_tokenized_image, batch_size=self.args.test_im, num_workers=self.args.num_workers, drop_last=False)

                new_im_dictionary = dict()
                for im, im_label in im_dataload :
                    im = im.cuda()
                    im, __ = self.model(im, None, 'test', only_sa=True)
                    
                    new_im_dictionary[im_label] = im
            
                self.__UpdateImageDictionaryForcibly__(new_im_dictionary)
                print(f"{im_label} has forcibly updated") # type:ignore

    def ISImageTokenized(self, im_path) :
        if isinstance(im_path, list) :
            return self.im_tokenized_label.intersection(im_path) != None
        return im_path in self.im_tokenized_label

    # Tokenize all Image Data. Save tokens and image index in im_retreival as (im, im_idxs)
    def SelfAttention(self) :
        # If Image has not beeing ready to load, return None
        if not self.im_dataload :
            return None
        # Tokenize the Image Data
        new_im_dictionary = dict()
        # for im, im_label in self.im_dataload :
            # im = im.cuda()
            # im, im_idxs = self.model(im, None, 'test', only_sa=True)

            # new_im_dictionary[im_label] = im
        # self.__UpdateImageDictionary__(new_im_dictionary)
        print("Image has been tokenized")

    # Save Image Self Attention Data
    def SaveImageToken(self, filename='im_dictionary.pt') :
        torch.save(self.im_dictionary, filename)

    # Load Image Self Attention Data
    def LoadImageToken(self, filename='im_dictionary.pt') :
        # If File not exist, return False
        if not os.path.exists(filename) :
            return False
        new_im_dictionary = torch.load(filename)
        self.__UpdateImageDictionary__(new_im_dictionary)
        print('ImageToken loaded')
        return True

    # Update Image Dictionary. It exclude exists new images when the images are already tokenized and saved in im_dictionary
    def __UpdateImageDictionary__(self, new_im_dictionary) :
        for keys in new_im_dictionary.keys() :
            # If There are no intersection between tokenized image label and new image label, update the tokenized image label
            if not self.im_tokenized_label.intersection(keys) :
                # if 'keys' is not Empty, add to image dictionary
                if keys :
                    self.im_tokenized_label.update(keys)
                    self.im_dictionary[keys] = new_im_dictionary[keys]
            else :
                intersection = self.im_tokenized_label.intersection(keys)
                _keys = []
                _keys.extend(keys)
                # Remove intersect im_label
                for im_label in intersection :
                    remove_index = _keys.index(im_label)
                    # Remove Tensor
                    new_im_dictionary[tuple(_keys)] = torch.cat((new_im_dictionary[tuple(_keys)][:remove_index], new_im_dictionary[tuple(_keys)][remove_index+1:]), dim=0)

                    im_datas = new_im_dictionary.pop(tuple(_keys))
                    # Update keys
                    _keys.pop(remove_index)
                    # Update im_dictionary
                    new_im_dictionary[tuple(_keys)] = im_datas
                
                # If '_keys' is not Empty, add to image dictionary
                if _keys :
                    self.im_tokenized_label.update(_keys)
                    self.im_dictionary[tuple(_keys)] = new_im_dictionary[tuple(_keys)]

    def __UpdateImageDictionaryForcibly__(self, new_im_dictionary) :
        for keys in new_im_dictionary.keys() :
            # If There are no intersection between tokenized image label and new image label, update the tokenized image label
            if not self.im_tokenized_label.intersection(keys) :
                # if 'keys' is not Empty, add to image dictionary
                if keys :
                    self.im_tokenized_label.update(keys)
                    self.im_dictionary[keys] = new_im_dictionary[keys]
            else :
                for tokenized_image_keys in self.im_dictionary.keys() :
                    tokenized_image_liat = set(tokenized_image_keys)
                    new_image_list = set(keys)
                    
                    intersection = tokenized_image_liat.intersection(new_image_list)
                    if intersection :
                        # Remove intersect im_label
                        for im_label in intersection :
                            tokenized_image_index = tokenized_image_keys.index(im_label)
                            new_image_index = keys.index(im_label)

                            self.im_dictionary[tokenized_image_keys][tokenized_image_index] = new_im_dictionary[keys][new_image_index]
