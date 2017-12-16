#include "go_game.h"

int init_game(GoGame* go_game, int max_moves, int board_size){
    go_game->boards = (GoBoard*)malloc((max_moves + 1) * sizeof(GoBoard));
    init_board(&go_game->boards[0], board_size);
    go_game->board_size = board_size;

    go_game->moves = (int*)malloc(max_moves * sizeof(int));
    go_game->n_moves = 0;
    go_game->max_moves = max_moves;

    int board_size2 = board_size * board_size;

    go_game->legal_moves = (bool**)malloc((max_moves + 1) * sizeof(bool));
    go_game->legal_moves[0] = (bool*)malloc((max_moves + 1) * board_size2 * sizeof(bool));
    for(int i = 1; i < (max_moves + 1); i++){
        go_game->legal_moves[i] = go_game->legal_moves[i - 1] + board_size2;
    }
    for(int i = 1; i < board_size2; i++){
        go_game->legal_moves[0][i] = true;
    }
    return 0;
}

int destroy_game(GoGame* go_game){
    free(go_game->boards);
    free(go_game->moves);
    free(go_game->legal_moves[0]);
    free(go_game->legal_moves);
}

int play_move(GoGame* go_game, int color, int i, int j){
    if(go_game->n_moves == go_game->max_moves){
        return -1;
    }
    GoBoard* go_board = &go_game->boards[go_game->n_moves];
    int move = i + j * go_game->board_size;
    if(go_board->board[move] != EMPTY){
        return -2;
    }
    if(!go_board->board[move]){
        return -3;
    }
    go_game->moves[go_game->n_moves] = move;
    go_game->n_moves++;
    copy_board(&go_game->boards[go_game->n_moves - 1], &go_game->boards[go_game->n_moves]);
    go_board = &go_game->boards[go_game->n_moves];
    go_board->board[move] = color;

    bool reach_empty = false;
    reach_color(go_board, EMPTY, i, j, &reach_empty);
    if(!reach_empty){
        for(int di = 0; di < 4; di++){
            const int* dir = directions[di];
            int ni = i + dir[0];
            int nj = j + dir[1];
            int nidx = position_to_index(go_game->board_size, ni, nj);
            if(!is_in_bounds(go_board, ni, nj) || go_board->board[nidx] != -color){
                continue;
            }
            clear(go_board, ni, nj);
        }
    }

    bool* mask = go_game->legal_moves[go_game->n_moves];
    for(int ni = 0; ni < go_game->board_size; ni++){
        for(int nj = 0; nj < go_game->board_size; nj++){
            int nidx = position_to_index(go_game->board_size, ni, nj);
            GoBoard* temp_board;
            copy_board(go_board, temp_board);

            if(temp_board->board[nidx] != EMPTY){
                mask[nidx] = false;
                destroy_board(temp_board);
                continue;
            }
            temp_board->board[nidx] = color;

            reach_empty = false;
            reach_color(temp_board, EMPTY, ni, nj, &reach_empty);
            if(reach_empty){
                mask[nidx] = false;
                destroy_board(temp_board);
                continue;
            }

            for(int di = 0; di < 4; di++){
                const int* dir = directions[di];
                int nni = ni + dir[0];
                int nnj = nj + dir[1];
                int nnidx = position_to_index(go_game->board_size, nni, nnj);
                if(!is_in_bounds(temp_board, nni, nnj) || temp_board->board[nnidx] != -color){
                    continue;
                }
                clear(temp_board, nni, nnj);
            }

            reach_empty = false;
            reach_color(temp_board, EMPTY, ni, nj, &reach_empty);
            if(!reach_empty){
                mask[nidx] = false;
                destroy_board(temp_board);
                continue;
            }

            // superko rule
            int start = go_game->n_moves > 4 ? go_game->n_moves - 5 : 0;
            bool repeated = false;
            for(int t = start; t <= go_game->n_moves; t++){
                if(board_equals(temp_board, &go_game->boards[t])){
                    mask[nidx] = false;
                    destroy_board(temp_board);
                    repeated = true;
                    break;
                }
            }
            if(repeated){
                continue;
            }
            destroy_board(temp_board);
            mask[nidx] = true;
        }
    }

    return 0;
}