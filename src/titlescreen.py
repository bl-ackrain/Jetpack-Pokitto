# titlescreen.py

import upygame


logoPixels = b'\
\x99\x99\x99\x98\x80\x00\x00\x99\x99\x88\x80\x00\x99\x99\x98\x88\x80\x09\x99\x98\x88\x80\x09\x99\x88\x88\x00\x99\x99\x88\x80\x09\x99\x88\x09\
\x01\x11\x11\x19\x88\x00\x00\x91\x11\x98\x88\x99\x11\x11\x19\x98\x88\x99\x11\x99\x88\x88\x91\x11\x98\x88\x89\x11\x19\x98\x88\x91\x18\x88\x99\
\x09\x18\x81\x11\x88\x80\x09\x11\x11\x19\x89\x11\x11\x11\x11\x19\x89\x91\x11\x19\x98\x89\x11\x11\x19\x88\x91\x11\x11\x99\x89\x11\x98\x89\x99\
\x00\x90\x09\x11\x98\x88\x91\x11\x99\x17\x89\x19\x99\x19\x99\x19\x89\x11\x99\x11\x98\x91\x11\x91\x11\x98\x91\x19\x91\x19\x89\x19\x88\x99\x19\
\x00\x00\x09\x91\x19\x89\x11\x98\x88\xc9\x79\x98\x89\x19\x88\x99\x89\x19\x88\x91\x98\x91\x19\x89\x11\x98\x91\x99\x89\x99\x89\x19\x89\x91\x19\
\x00\x00\x00\x91\x19\x89\x11\x98\x88\xf7\x4c\x74\x79\x19\x88\x88\x89\x19\x88\x91\x98\x91\x99\x89\x91\x98\x91\x98\x88\x80\x09\x19\x89\x11\x98\
\x00\x00\x00\x09\x19\x89\x11\x98\x94\x7f\x4f\x4c\x49\x19\x88\xc4\xc9\x19\x99\x91\x98\x91\x89\x49\x81\x98\x91\x98\x4c\x44\xc9\x19\x89\x19\x88\
\x00\x00\x00\x09\x19\x89\x11\x11\x19\x14\x17\x77\xc9\x19\x88\x47\x49\x11\x11\x19\x87\x91\x88\x98\x81\x98\x91\x98\x47\x44\x49\x19\x99\x18\x80\
\x00\x09\x88\x89\x19\x89\x11\x11\x1f\x1c\x44\xcc\x49\x19\x88\x44\x49\x11\x99\x98\x84\x91\x11\x11\x11\x98\x91\x98\x44\x44\x49\x11\x11\x18\x00\
\x00\x99\x88\x89\x19\x89\x11\x98\x99\x77\xc7\x47\x49\x19\x88\x74\x79\x19\x88\x8c\x47\x91\x94\xc4\x91\x98\x91\x98\xc4\x44\x79\x19\x98\x19\x80\
\x09\x11\x88\x89\x19\x89\x11\x98\x88\x8f\x98\x88\x09\x19\x88\x80\x09\x19\x88\x80\x00\x91\x98\x80\x91\x98\x91\x98\x88\x00\x09\x19\x89\x19\x88\
\x91\x19\x88\x89\x19\x89\x11\x98\x88\x79\x98\x88\x09\x19\x88\x80\x09\x19\x88\x80\x00\x91\x98\x80\x91\x98\x91\x98\x88\x00\x09\x19\x89\x11\x98\
\x91\x98\x88\x91\x19\x89\x11\x98\x8c\x91\x98\x88\x09\x19\x88\x80\x09\x19\x88\x80\x00\x91\x98\x80\x91\x98\x91\x98\x88\x89\x89\x19\x88\x91\x19\
\x91\x19\x99\x11\x98\x80\x91\x19\x99\x11\x98\x88\x09\x19\x88\x80\x09\x11\x98\x80\x00\x91\x98\x80\x91\x98\x91\x19\x99\x99\x89\x19\x88\x89\x19\
\x09\x11\x11\x19\x88\x00\x09\x11\x11\x19\x88\x00\x91\x11\x98\x80\x09\x11\x19\x88\x00\x91\x19\x89\x11\x98\x09\x11\x11\x19\x88\x91\x98\x80\x99\
\x00\x99\x99\x98\x80\x00\x00\x99\x99\x98\x80\x09\x99\x99\x99\x88\x89\x99\x99\x98\x80\x99\x99\x89\x99\x98\x00\x99\x99\x98\x88\x09\x99\x88\x09\
'
logo = upygame.surface.Surface(70, 16, logoPixels);