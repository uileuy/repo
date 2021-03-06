#!/usr/bin/env python3

from types import SimpleNamespace

from lilaclib import *

g = SimpleNamespace()

build_prefix = 'extra-x86_64'

def pre_build():
  g.oldfiles = clean_directory()
  g.files = download_official_pkgbuild('wireshark-gtk')

  packaging = False
  ignoring = False
  for line in edit_file('PKGBUILD'):
    if ignoring:
      if line.strip() == '}':
        ignoring = False
        packaging = False
      continue

    if line.startswith('pkgname='):
      line = 'pkgname=wireshark-gtk2'
    elif line.startswith('makedepends=('):
      line = line.replace("'qt5-base' 'qt5-multimedia' 'gtk3'", "'gtk2'")
    elif '--with-qt' in line:
      continue
    elif '--with-gtk3' in line:
      line = '      --with-gtk2 \\'
    elif line.startswith((
      'package_wireshark-cli(',
      'package_wireshark-qt(',
      'package_wireshark-common(',
    )):
      ignoring = True
      continue
    elif line.startswith('package_wireshark-gtk('):
      line = 'package() {'
      packaging = True
    elif packaging:
      if 'GTK frontend' in line:
        line = line.replace('GTK', 'GTK 2')
      elif line.strip().startswith('depends='):
        line = line.replace('gtk3', 'gtk2')
      elif line.strip().startswith(('replaces=', 'conflicts=')):
        continue
      elif line.strip().startswith('install '):
        front, dest = line.rsplit(None, 1)
        dest = dest.replace('-gtk', '-gtk2')
        line = front + ' ' + dest
      elif line.strip() == '}':
        line = '''\
  sed -i -e 's/GTK+/&2/' -e 's/-gtk/&2/' \\
         "${pkgdir}/usr/share/applications/wireshark-gtk2.desktop"
''' + line

    print(line)

def post_build():
  git_rm_files(g.oldfiles)
  git_add_files(g.files)
  git_commit()

if __name__ == '__main__':
  single_main()
