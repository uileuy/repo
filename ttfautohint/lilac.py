#!/usr/bin/env python3

from lilaclib import *

build_prefix = 'extra-x86_64'
post_build = aur_post_build

def pre_build():
  aur_pre_build()
  run_cmd("sh_-c_echo validpgpkeys=\('58E0C111E39F5408C5D3EC76C1A60EACE707FDA5'\) >> PKGBUILD".split('_'))

if __name__ == '__main__':
  single_main()

# vim:set ts=2 sw=2 et:
