from exm.io.io import createFolderStruc
from exm.io.io import nd2ToVol
from exm.io.io import writeH5
from exm.config.utils import load_cfg
from exm.align.build import alignBuild

import os
from nd2reader import ND2Reader
import tqdm

# get data parent directory and list all subfolders w/ codes
pdir = '/mp/nas2/ruihan/20220801_zebrafish/'
dirs = os.listdir(pdir)

# set ref vol path and moving vol template
fix_path = '/mp/nas2/ruihan/20220801_zebrafish/20220801_Code0/Channel405 SD_Seq0004.nd2'
mov_path_temp = os.path.join(pdir,'{}/Channel405 SD_Seq0004.nd2')

# get fovs
fovs = ND2Reader(fix_path).metadata['fields_of_view']

#build align obj w/ default params
cfg = load_cfg()
align = alignBuild(cfg)
align.buildSitkTile()

# iterate through each code dir
for dir_ in tqdm.tqdm(dirs[1:], desc='dir loop', position = 0):
    
    # deal with edge cases where dir is incomplete or not full of .nd2
    if 'incomplete' not in dir_ and 'ipynb' not in dir_:
        
        # get code from subfolder string
        code = dir_[-1]
        #create output dir
        createFolderStruc(code = code, out_dir = '/mp/nas2/jlove/alignment/zebrafish/20220801/')
        #format mov path with code dir
        mov_path = mov_path_temp.format(dir_)
        # iter each fov
        for fov in tqdm.tqdm(fovs, desc='fov loop', position = 1, leave = False):
            #get proper vols
            fix_vol = nd2ToVol(fix_path, fov)
            mov_vol = nd2ToVol(mov_path, fov)
            # lazy exception due to SITK failing sometimes
            try:
                #default tform and result
                tform = align.computeTransformMap(fix_vol, mov_vol)
                result = align.warpVolume(mov_vol, tform)
                #save
                align.writeTransformMap(f'/mp/nas2/jlove/alignment/zebrafish/20220801/code{code}/tforms/{fov}.txt', tform)
                writeH5(f'/mp/nas2/jlove/alignment/zebrafish/20220801/code{code}/{fov}.h5', result)
            except:
                # write code, fov to .txt file if it doesn't work
                with open('/mp/nas2/jlove/alignment/notebooks/zebrafish/20220801/failed.txt','a') as f:
                    f.write(f'{code},{fov}\n')

            




