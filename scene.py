import cv2
import numpy as np
#from matplotlib import pyplot as plt # WHY? I DON'T NEED THIS ON SERVER USE. WHY DID I ADD THIS?
from PIL import Image
import bottle
import json



#TODO using bottle.define_path_vars() to define path
db_dir = 'db'
scene_dir = 'scene'
img_path = f'{db_dir}/{scene_dir}/img/'
json_path = f'{db_dir}/{scene_dir}/json/' #Deprecated, probably scenes not going to use JSON to store metadata at all.

path_file = open(f'{db_dir}/{scene_dir}/scene_catalog.json','r')
SCENE_NAMES = json.load(path_file)
path_file.close()

FIRST_LAST_ONE=[0,-1]

def adjust_white(im,threshold=239) -> Image.Image:
    """
    Adjusting the colors of the image that its grayscale version
    is passing the giveb threshold (default: fifteen sixteenth of the color
    resolution (which is 256, and since it's starting from 0, it's
    255), 239). Supports image input in `numpy.ndarray` and `PIL.Image.Image`,
    but prefers `PIL.Image.Image`. On this development, must be in RGB format.
    Will return new instance of `PIL.Image.Image`.

    Parameters
    ----------
    TODO

    Returns
    -------
    TODO
    """
    if isinstance(im,np.ndarray):
        im_arr = im.copy()
        im = Image.fromarray(im)
    else:
        im_arr = np.array(im,dtype='uint8')
    white_coords = np.where(np.array(im.convert('L'),dtype='uint8')>=threshold)
    im_arr[white_coords]=[255,255,255]
    return Image.fromarray(im_arr)

def foreground_mask(im,rect) -> np.ndarray:
    #https://www.geeksforgeeks.org/python-foreground-extraction-in-an-image-using-grabcut-algorithm/
    #https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    if isinstance(im,Image.Image):
        im_arr = np.array(im)
        im_cv2 = im_arr[:,:,::-1]
    else:
        im_arr = im
        im_cv2 = im[:,:,::-1]
    mask = np.zeros(im_cv2.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64) 
    foregroundModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(im_cv2, mask, rect, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    return mask2

def mask_fill_in(mask,rect) -> np.ndarray:
    """
    #TODO explain

    Parameters
    ----------
    #TODO

    #TODO Returns
    """
    mask_coords = np.where(mask)
    unique_row = np.unique(mask_coords[0])
    unique_col = np.unique(mask_coords[1])
    out = np.zeros(mask.shape,dtype=bool)

    for row in unique_row:
        border_l, border_r = mask_coords[1][np.where(mask_coords[0]==row)][FIRST_LAST_ONE]
        out[row,:border_l] = True
        out[row,border_r:] = True

    for col in unique_col:
        border_u, border_d = mask_coords[0][np.where(mask_coords[1]==col)][FIRST_LAST_ONE]
        out[:border_u,col] = True
        out[border_d:,col] = True

    rect_mask = np.ones(mask.shape,dtype=bool)
    x0,y0,x,y = rect
    rect_mask[y0:y0+y,x0:x0+x] = False

    return np.logical_or(out, rect_mask)

def add_alpha(im,mask) -> np.ndarray :
    if isinstance(im,np.ndarray):
        y,x,c = im.shape
        im_arr = np.zeros((y,x,c+1))
        im_arr[:,:,:3]+=im
    else:
        im_arr = np.array(im.convert('RGBA'))
    im_arr[:,:,-1]=mask*255
    return im_arr
    
def apply_scene(im_rgba,scene_name):
    if isinstance(im_rgba,np.ndarray):
        mask=Image.fromarray(im_rgba[:,:,-1])
        im_rgba=Image.fromarray(im_rgba)
    else:
        mask=Image.fromarray(np.array(im_rgba)[:,:,-1])
    out = Image.open(f'{img_path}{scene_name}.jpg')
    out.paste(im_rgba,mask=mask)
    return out
    
def apply_scene_unmasked(im_rgb,rect,scene_name):
    im_adjust = adjust_white(im_rgb)
    mask = np.logical_not(mask_fill_in(foreground_mask(im_adjust,rect),rect))
    im_rgba = add_alpha(im_rgb,mask)
    return apply_scene(im_rgba,scene_name)

def super_random_scene(bottle_and_picks=None):
    if bottle_and_picks:
        b, picks = bottle_and_picks
    else:
        ((b,_,_),picks) = bottle.super_random_bottle()

    ingredients = bottle.get_ingredients_as_str(picks)
    name = bottle.get_fusion_name(picks
    )
    b_sq,x,y,x0,y0 = bottle.fit_square(b,dump_data=True)
    rect = (x0,y0,x,y)

    scene_name = np.random.choice(SCENE_NAMES)

    out = apply_scene_unmasked(b_sq, rect, scene_name)
    return out, name, ingredients, scene_name
    