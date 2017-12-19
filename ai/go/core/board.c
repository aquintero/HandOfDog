#include "board.h"

bool _reach_color_recursive(int* board, int size, int color, int i, int j, bool* visited);
void _clear_recursive(int* board, int size, int i, int j);
int _2D(int dim1, int i, int j);
int _3D(int dim1, int dim2, int i, int j, int k);

const int directions[4][2] = {
	{ 0, 1 },
	{ 0, -1 },
	{ 1, 0 },
	{ -1, 0 },
};

bool is_in_bounds(int size, int i, int j) {
	return !(i < 0 || j < 0 || i >= size || j >= size);
}

bool reach_color(int* board, int size, int size2, int color, int i, int j) {
	if (!is_in_bounds(size, i, j))
		return false;
	bool* visited = (bool*) malloc(size * size * sizeof(bool));

	for (int vi = 0; vi < size; vi++)
		for(int vj = 0; vj < size; vj++)
			visited[_2D(size, vi, vj)] = false;

	int start_color = board[_2D(size, i, j)];
	bool ret = _reach_color_recursive(board, size, color, i, j, visited);

	free(visited);
	return ret;
}

bool _reach_color_recursive(int* board, int size, int color, int i, int j, bool* visited) {
	visited[_2D(size, i, j)] = true;
	int start_color = board[_2D(size, i, j)];
	for (int di = 0; di < 4; di++) {
		const int* dir = directions[di];
		int ni = i + dir[0];
		int nj = j + dir[1];
		if (!is_in_bounds(size, ni, nj) || visited[_2D(size, ni, nj)])
			continue;
		if (board[_2D(size, ni, nj)] == color)
			return true;
		if (board[_2D(size, ni, nj)] == start_color && _reach_color_recursive(board, size, color, ni, nj, visited))
			return true;
	}
	return false;
}

bool clear(int* board, int size, int size2, int i, int j) {
	if (!is_in_bounds(size, i, j))
		return false;
	int color = board[_2D(size, i, j)];
	if (color == EMPTY)
		return false;
	bool reach_empty = reach_color(board, size, size, EMPTY, i, j);
	if (reach_empty)
		return false;
	_clear_recursive(board, size, i, j);
	return true;
}

void _clear_recursive(int* board, int size, int i, int j) {
	int color = board[_2D(size, i, j)];
	if (color == EMPTY)
		return;
	board[_2D(size, i, j)] = EMPTY;
	for (int di = 0; di < 4; di++) {
		const int* dir = directions[di];
		int ni = i + dir[0];
		int nj = j + dir[1];
		if (!is_in_bounds(size, ni, nj) || color != board[_2D(size, ni, nj)])
			continue;
		_clear_recursive(board, size, ni, nj);
	}
}

void score(int* board, int size, int size2, int score[2]) {
	int w = 0;
	int b = 0;
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			int color = board[_2D(size, i, j)];
			if (color == WHITE) 
				w++;
			else if (color == BLACK) 
				b++;
			else {
				bool reach_black = reach_color(board, size, size, BLACK, i, j);
				bool reach_white = reach_color(board, size, size, WHITE, i, j);
				if (reach_black && !reach_white)
					b++;
				else if (reach_white && !reach_black)
					w++;
			}
		}
	}
	score[0] = b;
	score[1] = w;
}

// No ko rule
bool play_stone(int* board, int size, int size2, int color, int i, int j) {
	if (!is_in_bounds(size, i, j) || board[_2D(size, i, j)] != EMPTY)
		return false;
	board[_2D(size, i, j)] = color;
	if (reach_color(board, size, size, EMPTY, i, j))
		return true;
	for (int di = 0; di < 4; di++) {
		const int* dir = directions[di];
		int ni = i + dir[0];
		int nj = j + dir[1];
		if (!is_in_bounds(size, ni, nj))
			continue;
		if (board[_2D(size, ni, nj)] == -color)
			clear(board, size, size, ni, nj);
	}
	if (reach_color(board, size, size, EMPTY, i, j))
		return true;
	return false;
}

void legal_moves(int* board, int size, int size2, int* board_history, int n_boards, int size3, int size4, int color, int* legal_moves, int size5, int size6) {
	int* temp_board = malloc(size * size * sizeof(int));

	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			if (board[_2D(size, i, j)] != EMPTY) {
				legal_moves[_2D(size, i, j)] = 0;
				continue;
			}
			for (int k = 0; k < size; k++)
				for (int l = 0; l < size; l++)
					temp_board[_2D(size, k, l)] = board[_2D(size, k, l)];
			if (!play_stone(temp_board, size, size, color, i, j)) {
				legal_moves[_2D(size, i, j)] = 0;
				continue;
			}
			bool copy = 1;
			for (int t = 0; t < n_boards; t++){
                copy = 1;
				for (int k = 0; k < size && copy; k++)
					for (int l = 0; l < size && copy; l++)
						if (board_history[_3D(size, size, t, k, l)] != temp_board[_2D(size, k, l)])
							copy = 0;
                if(copy)
                    break;
            }
			legal_moves[_2D(size, i, j)] = !copy;
		}
	}

	free(temp_board);
}


int _2D(int dim1, int i, int j){
    return dim1 * i + j;
}

int _3D(int dim1, int dim2, int i, int j, int k){
    return dim1 * dim2 * i + j * dim2 + k ;
}