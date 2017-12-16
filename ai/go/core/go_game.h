#ifndef GO_GAME
#define GO_GAME

#include "go_board.h"

typedef struct GoGame {
    GoBoard* boards;
    int* moves;
    bool** legal_moves;
    int board_size;
    int n_moves;
    int max_moves;
} GoGame;

int init_game(GoGame* go_game, int max_moves, int board_size);
int destroy_game(GoGame* go_game);
int play_move(GoGame* go_game, int color, int i, int j);

#endif