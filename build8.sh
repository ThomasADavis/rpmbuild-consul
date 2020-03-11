#!/bin/bash

source /etc/os-release
tmp=$(mktemp -d)

git clone https://github.com/ThomasADavis/rpmbuild-consul.git ${tmp}
mkdir -p ${tmp}/{SOURCES,SRPMS}
spectool -g -C ${tmp}/SOURCES ${tmp}/SPECS/*.spec

mock --clean \
	--root centos-stream-$(uname -i)

mock --buildsrpm \
         --cleanup-after \
         --resultdir ${tmp}/SRPMS \
         --root centos-stream-$(uname -i) \
         --sources ${tmp}/SOURCES \
         --spec ${tmp}/SPECS/*.spec

mock --rebuild \
         --root centos-stream-$(uname -i) \
         ${tmp}/SRPMS/*.src.rpm

#    rm -rf ${tmp}
