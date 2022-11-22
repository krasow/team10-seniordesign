# First clone the repository
cd ./librealsense

# Now the build
cd build
## Install CMake with Python bindings (that's what the -DBUILD flag is for)
## see link: https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python#building-from-source
cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true
## Recompile and install librealsense binaries
## This is gonna take a while! The -j4 flag means to use 4 cores in parallel
## but you can remove it and simply run `sudo make` instead, which will take longer
sudo make -j4 && sudo make install

## Export pyrealsense2 to your PYTHONPATH so `import pyrealsense2` works
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/pyrealsense2
