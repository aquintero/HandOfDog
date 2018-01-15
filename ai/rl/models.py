from keras.layers import Input, Dense, Conv2D, Flatten
from keras.models import Model
from keras import regularizers
import numpy as np


class CNNModel:
    def __init__(self, board_size=19):
        self.board_size = board_size

        self._input_board = Input(shape=(3, board_size, board_size))
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(self._input_board)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = Conv2D(32, (3, 3), padding='same', activation='relu')(x)

        policy = Conv2D(2, (1, 1), padding='same', activation='relu')(x)
        policy = Flatten()(policy)
        policy = Dense(board_size * board_size + 1, activation='sigmoid', kernel_regularizer=regularizers.l2(0.0001))(policy)

        value = Conv2D(1, (1, 1), padding='same', activation='relu')(x)
        value = Flatten()(value)
        value = Dense(1, activation='sigmoid', kernel_regularizer=regularizers.l2(0.0001))(value)

        self._outputs = [policy, value]

        self.model = Model(inputs=self._input_board, outputs=self._outputs)
        self.model.compile(loss=['binary_crossentropy', 'mean_squared_error'], optimizer='adadelta')

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_weights(self):
        self.model.get_weights()

    def predict(self, states):
        x = []
        for i in range(len(states)):
            x.append(np.zeros((3, self.board_size, self.board_size)))
            x[i][0] = states[i].color
            x[i][1:] = states[i].history
        x = np.array(x)
        values, win_rate = self.model.predict(x, self.board_size)
        return np.squeeze(values), np.squeeze(win_rate)
