from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from rest_framework import serializers
from basic.models import Picker
from colorthief import ColorThief
from PIL import Image
import requests

NUM_CLUSTERS = 10


class PickerSerializer(serializers.HyperlinkedModelSerializer):
    #id=serializers.PrimaryKeyRelatedField(read_only=True)
    def create (self, validated_data):
        url=validated_data.get('url')
        #url already present then update
        im=Image.open(requests.get(url, stream=True).raw)
        #img.show()
        #Code to find the most dominant color in the image
        im = im.resize((150, 150))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

        print('finding clusters')
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        print('cluster centres:\n', codes)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)      # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        index_max = np.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii') # actual colour, (in HEX)
        print('most frequent is %s (#%s)' % (peak, colour))

        # code to find the color of the border
        width, height=im.size
        print(width, height)
        #converting to rgb colorspace
        img_rgb=im.convert("RGB")
        rgb_pixel_value=img_rgb.getpixel((height-1, width-1))
        def rgb_to_hex(rgb):
            return '%02x%02x%02x' % rgb
        hex_color="#" +rgb_to_hex(rgb_pixel_value)
        colour="#" + colour
        return Picker.objects.create(url=url, dominant_color=colour, logo_border=hex_color)



    class Meta:
        model= Picker
        fields='__all__'
        read_only_fields=('dominant_color', 'logo_border')
