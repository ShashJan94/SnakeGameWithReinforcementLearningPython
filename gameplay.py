import os
import logging
import threading
import pygame
import numpy as np
import matplotlib.pyplot as plt
from snake import Snake
from rat import Rat
from snakeAI import SnakeAI
import sys
from tensorflow.keras.optimizers import Adam
from constants import GRID_WIDTH, GRID_SIZE, GRID_HEIGHT, BLUE, GREEN, WHITE, RED, UP, DOWN, LEFT, RIGHT, BLACK
# Setup logging
logging.basicConfig(level=logging.INFO)


# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE + 100))  # Extra space for buttons
font = pygame.font.SysFont("Arial", 18)


class SnakeGame:
    def __init__(self):
        # Initialize game state variables
        self.button_area_height = None
        self.player_snake = None
        self.ai_snake = None
        self.rat = None
        self.ai_agent = None
        self.player_score = 0
        self.ai_score = 0
        self.level = 1
        self.current_match = 1
        self.total_matches = 3
        self.rats_to_win = 6  # Need to eat more than 5 rats to win
        self.statistics_thread = None
        self.load_model = False
        self.paused = False
        self.running = False  # Game starts in a paused state
        self.buttons = []

        # Update the screen size to fit the buttons
        self.button_height = 30
        self.button_spacing = 10
        self.button_area_height = self.button_height + 2 * self.button_spacing
        self.screen_width = GRID_WIDTH * GRID_SIZE
        self.screen_height = GRID_HEIGHT * GRID_SIZE + self.button_area_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Call reset_game to initialize game state
        self.reset_game()

        # Initialize buttons
        self.initialize_buttons()

    def initialize_buttons(self):
        button_width = (self.screen_width - 20) // 7
        self.buttons = [
            {"label": "Start", "action": self.start_game},
            {"label": "Reset", "action": self.reset_game},
            {"label": "Save State", "action": self.save_game_state},
            {"label": "Load State", "action": self.load_game_state},
            {"label": "Exit", "action": self.exit_game},
            {"label": "Pause", "action": self.toggle_pause},
            {"label": "Statistics", "action": self.show_statistics_thread},
        ]

        for i, button in enumerate(self.buttons):
            button["rect"] = pygame.Rect(
                2 + i * (button_width + self.button_spacing),
                GRID_HEIGHT * GRID_SIZE + self.button_spacing,
                button_width,
                self.button_height
            )

    def start_game(self):
        self.load_ai_model()  # Load the AI model when the game starts
        self.running = True

    def reset_game(self):
        # Reset game-specific variables
        self.player_snake = Snake(GREEN, Snake.randomize_position())
        self.ai_snake = Snake(BLUE, Snake.randomize_center_position())

        # Ensure that the snakes don't start at the same position
        while self.player_snake.get_head_position() == self.ai_snake.get_head_position():
            self.ai_snake = Snake(BLUE, Snake.randomize_center_position())
        self.rat = Rat(RED)
        self.ai_agent = SnakeAI(GRID_WIDTH * GRID_HEIGHT, 4)  # 4 actions: UP, DOWN, LEFT, RIGHT
        self.player_score = 0
        self.ai_score = 0
        self.level = 1
        self.current_match = 1
        self.running = False  # Pause the game until Start is pressed

    def game_loop(self) -> None:
        while True:
            self.handle_events()
            if self.running and not self.paused:
                self.update_game()
                self.draw_game()
            else:
                self.draw_buttons()
            pygame.display.flip()
            clock.tick(self.calculate_speed())  # Use the new method to calculate speed

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player_snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.player_snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.player_snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.player_snake.turn(RIGHT)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()

    def update_game(self):
        if not self.player_snake.move():
            self.display_message("You Lose!")
            self.ai_score += 1
            self.reset_match()

        if not self.ai_snake.move():
            self.display_message("Opponent Loses!")
            self.player_score += 1
            self.reset_match()

        if self.player_snake.get_head_position() == self.rat.position:
            self.player_snake.grow()
            self.player_score += 1
            self.rat.randomize_position()
            if self.player_score >= self.rats_to_win:
                self.display_message("You Win!")
                self.level_up()

        if self.ai_snake.get_head_position() == self.rat.position:
            self.ai_snake.grow()
            self.ai_score += 1
            self.rat.randomize_position()
            if self.ai_score >= self.rats_to_win:
                self.display_message("Opponent Wins!")
                self.level_up()

        if self.check_collision():
            if self.player_score == self.ai_score:
                self.display_message("Draw!")
            elif self.player_score > self.ai_score:
                self.display_message("You Win!")
            else:
                self.display_message("Opponent Wins!")
            self.reset_match()

        self.handle_ai_snake()

    def check_collision(self):
        player_head = self.player_snake.get_head_position()
        ai_head = self.ai_snake.get_head_position()
        return player_head == ai_head

    def handle_ai_snake(self):
        state = np.zeros((1, GRID_WIDTH * GRID_HEIGHT))
        head_pos = self.ai_snake.get_head_position()
        state[0, head_pos[1] // GRID_SIZE * GRID_WIDTH + head_pos[0] // GRID_SIZE] = 1
        action = self.ai_agent.act(state)
        if action == 0:
            self.ai_snake.turn(UP)
        elif action == 1:
            self.ai_snake.turn(DOWN)
        elif action == 2:
            self.ai_snake.turn(LEFT)
        elif action == 3:
            self.ai_snake.turn(RIGHT)

        if not self.ai_snake.move():
            self.ai_snake.alive = False

        next_state = np.zeros((1, GRID_WIDTH * GRID_HEIGHT))
        head_pos = self.ai_snake.get_head_position()
        next_state[0, head_pos[1] // GRID_SIZE * GRID_WIDTH + head_pos[0] // GRID_SIZE] = 1
        reward = -0.1
        if not self.ai_snake.alive:
            reward = -10
        elif self.ai_snake.get_head_position() == self.rat.position:
            reward = 10

        done = not self.ai_snake.alive
        self.ai_agent.remember(state, action, reward, next_state, done)

        if done:
            self.ai_agent.replay(32)

    def draw_game(self):
        screen.fill(BLACK)
        self.player_snake.draw(screen)
        self.ai_snake.draw(screen)
        self.rat.draw(screen)
        self.draw_scoreboard()
        self.draw_buttons()

    def draw_scoreboard(self):
        score_text = font.render(
            f"Player Score: {self.player_score}  AI Score: {self.ai_score}  "
            f"Match: {self.current_match}/{self.total_matches}  Level: {self.level}",
            True, WHITE)
        screen.blit(score_text, [10, 10])

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(screen, WHITE, button["rect"])
            text_surf = font.render(button["label"], True, BLACK)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            screen.blit(text_surf, text_rect)

    def save_game_state(self):
        state = np.array([
            self.player_snake.positions,
            self.ai_snake.positions,
            self.player_score,
            self.ai_score,
            self.rat.position,
            self.level,
            self.current_match,
            self.total_matches
        ], dtype=object)
        if not os.path.exists("game_states"):
            os.makedirs("game_states")
        np.save("game_states/game_state.npy", state)
        logging.info("Game state saved to game_states/game_state.npy")

    def load_game_state(self):
        if os.path.exists("game_states/game_state.npy"):
            state = np.load("game_states/game_state.npy", allow_pickle=True)
            self.player_snake.positions = list(state[0])
            self.ai_snake.positions = list(state[1])
            self.player_score = state[2]
            self.ai_score = state[3]
            self.rat.position = tuple(state[4])
            self.level = state[5]
            self.current_match = state[6]
            self.total_matches = state[7]
            logging.info("Game state loaded from game_states/game_state.npy")

    def show_statistics_thread(self):
        if self.statistics_thread is None or not self.statistics_thread.is_alive():
            self.statistics_thread = threading.Thread(target=self.show_statistics)
            self.statistics_thread.start()

    def show_statistics(self):
        plt.ion()
        fig, axs = plt.subplots(6, 1, figsize=(8, 18))

        while self.running:
            axs[0].clear()
            axs[0].plot(self.ai_agent.loss_history, label='Loss')
            axs[0].set_title('AI Snake Training Loss')
            axs[0].set_xlabel('Episode')
            axs[0].set_ylabel('Loss')
            axs[0].legend()

            axs[1].clear()
            axs[1].plot(self.ai_agent.reward_history, label='Reward')
            axs[1].set_title('AI Snake Reward History')
            axs[1].set_xlabel('Episode')
            axs[1].set_ylabel('Reward')
            axs[1].legend()

            axs[2].clear()
            moving_avg = np.convolve(self.ai_agent.reward_history, np.ones((50,)) / 50, mode='valid')
            axs[2].plot(moving_avg, label='Moving Average of Reward')
            axs[2].set_title('AI Snake Moving Average Reward (Window 50)')
            axs[2].set_xlabel('Episode')
            axs[2].set_ylabel('Average Reward')
            axs[2].legend()

            # Additional plots
            axs[3].clear()
            exploration_rate = [max(self.ai_agent.epsilon * (self.ai_agent.epsilon_decay ** i),
                                    self.ai_agent.epsilon_min) for i in range(len(self.ai_agent.loss_history))]
            axs[3].plot(exploration_rate, label='Exploration Rate')
            axs[3].set_title('Exploration Rate Over Time')
            axs[3].set_xlabel('Episode')
            axs[3].set_ylabel('Exploration Rate')
            axs[3].legend()

            axs[4].clear()
            cumulative_rewards = np.cumsum(self.ai_agent.reward_history)
            axs[4].plot(cumulative_rewards, label='Cumulative Rewards')
            axs[4].set_title('Cumulative Rewards Over Time')
            axs[4].set_xlabel('Episode')
            axs[4].set_ylabel('Cumulative Reward')
            axs[4].legend()

            axs[5].clear()
            predicted_performance = np.convolve(self.ai_agent.reward_history, np.ones((100,)) / 100, mode='valid')
            best_performance = np.max(predicted_performance) if len(predicted_performance) > 0 else 0
            axs[5].plot(predicted_performance, label='Predicted Performance')
            axs[5].axhline(y=best_performance, color='r', linestyle='--', label='Best Performance')
            axs[5].set_title('Predicted Performance (Window 100)')
            axs[5].set_xlabel('Episode')
            axs[5].set_ylabel('Performance')
            axs[5].legend()

            plt.tight_layout()
            plt.pause(0.1)

        plt.ioff()
        plt.show()

    def reset_match(self):
        self.current_match += 1
        if self.current_match > self.total_matches:
            self.level_up()
        else:
            self.initialize_match()

    def initialize_match(self):
        self.player_snake = Snake(GREEN, Snake.randomize_position())
        self.ai_snake = Snake(BLUE, Snake.randomize_center_position())
        # Ensure the starting positions again
        while self.player_snake.get_head_position() == self.ai_snake.get_head_position():
            self.ai_snake = Snake(BLUE, Snake.randomize_center_position())
        self.rat.randomize_position()
        self.player_score = 0
        self.ai_score = 0

    def exit_game(self):
        self.save_ai_model()  # Automatically save the AI model on exit
        self.running = False
        pygame.quit()
        sys.exit()

    def toggle_pause(self):
        self.paused = not self.paused

    def display_message(self, message):
        self.paused = True
        screen.fill(BLACK)
        message_text = font.render(message, True, RED)
        screen.blit(message_text,
                    [GRID_WIDTH * GRID_SIZE // 2 - message_text.get_width() // 2, GRID_HEIGHT * GRID_SIZE // 2])
        pygame.display.flip()
        pygame.time.wait(3000)  # Display the message for 3 seconds
        self.paused = False

    def level_up(self):
        self.level += 1
        self.current_match = 1  # Reset the current match counter
        self.initialize_match()

    def calculate_speed(self):
        # Linear increase in game speed based on the current level
        return 2 + (self.level - 1) * 2

    def save_ai_model(self):
        if self.running:  # Ensure the game has been running before saving
            if not os.path.exists("weights"):
                os.makedirs("weights")
            self.ai_agent.save("weights/snake_ai.weights.h5")
            logging.info("AI model saved to weights/snake_ai.weights.h5")
        else:
            logging.info("Game not started. No weights saved.")

    def load_ai_model(self):
        if not os.path.exists("weights"):
            os.makedirs("weights")
        if os.path.exists("weights/snake_ai.weights.h5"):
            self.ai_agent.load("weights/snake_ai.weights.h5")
            self.ai_agent.model.compile(loss='mse', optimizer=Adam(learning_rate=self.ai_agent.learning_rate))
            logging.info("AI model loaded from weights/snake_ai.weights.h5")
        else:
            logging.info("No AI model found. Starting fresh.")
