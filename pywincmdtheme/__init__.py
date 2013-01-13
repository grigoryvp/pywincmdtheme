#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# pywincmdtheme implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os
import sys
import re
import copy
import _winreg
from win32com.shell import shell, shellcon
import pythoncom


def main() :

  sPath = os.path.join( os.path.expanduser( "~" ), ".Xresources" )
  mColors = {}
  for i in range( 16 ) :
    mColors[ i ] = 0
  try :
    with open( sPath ) as oFile :
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
  except IOError :
    print( "~/.Xresources not found, using Ubuntu terminal color theme." )
    mColors = {
      0 : 0x300a24,
      1 : 0xcc0000,
      2 : 0x4e9a06,
      3 : 0xc4a000,
      4 : 0x3465a4,
      5 : 0x75507b,
      6 : 0x06989a,
      7 : 0xd3d7cf,
      8 : 0x555753,
      9 : 0xef2929,
      10 : 0x8ae234,
      11 : 0xfce94f,
      12 : 0x729fcf,
      13 : 0xad7fa8,
      14 : 0x34e2e2,
      15 : 0xeeeeec,
    }

  ##  Windows don't have separate backgound and foreground colors.
  if 'background' in mColors :
    mColors[ 0 ] = mColors[ 'background' ]
    del mColors[ 'background' ]
  if 'foreground' in mColors :
    mColors[ 7 ] = mColors[ 'foreground' ]
    del mColors[ 'foreground' ]

  ##  Colors is .Xresources are defined as "RGB" text, and while converting
  ##  in number that became 0xRGB, and we need red to be less significant,
  ##  so convert to 0xBGR
  for nKey, nVal in mColors.items() :
    nVal = ((nVal >> 16) & 0xFF) + (nVal & 0xFF00) + ((nVal << 16) & 0xFF0000)
    mColors[ nKey ] = int( nVal )

  ##  Window color table is different from ANSI:
  mColorsOld = copy.copy( mColors )
  mColors[ 1 ] = mColorsOld[ 4 ]
  mColors[ 3 ] = mColorsOld[ 6 ]
  mColors[ 4 ] = mColorsOld[ 1 ]
  mColors[ 6 ] = mColorsOld[ 3 ]
  mColors[ 9 ] = mColorsOld[ 12 ]
  mColors[ 11 ] = mColorsOld[ 14 ]
  mColors[ 12 ] = mColorsOld[ 9 ]
  mColors[ 14 ] = mColorsOld[ 11 ]

  if len( sys.argv ) > 1 and '--update-link' in sys.argv[ 1 ] :
    if len( sys.argv ) < 3 :
      print( "Error: Path to .lnk file not specified." )
      exit( 1 )
    oLink = pythoncom.CoCreateInstance( shell.CLSID_ShellLink, None,
      pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink )
    oPersist= oLink.QueryInterface( pythoncom.IID_IPersistFile )
    sFile = sys.argv[ 2 ]
    oPersist.Load( sFile )
    oLinkData = oLink.QueryInterface( shell.IID_IShellLinkDataList )
    oBlock = oLinkData.CopyDataBlock( shellcon.NT_CONSOLE_PROPS_SIG )
    lColors = []
    for i in range( 16 ) :
      lColors.append( mColors[ i ] )
    oBlock[ 'ColorTable' ] = lColors
    ##  Background color( 0 ) and foreground color( 7, white  ). Windows
    ##  tends to set this into white-on-blue for powershell that is pinned
    ##  into taskbar.
    oBlock[ 'FillAttribute' ] = 7
    oLinkData.RemoveDataBlock( shellcon.NT_CONSOLE_PROPS_SIG )
    oLinkData.AddDataBlock( oBlock )
    oPersist.Save( sFile, True )
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

