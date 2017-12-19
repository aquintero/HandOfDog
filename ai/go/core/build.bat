swig -o go_core.c -python -py3 -O go_core.i
gcc -c board.c  go_core.c -I C:\Users\alexq\Miniconda3\include -I C:\Users\alexq\Miniconda3\Lib\site-packages\numpy\core\include
gcc -shared board.o go_core.o C:\Users\alexq\Miniconda3\python36.dll c:\Windows\System32\msvcr120.dll -o _go_core.pyd
del *.o
del go_core.c