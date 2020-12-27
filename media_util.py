import PIL.Image
import scipy 
import numpy as np
import os
import json

def is_a_video(filename):
    return filename.endswith(".mp4")

def is_an_image(filename):
    return filename.endswith(("jpg", "jpeg", "png"))

def get_post_data(path):
    filename = ""
    metadata = {}
    for temp_filename  in os.listdir(path):
        temp_filename = path + temp_filename 
        if os.path.isfile(temp_filename):
            if is_metadata_file(temp_filename):
                metadata = get_metadata(temp_filename)
            else:
                filename = temp_filename
    return filename, metadata

def is_metadata_file(filename):
    return filename.endswith(".json")

def get_metadata(temp_filename):
    with open(temp_filename) as metadata_json:
        metadata = json.load(metadata_json)
    return metadata

class PhotoCropper:
    #thanks to https://github.com/basnijholt/instacron

    def prepare_and_fix_photo(self, photo):
        with open(photo, "rb") as f:
            img = PIL.Image.open(f)
            img = self.strip_exif(img)
            if not self.correct_ratio(photo):
                img = self.crop_maximize_entropy(img)
            img.save(photo)
        return photo

    def crop(self, x, y, data, w, h):
        x = int(x)
        y = int(y)
        return data[y : y + h, x : x + w]

    def crop_maximize_entropy(self, img, min_ratio=4 / 5, max_ratio=90 / 47):
        from scipy.optimize import minimize_scalar

        w, h = img.size
        data = np.array(img)
        ratio = w / h
        if ratio > max_ratio:  # Too wide
            w_max = int(max_ratio * h)

            def _crop(x):
                return self.crop(x, y=0, data=data, w=w_max, h=h)

            xy_max = w - w_max
        else:  # Too narrow
            h_max = int(w / min_ratio)

            def _crop(y):
                return self.crop(x=0, y=y, data=data, w=w, h=h_max)

            xy_max = h - h_max
        
        def _entropy(data):
            """Calculate the entropy of an image"""
            hist = np.array(PIL.Image.fromarray(data).histogram())
            hist = hist / hist.sum()
            hist = hist[hist != 0]
            return -np.sum(hist * np.log2(hist))

        to_minimize = lambda xy: -_entropy(_crop(xy))  # noqa: E731
        x = minimize_scalar(to_minimize, bounds=(0, xy_max), method="bounded").x
        return PIL.Image.fromarray(_crop(x))

    def strip_exif(self,img):
        """Strip EXIF data from the photo to avoid a 500 error."""
        data = list(img.getdata())
        image_without_exif = PIL.Image.new(img.mode, img.size)
        image_without_exif.putdata(data)
        return image_without_exif
    
    def correct_ratio(self,photo):
        from instabot.api.api_photo import compatible_aspect_ratio, get_image_size

        return compatible_aspect_ratio(get_image_size(photo))

    