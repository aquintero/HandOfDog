#include "go_board.h"

 const int directions[4][2] = {
    {0, 1},
    {0, -1},
    {1, 0},
    {-1, 0},
};

int position_to_index(int size, int i, int j){
    return i + j * size;
}

int init_board(GoBoard* go_board, int size){
    go_board->size = size;
    go_board->board = (int*)malloc(size * sizeof(int));
    for(int i = 0; i < go_board->size * go_board->size; i++){
        go_board->board[i] = EMPTY;
    }
    return 0;
}

int copy_board(GoBoard* from, GoBoard* to){
    init_board(to, from->size);
    for(int i = 0; i < to->size * to->size; i++){
        to->board[i] = from->board[i];
    }
    return 0;
}

bool board_equals(GoBoard* b1, GoBoard* b2){
    for(int i = 0; i < b1->size * b1->size; i++){
        if(b1->board[i] != b2->board[i]){
            return false;
        }
    }
    return true;
}

int destroy_board(GoBoard* go_board){
    free(go_board->board);
    return 0;
}

int reset_board(GoBoard* go_board){
    for(int i = 0; i < go_board->size * go_board->size; i++){
        go_board->board[i] = EMPTY;
    }
    return 0;
}

bool is_in_bounds(GoBoard* go_board, int i, int j){
    return !(i < 0 || j < 0 || i >= go_board->size || j >= go_board->size);
}

int reach_color(GoBoard* go_board, int color, int i, int j, bool* ret){
    if(!is_in_bounds(go_board, i, j)){
        return -1;
    }

    bool* visited = malloc(go_board->size * go_board->size * sizeof(bool));
    for(int vi = 0; vi < go_board->size * go_board->size; vi++){
        visited[vi] = false;
    }

    int idx = i + j * go_board->size;
    int start_color = go_board->board[idx];
    *ret = _reach_color_recursive(go_board, color, i, j, visited);

    free(visited);
    return 0;
}

bool _reach_color_recursive(GoBoard* go_board, int color, int i, int j, bool* visited){
    int idx = position_to_index(go_board->size, i, j);
    visited[idx] = true;
    int start_color = go_board->board[idx];
    for(int di = 0; di < 4; di++){
        const int* dir = directions[di];
        int ni = i + dir[0];
        int nj = j + dir[1];
        if(!is_in_bounds(go_board, ni, nj)){
            continue;
        }
        int nidx = position_to_index(go_board->size, ni, nj);
        if(visited[nidx]){
            continue;
        }
        if(go_board->board[nidx] == color){
            return true;
        }
        if(go_board->board[nidx] == start_color){
            _reach_color_recursive(go_board, color, ni, nj, visited);
        }
    }
    return false;
}

int clear(GoBoard* go_board, int i, int j){
    if(!is_in_bounds(go_board, i, j)){
        return -1;
    }

    int idx = position_to_index(go_board->size, i, j);
    int color = go_board->board[idx];
    if(color == EMPTY){
        return 0;
    }
    bool reach_empty;
    reach_color(go_board, EMPTY, i, j, &reach_empty);
    if(reach_empty){
        return 0;
    }
    _clear_recursive(go_board, i, j);

    return 0;
}

int _clear_recursive(GoBoard* go_board, int i, int j){
    if(!is_in_bounds(go_board, i, j)){
        return -1;
    }

    int idx = position_to_index(go_board->size, i, j);
    int color = go_board->board[idx];
    if(color == EMPTY){
        return 0;
    }
    go_board->board[idx] = EMPTY;
    for(int di = 0; di < 4; di++){
        const int* dir = directions[di];
        int ni = i + dir[0];
        int nj = j + dir[1];
        int nidx = position_to_index(go_board->size, ni, nj);
        if(!is_in_bounds(go_board, ni, nj || color != go_board->board[nidx])){
            continue;
        }
        _clear_recursive(go_board, ni, nj);
    }
}