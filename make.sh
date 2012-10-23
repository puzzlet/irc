#!/bin/bash -x
PKG_NAME=python-irc
VER=`git describe --tag`
DEB_VER=0build`date --utc +%Y%m%d%H%M`utc

echo $VER > VERSION

rm -rf deb_dist/*

python setup.py --command-packages=stdeb.command sdist_dsc \
                --package $PKG_NAME \
                --debian-version $DEB_VER

cp debian/* deb_dist/irc-$VER/debian

cd deb_dist/irc-$VER
debuild -uc -us
cd -

echo "Debian package created: deb_dist/$PKG_NAME_$VER-${DEB_VER}_all.deb"
