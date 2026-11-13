@echo off
setlocal
set VSDIR=C:\Program Files\Microsoft Visual Studio\2022\Community
call "%VSDIR%\VC\Auxiliary\Build\vcvars64.bat" >nul || exit /b 1
cd /d "%~dp0"
if not exist build mkdir build
set MH=third_party\minhook\src
cl /nologo /O2 /MT /W3 /c /Ithird_party\minhook\include /Fobuild\ %MH%\hook.c %MH%\buffer.c %MH%\trampoline.c %MH%\hde\hde64.c || exit /b 1
set OBJS=build\hook.obj build\buffer.obj build\trampoline.obj build\hde64.obj
cl /nologo /std:c++20 /O2 /MT /EHsc /W3 /DUNICODE /D_UNICODE /DWIN32_LEAN_AND_MEAN /DNOMINMAX /D_CRT_SECURE_NO_WARNINGS /Ithird_party\minhook\include /Ithird_party\dr_libs ^
   src\main.cpp src\proxy_multi.cpp src\decoders.cpp %OBJS% ^
   /Fobuild\ /Fdbuild\ /Zi /LD /Fe:build\winmm.dll ^
   /link /DEF:src\proxy.def /DEBUG /OPT:REF /OPT:ICF user32.lib ole32.lib shell32.lib bcrypt.lib || exit /b 1
echo built build\winmm.dll
rem release build: the same code without debug symbols (no PDB path in the DLL) and with NDEBUG (no assert file paths)
if not exist build\public mkdir build\public
cl /nologo /std:c++20 /O2 /MT /EHsc /W3 /DNDEBUG /DUNICODE /D_UNICODE /DWIN32_LEAN_AND_MEAN /DNOMINMAX /D_CRT_SECURE_NO_WARNINGS /Ithird_party\minhook\include /Ithird_party\dr_libs ^
   src\main.cpp src\proxy_multi.cpp src\decoders.cpp %OBJS% ^
   /Fobuild\public\ /LD /Fe:build\public\winmm.dll ^
   /link /DEF:src\proxy.def /OPT:REF /OPT:ICF user32.lib ole32.lib shell32.lib bcrypt.lib || exit /b 1
echo built build\public\winmm.dll
