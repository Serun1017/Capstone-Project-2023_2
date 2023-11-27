import numpy as np

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
