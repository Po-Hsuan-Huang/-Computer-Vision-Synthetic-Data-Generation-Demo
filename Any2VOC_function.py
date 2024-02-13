# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 10:13:27 2016

@author: gene
"""
import numpy as np
import xml.etree.cElementTree as ET
from PIL import Image
import os, glob


#filename = "000001"
#width = 500
#height = 353 
#depth = 3
#classlabel = "Gunkanmaki"
#xmin = 0
#ymin = 0
#xmax = width
#ymax = height



def CreateTrainData(imgroot, max_wsize, max_hsize, degrees_set, xmin, ymin, xmax, ymax):
    
    # Check the output folders is ready or not
    VOCroot  = "marathon2017/"
    Res_path = "marathon2017/results/"
    Ann_path = VOCroot+"Annotations/"
    Set_path = VOCroot+"ImageSets/"
    Jpg_path = VOCroot+"JPEGImages/"
    Tag_path = VOCroot+'VOC_XML_Labeling/data/'


    if not os.path.exists(VOCroot):
        os.makedirs(VOCroot)
    if not os.path.exists(Res_path):
        os.makedirs(Res_path)
    if not os.path.exists(Ann_path):
        os.makedirs(Ann_path)
    if not os.path.exists(Set_path):
        os.makedirs(Set_path)    
    if not os.path.exists(Jpg_path):
        os.makedirs(Jpg_path)
    if not os.path.exists(Tag_path):
        os.makedirs(Tag_path)
    
    # Search each folder 
    classN  = 0 
    counter = 0
    
    # Clear Labeling Tags
    with open(Tag_path+"predefined_classes.txt","a") as file:
        file.write("")
        
    for folder_name in os.listdir(imgroot):
        classN += 1
        print '{} {}'.format(classN, folder_name)
        # Create Labeling Tags
        with open(Tag_path+"predefined_classes.txt","a") as file:
            file.write(folder_name+"\n")
        
        # Each image
        for image_path in glob.glob(imgroot+folder_name+"/*.JPG"):
            image_obj = ImageResizeNCrop(image_path, max_wsize, max_hsize)
            
            # Image Rotation
            for degrees in degrees_set:
                counter += 1
                
                # Create xml of the image
                filename = '{:06d}'.format(counter)
                tree = VOCxml(filename, image_obj, folder_name, xmin, ymin, xmax, ymax)
                tree.write(Ann_path + filename + ".xml") 
                
                # Save the image list of training
                with open(Set_path+"trainval.txt","a") as file:
                    file.write(filename+"\n")
                
                with open(Set_path+"test.txt","a") as file:
                    file.write(filename+"\n")
                
                # Rotate image and save it
                image_obj.rotate(degrees).save( Jpg_path+filename+'.jpg'.format(counter), "jpeg" )

    return classN
    
# Create the xml info of the image
def VOCxml(filename, image_obj, classlabel, img_pos, text_pos, text_space, font_type ):
    '''
        filename : str
            name of the file
        
        image_obj: PIL image
            background+tag image
        
        classlabel : tuple of str
            name of the label 
            In the case of marathon tag. there are two labels. One is the tag
            another is the numbers of ID on the tag.
            
            classlabel[1] : label name of the tag
            classlabel[2] : lable name of the text
        
        img_pos : tuple of float
            position of the upperleft cornet and the lower_right corner
            (x1,y1,x2,y2) of the tag image
        
        text_pos : tuple of float
            position of the text on the tag. Position of the upperleft cornet and the lower_right corner
            (x1,y1,x2,y2) of the tag image
        
        text_space : tuple of flaot || float
            space of each bounding box for each character in the text,
            or None if there is only one character.
        
        
        font_type : str
            font type of the text
            
        
    '''
    
    width, height = image_obj.size
    depth = 3
    #xmin = width/4
    #ymin = height/4
    #xmax = (width/4)*3
    #ymax = (width/4)*3
    
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "Wan-Jin-Shi_Marathon"
    ET.SubElement(root, "filename").text = filename+".jpg"
    
    node1 = ET.SubElement(root, "source")
    ET.SubElement(node1, "database").text = "The WJS Database"
    ET.SubElement(node1, "annotation").text = "PASCAL VOC2007"
    ET.SubElement(node1, "image").text = "Acer"
    ET.SubElement(node1, "flickrid").text = "no"
    ET.SubElement(node1, "font_type").text = font_type
    
    node2 = ET.SubElement(root, "owner")
    ET.SubElement(node2, "flickrid").text = "Acer"
    ET.SubElement(node2, "name").text = "KR7800"

    # size of the the screen
    node3 = ET.SubElement(root, "size")
    ET.SubElement(node3, "width").text = str(height)
    ET.SubElement(node3, "height").text = str(width)
    ET.SubElement(node3, "depth").text = str(depth)
    
    ET.SubElement(root, "segmented").text = "0"
    
        
        
    node4 = ET.SubElement(root, "object")
    ET.SubElement(node4, "name").text = classlabel[0]
    ET.SubElement(node4, "pose").text = "unspecified"
    ET.SubElement(node4, "truncated").text = "0"
    ET.SubElement(node4, "difficult").text = "0"
    
    # Bounding box of the target image 
    xmin, ymin, xmax, ymax = img_pos
    xmin = int(round(xmin))
    ymin = int(round(ymin))
    xmax = int(round(xmax))
    ymax = int(round(ymax))
    ET.SubElement(node4, "annotation_id").text = "bndbox_img"
    node6 = ET.SubElement(node4, "bndbox")
    ET.SubElement(node6, "xmin").text = str(xmin)
    ET.SubElement(node6, "ymin").text = str(ymin)
    ET.SubElement(node6, "xmax").text = str(xmax)
    ET.SubElement(node6, "ymax").text = str(ymax)
    
    # Bounding box of the target texts
    if isinstance(text_space, int):
       
        for i in range(text_space):
            
            node5 = ET.SubElement(root, "object")
            xmin , ymin, xmax, ymax = text_pos.pop(0) 
            xmin = int(round(xmin))
            ymin = int(round(ymin))
            xmax = int(round(xmax))
            ymax = int(round(ymax))
           
            boundboxname = "bndbox_text%d" %i
            ET.SubElement(node5, "name").text = classlabel[i+1]
            ET.SubElement(node5, "pose").text = "unspecified"
            ET.SubElement(node5, "truncated").text = "0"
            ET.SubElement(node5, "difficult").text = "0"
            ET.SubElement(node5, "annotation_id").text = boundboxname
            node6 = ET.SubElement(node5, "bndbox")
            ET.SubElement(node6, "xmin").text = str(xmin)
            ET.SubElement(node6, "ymin").text = str(ymin)
            ET.SubElement(node6, "xmax").text = str(xmax)
            ET.SubElement(node6, "ymax").text = str(ymax)
            
    else :
        xmin, ymin, xmax, ymax = text_pos
        
        node5 = ET.SubElement(node4, "bndbox_text")
        
        ET.SubElement(node5, "name").text = classlabel[1]

        ET.SubElement(node5, "xmin").text = str(xmin)
        ET.SubElement(node5, "ymin").text = str(ymin)
        ET.SubElement(node5, "xmax").text = str(xmax)
        ET.SubElement(node5, "ymax").text = str(ymax)



    
    return ET.ElementTree(root)

# Resize the image and crop
def ImageResizeNCrop(image_path, max_wsize, max_hsize):

    image_obj = Image.open(image_path)
    img_width,img_height = image_obj.size
    #	 Calculate the resize rate by short edge
    resize_rate = max_hsize / min(img_width,img_height)    
    img_width   = int(img_width  * resize_rate)
    img_height  = int(img_height * resize_rate)
    
    # Crop the
    cropx = int((img_width -max_wsize)/2)
    cropy = int((img_height-max_hsize)/2)
    image_obj.thumbnail( (img_width, img_height), Image.ANTIALIAS)
    image_obj = image_obj.crop( ( cropx, cropy, int(max_wsize)+cropx, int(max_hsize)+cropy) )
    return image_obj