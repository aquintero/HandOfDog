#ifndef GO_CORE_BOARD
#define GO_CORE_BOARD

#include <stdbool.h>
#include <stdlib.h>

#define BLACK -1
#define EMPTY 0
#define WHITE 1

bool is_in_bounds(int size, int i, int j);
bool reach_color(int* board, int size, int size2, int color, int i, int j);
bool clear(int* board, int size, int size2, int i, int j);
void score(int* board, int size, int size2, int score[2]);
bool play_stone(int* board, int size, int size2, int color, int i, int j);
void legal_moves(int* board, int size, int size2, int* board_history, int n_boards, int size3, int size4, int color, int* legal_moves, int size5, int size6);

#endif
