#!/bin/sh
set -e
echo "move parameters folder to ~/opt/slakos"
echo "$(pwd)"
mkdir -p  ~/opt/slakos
cp -r ./pbc-0-3 ~/opt/slakos
echo "copy sucess !"
