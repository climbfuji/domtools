How to create videos from quilting component output (e.g. Gaussian):

# Extract variables needed
for file in atmf0??.nc; do echo $file; ncks -v lat,lon,hgtsfc,srh03,srh01 $file $file.srh.nc; done

# For creating one file (concatenating) - not needed below, but possibly useful (ncview etc.)
for file in atmf0??.nc.srh.nc; do echo $file; ncks --mk_rec_dmn time $file $file.tmprecdim.nc; done
ncrcat atmf0*.nc.srh.nc.tmprecdim.nc atmf000-096.srh.nc

# Resample to various lat/lon resolution for faster plotting
cdo -P 18 remapcon,r360x180 sfcf096.nc.orog.nc sfcf096.nc.orog.nc.360x180.nc

# Run python plotting scripts to create png; one is the timestep in C/Python notation
# DH* TODO - NO, it's a mix between C and Fortran notation, cleanup!
python srh.py 1

# If the output is non-contiguous and/or doesn't start at "1", copy/link files
# to something temporary starting with index 1 and increasing by 1 each step.
mkdir ffmpeg; cd ffmpeg
cp ../srh03_01.png ./srh03_01.png
cp ../srh03_04.png ./srh03_02.png
cp ../srh03_07.png ./srh03_03.png
...
ffmpeg -framerate 2 -i srh03_%02d.png -c:v libx264 -pix_fmt yuv420p out.mp4
