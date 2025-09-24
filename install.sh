## if you do not have sudo, change the simgrid cmake to `cmake -DCMAKE_INSTALL_PREFIX=$HOME/local/ ..`, the wrench cmake to `cmake -DSimGrid_PATH=$HOME/local -DCMAKE_INSTALL_PREFIX=$HOME/`, the simulator cmake to `cmake -DWRENCH_PATH=$HOME/local -DCMAKE_INSTALL_PREFIX=$HOME/local  ..`, remove the 3 `sudo ldconfig`, remove the `sudo` from each `make install`, add `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib` to your bashrc and any scripts that run the simulator, then change the simcal install to use the local user install or an environment

echo Installing SimGrid
set -e
wget https://github.com/simgrid/simgrid/releases/download/v4.0/simgrid-4.0.tar.gz
tar -xf simgrid-4.0.tar.gz 
cd simgrid-4.0
mkdir -p build
cd build
cmake ..
make -j `nproc`
sudo make install
sudo ldconfig
cd ../../local/lib64

echo Installing Wrench
wget https://github.com/wrench-project/wrench/archive/refs/tags/v2.6.tar.gz
tar -xzf v2.6.tar.gz 
cd wrench-2.6
mkdir -p build
cd build
cmake ..
make -j `nproc`
sudo make install
sudo ldconfig
cd ../..

echo Installing Simulator
cd simulator
mkdir -p build
cd build
cmake ..
make -j `nproc`
sudo make install
sudo ldconfig
cd ../..

echo Installing simcal
git clone https://github.com/wrench-project/simcal.git
set -e
cd simcal
git pull
sudo pip install -r requirements.txt
sudo ./setup.py install

echo Installation complete
