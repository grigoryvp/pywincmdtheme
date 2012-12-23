#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import sys
import re
import _winreg

def main() :

  sPath = os.path.join( os.path.expanduser( "~" ), ".Xresources" )
  with open( sPath ) as oFile :
    mColors = {}
    for sLine in oFile :
      ## *background: #300a24
      sRe = r'.+background\s*:\s*#(?P<color>[\da-fA-F]+)'
      oMatch = re.match( sRe, sLine )
      if oMatch :
        mMatch = oMatch.groupdict()
        mColors[ 'background' ] = int( mMatch[ 'color' ], 16 )
      sRe = r'.+foreground\s*:\s*#(?P<color>[\da-fA-F]+)'
      oMatch = re.match( sRe, sLine )
      if oMatch :
        mMatch = oMatch.groupdict()
        mColors[ 'foreground' ] = int( mMatch[ 'color' ], 16 )
      sRe = r'.+color(?P<id>\d+)\s*:\s*#(?P<color>[\da-fA-F]+)'
      oMatch = re.match( sRe, sLine )
      if oMatch :
        mMatch = oMatch.groupdict()
        mColors[ int( mMatch[ 'id' ] ) ] = int( mMatch[ 'color' ], 16 )

  ##  Windows don't have separate backgound and foreground colors.
  if 'background' in mColors :
    mColors[ 0 ] = mColors[ 'background' ]
    del mColors[ 'background' ]
  if 'foreground' in mColors :
    mColors[ 7 ] = mColors[ 'foreground' ]
    del mColors[ 'foreground' ]

  if( '--update-link' in sys.argv ) :
    assert False, "Not implemented."
  else :
    nGroup = _winreg.HKEY_CURRENT_USER
    nRight = _winreg.KEY_ALL_ACCESS
    with _winreg.OpenKey( nGroup, 'Console', 0, nRight ) as oKey :
      for nKey, nVal in mColors.items() :
        sName = 'ColorTable{:02d}'.format( nKey )
        _winreg.SetValueEx( oKey, sName, 0, _winreg.REG_DWORD, nVal )
    print( """
      Done. Note that command-line applications pinned to taskbar will not
      be affected by global color theme. To apply color theme to pinned
      command-line application find corresponding .lnk file and execute
      this tool with '--update-link' key and full path to .lnk file.
    """.strip().replace( '\n', '' ).replace( '      ', ' ' ) )

