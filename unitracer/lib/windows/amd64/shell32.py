#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009-2014, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Wrapper for shell32.dll in ctypes.
"""

# TODO
# * Add a class wrapper to SHELLEXECUTEINFO
# * More logic into ShellExecuteEx

__revision__ = "$Id: shell32.py 1299 2013-12-20 09:30:55Z qvasimodo $"

from defines import *
from kernel32 import LocalFree

#==============================================================================
# This is used later on to calculate the list of exported symbols.
_all = None
_all = set(vars().keys())
#==============================================================================

#--- Constants ----------------------------------------------------------------

SEE_MASK_DEFAULT            = 0x00000000
SEE_MASK_CLASSNAME          = 0x00000001
SEE_MASK_CLASSKEY           = 0x00000003
SEE_MASK_IDLIST             = 0x00000004
SEE_MASK_INVOKEIDLIST       = 0x0000000C
SEE_MASK_ICON               = 0x00000010
SEE_MASK_HOTKEY             = 0x00000020
SEE_MASK_NOCLOSEPROCESS     = 0x00000040
SEE_MASK_CONNECTNETDRV      = 0x00000080
SEE_MASK_NOASYNC            = 0x00000100
SEE_MASK_DOENVSUBST         = 0x00000200
SEE_MASK_FLAG_NO_UI         = 0x00000400
SEE_MASK_UNICODE            = 0x00004000
SEE_MASK_NO_CONSOLE         = 0x00008000
SEE_MASK_ASYNCOK            = 0x00100000
SEE_MASK_HMONITOR           = 0x00200000
SEE_MASK_NOZONECHECKS       = 0x00800000
SEE_MASK_WAITFORINPUTIDLE   = 0x02000000
SEE_MASK_FLAG_LOG_USAGE     = 0x04000000

SE_ERR_FNF              = 2
SE_ERR_PNF              = 3
SE_ERR_ACCESSDENIED     = 5
SE_ERR_OOM              = 8
SE_ERR_DLLNOTFOUND      = 32
SE_ERR_SHARE            = 26
SE_ERR_ASSOCINCOMPLETE  = 27
SE_ERR_DDETIMEOUT       = 28
SE_ERR_DDEFAIL          = 29
SE_ERR_DDEBUSY          = 30
SE_ERR_NOASSOC          = 31

SHGFP_TYPE_CURRENT = 0
SHGFP_TYPE_DEFAULT = 1

CSIDL_DESKTOP                   = 0x0000
CSIDL_INTERNET                  = 0x0001
CSIDL_PROGRAMS                  = 0x0002
CSIDL_CONTROLS                  = 0x0003
CSIDL_PRINTERS                  = 0x0004
CSIDL_PERSONAL                  = 0x0005
CSIDL_FAVORITES                 = 0x0006
CSIDL_STARTUP                   = 0x0007
CSIDL_RECENT                    = 0x0008
CSIDL_SENDTO                    = 0x0009
CSIDL_BITBUCKET                 = 0x000a
CSIDL_STARTMENU                 = 0x000b
CSIDL_MYDOCUMENTS               = CSIDL_PERSONAL
CSIDL_MYMUSIC                   = 0x000d
CSIDL_MYVIDEO                   = 0x000e
CSIDL_DESKTOPDIRECTORY          = 0x0010
CSIDL_DRIVES                    = 0x0011
CSIDL_NETWORK                   = 0x0012
CSIDL_NETHOOD                   = 0x0013
CSIDL_FONTS                     = 0x0014
CSIDL_TEMPLATES                 = 0x0015
CSIDL_COMMON_STARTMENU          = 0x0016
CSIDL_COMMON_PROGRAMS           = 0x0017
CSIDL_COMMON_STARTUP            = 0x0018
CSIDL_COMMON_DESKTOPDIRECTORY   = 0x0019
CSIDL_APPDATA                   = 0x001a
CSIDL_PRINTHOOD                 = 0x001b
CSIDL_LOCAL_APPDATA             = 0x001c
CSIDL_ALTSTARTUP                = 0x001d
CSIDL_COMMON_ALTSTARTUP         = 0x001e
CSIDL_COMMON_FAVORITES          = 0x001f
CSIDL_INTERNET_CACHE            = 0x0020
CSIDL_COOKIES                   = 0x0021
CSIDL_HISTORY                   = 0x0022
CSIDL_COMMON_APPDATA            = 0x0023
CSIDL_WINDOWS                   = 0x0024
CSIDL_SYSTEM                    = 0x0025
CSIDL_PROGRAM_FILES             = 0x0026
CSIDL_MYPICTURES                = 0x0027
CSIDL_PROFILE                   = 0x0028
CSIDL_SYSTEMX86                 = 0x0029
CSIDL_PROGRAM_FILESX86          = 0x002a
CSIDL_PROGRAM_FILES_COMMON      = 0x002b
CSIDL_PROGRAM_FILES_COMMONX86   = 0x002c
CSIDL_COMMON_TEMPLATES          = 0x002d
CSIDL_COMMON_DOCUMENTS          = 0x002e
CSIDL_COMMON_ADMINTOOLS         = 0x002f
CSIDL_ADMINTOOLS                = 0x0030
CSIDL_CONNECTIONS               = 0x0031
CSIDL_COMMON_MUSIC              = 0x0035
CSIDL_COMMON_PICTURES           = 0x0036
CSIDL_COMMON_VIDEO              = 0x0037
CSIDL_RESOURCES                 = 0x0038
CSIDL_RESOURCES_LOCALIZED       = 0x0039
CSIDL_COMMON_OEM_LINKS          = 0x003a
CSIDL_CDBURN_AREA               = 0x003b
CSIDL_COMPUTERSNEARME           = 0x003d
CSIDL_PROFILES                  = 0x003e

CSIDL_FOLDER_MASK               = 0x00ff

CSIDL_FLAG_PER_USER_INIT        = 0x0800
CSIDL_FLAG_NO_ALIAS             = 0x1000
CSIDL_FLAG_DONT_VERIFY          = 0x4000
CSIDL_FLAG_CREATE               = 0x8000

CSIDL_FLAG_MASK                 = 0xff00

#--- Structures ---------------------------------------------------------------

# typedef struct _SHELLEXECUTEINFO {
#   DWORD     cbSize;
#   ULONG     fMask;
#   HWND      hwnd;
#   LPCTSTR   lpVerb;
#   LPCTSTR   lpFile;
#   LPCTSTR   lpParameters;
#   LPCTSTR   lpDirectory;
#   int       nShow;
#   HINSTANCE hInstApp;
#   LPVOID    lpIDList;
#   LPCTSTR   lpClass;
#   HKEY      hkeyClass;
#   DWORD     dwHotKey;
#   union {
#     HANDLE hIcon;
#     HANDLE hMonitor;
#   } DUMMYUNIONNAME;
#   HANDLE    hProcess;
# } SHELLEXECUTEINFO, *LPSHELLEXECUTEINFO;

class SHELLEXECUTEINFO(Structure):
    _fields_ = [
        ("cbSize",       DWORD),
        ("fMask",        ULONG),
        ("hwnd",         HWND),
        ("lpVerb",       LPSTR),
        ("lpFile",       LPSTR),
        ("lpParameters", LPSTR),
        ("lpDirectory",  LPSTR),
        ("nShow",        ctypes.c_int),
        ("hInstApp",     HINSTANCE),
        ("lpIDList",     LPVOID),
        ("lpClass",      LPSTR),
        ("hkeyClass",    HKEY),
        ("dwHotKey",     DWORD),
        ("hIcon",        HANDLE),
        ("hProcess",     HANDLE),
    ]

    def __get_hMonitor(self):
        return self.hIcon
    def __set_hMonitor(self, hMonitor):
        self.hIcon = hMonitor
    hMonitor = property(__get_hMonitor, __set_hMonitor)

LPSHELLEXECUTEINFO = POINTER(SHELLEXECUTEINFO)


#==============================================================================
# This calculates the list of exported symbols.
_all = set(vars().keys()).difference(_all)
__all__ = [_x for _x in _all if not _x.startswith('_')]
__all__.sort()
#==============================================================================
