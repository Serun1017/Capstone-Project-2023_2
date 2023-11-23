import numpy as np
import cv2

from options import Option
from ModelLoad import ModelLoader
from SketchPreload import SketchLoader
from ImagePreload import ImageLoader
# sk is tokenized sketch data.
# im_dictionary is tokenized image data as dictionary
def retrieveImage(model, sk, im_dictionary) :
    labels = []
    
    for i, keys in enumerate(im_dictionary.keys()) :
        im = im_dictionary[keys]
        labels = np.concatenate((labels, keys), axis=0)

        sk_temp = sk.unsqueeze(1).repeat(1, len(keys), 1, 1).flatten(0, 1).cuda()
        im_temp = im.unsqueeze(0).repeat(1, 1, 1, 1).flatten(0, 1).cuda()

        # Relation Network
        feature_1, feature_2 = model(sk_temp, im_temp, 'test')
        if i == 0 :
            dist_im = feature_2.view(1, len(keys)).cpu().data.numpy()  # 1*args.batch
        else :
            dist_im = np.concatenate((dist_im, feature_2.view(1, len(keys)).cpu().data.numpy()), axis=1) # type:ignore
    dist_im = np.squeeze(dist_im) # type:ignore

    sorted_indices = np.argsort(dist_im)
    sorted_indices = sorted_indices[::-1]

    dist_im = dist_im[sorted_indices]
    labels = labels[sorted_indices]

    result = np.stack([dist_im, labels])
    return result

if __name__ == "__main__" :
    args = Option().parse()
    model = ModelLoader(args)

    ### Test Image Loaded to img
    path = 'C:\\Users\\tjgh2\\OneDrive\\바탕 화면\\capstone\\Capstone Project\\datasets\\raster_sketches\\1\\000000006336.jpg'
    image_path = np.fromfile(path, np.uint8)
    img = cv2.imdecode(image_path, cv2.IMREAD_COLOR)

    # Sketch Loader Load
    sketch = SketchLoader(model, args)
    sketch.LoadSketch(img)

    # Image Data Load
    im_path = 'C:\\Users\\tjgh2\\OneDrive\\바탕 화면\\capstone\\Capstone Project\\datasets\\images\\1' 
    image_data = ImageLoader(model, im_path, args)

    image_data.LoadImageToken()

    # If you load the image, you must call SelfAttention() to tokenize the image
    image_data.LoadImage()
    image_data.SelfAttention()

    # If you want to save the tokenized image, call SaveImageToken()
    image_data.SaveImageToken()

    # sk_data has tokenized sketch data, If you call LoadSketch()   
    sk = sketch.sk_data
    # im_dictionary has tokenized image data as dictionary, If you call LoadImageToken() or LoadImages() and SelfAttention()
    im_dictionary = image_data.im_dictionary

    # retrievaImage return the distance of sketch and image, labels of images
    result = retrieveImage(model, sk, im_dictionary)

    print(result[1])

