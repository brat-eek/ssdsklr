import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
from PIL import Image
import cv2
import numpy as np
import warnings
warnings.filterwarnings("error")

def get_data_from_tag(node, tag, indx):
    return node.getElementsByTagName(tag)[indx].childNodes[0].data

ll=[]
for rootdirs, rootsubdirs, rootfilenames in os.walk(
        '/data/caffe/examples/brandsdevkit/brands2017/Annotations1'):
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
                        #ll.append(filename)
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
                        try:
                            xmind = float(get_data_from_tag(obj, 'x', 0)) 
                            xmaxd = float(get_data_from_tag(obj, 'x', 1)) 
                            ymind = float(get_data_from_tag(obj, 'y', 0)) 
                            ymaxd = float(get_data_from_tag(obj, 'y', 2)) 
                            xmind = min(xmind,xmaxd)
                            xmaxd = max(xmind,xmaxd)
                            ymind = min(ymind,ymaxd)
                            ymaxd = max(ymaxd,ymind)
                            cls = get_data_from_tag(obj, "name", 0).lower().strip()
                        except:
                            print filename
                            print 'check this'
                        print xmind, xmaxd, ymind, ymaxd, cls

                        annotation = Element("annotation")
                        filenamexml = SubElement(annotation, "filename")
                        size = SubElement(annotation, "size")
                        width = SubElement(size, "width")
                        height = SubElement(size, "height")
                        depth = SubElement(size, "depth")
                        width.text = str(img_width)
                        height.text = str(img_height)
                        depth.text = str(img_depth)
                        object = SubElement(annotation, "object")
                        name = SubElement(object, "name")
                        bndbox = SubElement(object, "bndbox")
                        xmin = SubElement(bndbox, "xmin")
                        xmax = SubElement(bndbox, "xmax")
                        ymin = SubElement(bndbox, "ymin")
                        ymax = SubElement(bndbox, "ymax")
                        filenamexml.text = filename
                        name.text = cls
                        xmin.text = str(int(xmind))
                        xmax.text = str(int(xmaxd))
                        ymin.text = str(int(ymind))
                        ymax.text = str(int(ymaxd))
                        if ymaxd > ymind and xmaxd > xmind and ymind >0 and ymaxd < img_height and xmind >0 and xmaxd < img_width and img_depth==3:
                            try:
                                flags = cv2.CV_LOAD_IMAGE_COLOR
                                img = cv2.imread('/data/caffe/examples/brandsdevkit/brands2017/JPEGImages/' + imagefile + '.jpg', flags)
                                ElementTree(annotation).write("/data/caffe/examples/brandsdevkit/brands2017/Annotations_jpeg/" + filename)
                                print filename
                            except RuntimeWarning:
                                print 'bad file press 1 to cont.'
                                a=input()
                                ll.append(filename)

np.save('jpegerrimgs.npy', ll)

