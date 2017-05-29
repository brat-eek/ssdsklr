import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
from PIL import Image
import numpy as np

def get_data_from_tag(node, tag, indx):
    return node.getElementsByTagName(tag)[indx].childNodes[0].data

dicnary={}
for rootdirs, rootsubdirs, rootfilenames in os.walk(
        '/data/caffe/examples/brandsdevkit/brands2017/Annotations'):
   # for rootsubdir in rootsubdirs:
   #     for level2dirs, level2subdirs, level2filenames in os.walk(os.path.join(rootdirs, rootsubdir)):
            
            for filename in rootfilenames:
                if filename != '.DS_Store' and '.xml' in filename:
                    with open(os.path.join(rootdirs, filename)) as f:
                        #print os.path.join(rootdirs, filename)
                        #a=input()
                        data = minidom.parseString(f.read())

                    objs = data.getElementsByTagName('object')

                    #sizes = data.getElementsByTagName('size')
                    #width = 0
                    #height = 0

                    #for size in sizes:
                    #    width = float(get_data_from_tag(size, 'width'))
                    #    height = float(get_data_from_tag(size, 'height'))
                    #    print width
                    #    print height

                    imagefile = filename.split('.xml')[0]
                    if not os.path.exists('/data/caffe/examples/brandsdevkit/brands2017/JPEGImages/' + imagefile + '.jpg'):
                        continue
                    #print 'image found'
                    im = Image.open('/data/caffe/examples/brandsdevkit/brands2017/JPEGImages/' + imagefile + '.jpg')
                    img_width, img_height = im.size
                    #print img_width, img_height
                    if im.mode=='RGB':
                        img_depth = 3
                    else : 
                        img_depth = 1
                    #print img_depth
                    #a=input() 
                    #scale_x = img_width / width
                    #scale_y = img_height / height
                    #print scale_x
                    #print scale_y
                    num_objs = len(objs)
                    #print num_objs
                    
                    # Load object bounding boxes into a data frame.
                    for ix, obj in enumerate(objs):
                        # Make pixel indexes 0-based
                        #print ix, obj
                        #a=input()
                        #xmind = float(get_data_from_tag(obj, 'x', 0)) - 1
                        #xmaxd = float(get_data_from_tag(obj, 'x', 1)) - 1
                        #ymind = float(get_data_from_tag(obj, 'y', 0)) - 1
                        #ymaxd = float(get_data_from_tag(obj, 'y', 1)) - 1
                        try:
                            cls = get_data_from_tag(obj, "name", 0).lower().strip()
                            dicnary[cls]=0
                            print cls, dicnary[cls]
                        except:
                            print 'oooooooooooooooooooooooooooooooooooooooooooooooooooo'
                        #annotation = Element("annotation")
                        #filenamexml = SubElement(annotation, "filename")
                        #size = SubElement(annotation, "size")
                        #width = SubElement(size, "width")
                        #height = SubElement(size, "height")
                        #depth = SubElement(size, "depth")
                        #width.text = str(img_width)
                        #height.text = str(img_height)
                        #depth.text = str(img_depth)
                        #object = SubElement(annotation, "object")
                        #name = SubElement(object, "name")
                        #bndbox = SubElement(object, "bndbox")
                        #xmin = SubElement(bndbox, "xmin")
                        #xmax = SubElement(bndbox, "xmax")
                        #ymin = SubElement(bndbox, "ymin")
                        #ymax = SubElement(bndbox, "ymax")
                        #filenamexml.text = filename
                        #name.text = cls
                        #xmin.text = str(xmind)
                        #xmax.text = str(xmaxd)
                        #ymin.text = str(ymind)
                        #ymax.text = str(ymaxd)
                        #ElementTree(annotation).write(
                        #    "/data/caffe/examples/brandsdevkit/brands2017/Annotations_new" + filename)
                        print filename
np.save('brand_names.npy',dicnary)
