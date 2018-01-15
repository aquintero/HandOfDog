from ai.go.go_player import GoPlayer
import numpy as np


class MCTree:
    def __init__(self, root_state, root_prior_values, root_prior_win_rate):
        self.root = MCNode(None, None, root_state, root_prior_values, root_prior_win_rate)


class MCNode:
    def __init__(self, parent, parent_action, state, prior_values, prior_win_rate):
        self.parent = parent
        self.parent_action = parent_action
        self.state = state
        self.prior_values = prior_values
        self.prior_win_rate = prior_win_rate
        self.visits = np.zeros(prior_values.shape)
        self.post_values = np.zeros(prior_values.shape)
        self.post_win_rate = 0
        self.children = np.empty(prior_values.shape, dtype=object)


class MCSearch:
    def __init__(self, engine, model, root_state, root_prior_values, root_prior_win_rate):
        self.engine = engine
        self.model = model
        self.tree = MCTree(root_state, root_prior_values, root_prior_win_rate)

    def step(self, batch_size=4, alpha=0.03, epsilon=0.25, c=0.01, virtual_loss=2):
        # select

        nodes = []
        actions = []
        for i in range(batch_size):
            node = self.tree.root
            while True:
                noise = np.random.dirichlet(np.full(node.prior_values.shape, alpha))
                confidence = c * (node.prior_values * (1 - epsilon) + noise * epsilon) * np.sqrt(np.sum(node.visits)) / (1 + node.visits)
                action = np.argmax(node.post_values + noise + confidence)
                node.post_values[action] -= virtual_loss  # virtual loss
                if node.children[action] is None:
                    nodes.append(node)
                    actions.append(action)
                    break
                node = node.children[action]

        # evaluate

        batch = []
        for i in range(batch_size):
            batch.append(self.engine.next_state(nodes[i].state, actions[i]))
        values, win_rate = self.model.predict(batch)

        for i in range(batch_size):
            values[i][:-1] *= self.engine.legal_mask(batch[i]).flatten(order='F')
            nodes[i].children[actions[i]] = MCNode(nodes[i], actions[i], batch[i], values[i], win_rate[i])

        # back propagate

        for i in range(batch_size):
            node = nodes[i]
            action = actions[i]
            while True:
                node.visits[action] += 1
                node.post_values[action] += virtual_loss
                node.post_values[action] += (values[i][action] - node.post_values[action]) * (node.visits[action] - 1) / node.visits[action]
                if node.parent is None:
                    break
                action = node.parent_action
                node = node.parent

    def get_prior_values(self):
        return self.tree.root.prior_values

    def get_post_values(self):
        return self.tree.root.post_values

    def get_policy(self, legal_mask, temperature=0.1):
        policy = np.power(self.tree.root.visits, 1 / temperature, dtype=float)
        policy[:-1] *= legal_mask.flatten(order='F')
        if np.max(policy) < 1e-9 or np.max(policy) == np.nan:
            best_moves = np.argwhere(self.tree.root.visits == np.amax(self.tree.root.visits))
            policy = np.zeros(policy.shape)
            policy[best_moves] = 1
            policy[:-1] *= np.array(legal_mask.flatten(order='F'), dtype=float)
            if np.max(policy) < 1e-9 or np.max(policy) == np.nan:
                policy = np.zeros(policy.shape)
                policy[-1] = 1

        policy /= np.max(policy)
        policy /= np.sum(policy)
        return policy

    def choose_action(self, legal_mask, temperature=0.1):
        policy = self.get_policy(legal_mask, temperature=temperature)
        action = np.random.choice(np.arange(policy.size), p=policy)
        if action < 361 and legal_mask.flatten(order='F')[action] == 0:
            raise Exception(f'selected invalid action {action} with probability {policy[action]}')
        return action

    def move_root(self, action):
        if self.tree.root.children[action] is None:
            state = self.engine.next_state(self.tree.root.state, action)
            values, win_rate = self.model.predict([state])
            self.tree.root = MCNode(None, None, state, values, win_rate)
        else:
            self.tree.root = self.tree.root.children[action]
            self.tree.root.parent = None
            self.tree.root.parent_action = None


class MCPlayer(GoPlayer):
    def __init__(self, search, steps_per_move=40):
        self.search = search
        self.steps_per_move = steps_per_move

    def play(self, color, history, n_moves, legal_mask, temperature=0.1):
        for i in range(self.steps_per_move // 4):
            self.search.step(batch_size=4)

        action = self.search.choose_action(legal_mask, temperature=temperature)
        self.search.move_root(action)
        return action
