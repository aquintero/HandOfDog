#ifndef GO_BOARD
#define GO_BOARD

#include <stdlib.h>
#include <stdbool.h>

#define EMPTY 0
#define BLACK -1
#define WHITE 1

typedef struct GoBoard {
    int size;
    int* board;
} GoBoard;

extern const int directions[4][2];

int position_to_index(int size, int i, int j);
int init_board(GoBoard* go_board, int size);
int copy_board(GoBoard* from, GoBoard* to);
int destroy_board(GoBoard* go_board);
bool board_equals(GoBoard* b1, GoBoard* b2);
int reset_board(GoBoard* go_board);
int reach_color(GoBoard* go_board, int color, int i, int j, bool* ret);
bool is_in_bounds(GoBoard* go_board, int i, int j);
bool _reach_color_recursive(GoBoard* go_board, int color, int i, int j, bool* visited);
int clear(GoBoard* go_board, int i, int j);
int _clear_recursive(GoBoard* go_board, int i, int j);

#endif