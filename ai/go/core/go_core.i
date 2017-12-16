%module go_core
%include <windows.i>
%{
#include "go_board.h"
#include "go_game.h"
%}

%include go_board.h
%include go_game.h