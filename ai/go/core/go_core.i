%module go_core
%{
    #define SWIG_FILE_WITH_INIT
    #include "board.h"
%}
%include <windows.i>
%include "numpy.i"
%init %{
    import_array();
%}

%apply (int ARGOUT_ARRAY1[ANY]) {(int score[2])};
%apply (int* INPLACE_ARRAY2, int DIM1, int DIM2) {(int* board, int size, int size2)};
%apply (int* INPLACE_ARRAY3, int DIM1, int DIM2, int DIM3) {(int* board_history, int n_boards, int size3, int size4)};
%apply (int* INPLACE_ARRAY2, int DIM1, int DIM2) {(int* legal_moves, int size5, int size6)};
%include "board.h"
