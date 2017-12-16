swig -o go_core.c -python -py3 -O go_core.i
gcc -c go_board.c go_game.c go_core.c -IC:\Users\alexq\Miniconda3\include
gcc -shared go_game.o go_board.o go_core.o C:\Users\alexq\Miniconda3\python36.dll c:\Windows\System32\msvcr120.dll -o _go_core.pyd
del *.o
del go_core.c