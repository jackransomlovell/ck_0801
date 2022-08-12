from exm.io.io import createFolderStruc
from exm.io.io import nd2ToVol
from exm.io.io import writeH5

from nd2reader import ND2Reader
from tqdm import tqdm

fix_path = '/mp/nas2/ruihan/20220801_zebrafish/20220801_Code0/Channel405 SD_Seq0004.nd2'
fovs = ND2Reader(fix_path).metadata['fields_of_view']

createFolderStruc(code = 0, out_dir = '/mp/nas2/jlove/alignment/zebrafish/20220801/')

for fov in tqdm(fovs):
    fix_vol = nd2ToVol(fix_path, fov)
    writeH5(f'/mp/nas2/jlove/alignment/zebrafish/20220801/code0/{fov}.h5', fix_vol)

