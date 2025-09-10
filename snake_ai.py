import os
import sys
import time
import random
import heapq
import termios
import tty

# Game configuration
WIDTH = 20
HEIGHT = 15
SLEEP_TIME = 0.15  # time between steps

DIRS = [(0,1),(0,-1),(1,0),(-1,0)]  # right, left, down, up

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(snake, food):
    clear_screen()
    for r in range(HEIGHT):
        line = ''
        for c in range(WIDTH):
            if (r,c) == food:
                line += 'F'
            elif (r,c) == snake[0]:
                line += 'H'  # Head
            elif (r,c) in snake[1:]:
                line += 'S'  # Body
            elif r == 0 or r == HEIGHT-1 or c == 0 or c == WIDTH-1:
                line += '#'
            else:
                line += ' '
        print(line)
    print("\nSnake length:", len(snake))
    print("AI-controlled snake. Press Ctrl+C to quit.")

def neighbors(pos, snake_set):
    r,c = pos
    results = []
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        # inside board and not snake body (except tail - special case)
        if 0 < nr < HEIGHT-1 and 0 < nc < WIDTH-1 and (nr,nc) not in snake_set:
            results.append((nr,nc))
    return results

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star(start, goal, snake_set):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start:0}
    closed_set = set()

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_set.add(current)

        for neighbor in neighbors(current, snake_set):
            if neighbor in closed_set:
                continue
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))

    return None

def spawn_food(snake):
    empty_spaces = [(r,c) for r in range(1, HEIGHT-1) for c in range(1, WIDTH-1) if (r,c) not in snake]
    return random.choice(empty_spaces)

def main():
    snake = [(HEIGHT//2, WIDTH//2), (HEIGHT//2, WIDTH//2 - 1), (HEIGHT//2, WIDTH//2 - 2)]
    food = spawn_food(snake)

    try:
        while True:
            snake_set = set(snake)
            path = a_star(snake[0], food, snake_set)
            if path is None or len(path) == 0:
                # No path found, try to move safely (any valid neighbor)
                safe_moves = neighbors(snake[0], snake_set)
                if not safe_moves:
                    print("No moves left! Game Over.")
                    break
                next_move = safe_moves[0]
            else:
                next_move = path[0]

            # Move snake
            snake.insert(0, next_move)
            if next_move == food:
                food = spawn_food(snake)  # spawn new food
            else:
                snake.pop()  # remove tail

            print_board(snake, food)
            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("\nGame stopped by user.")

if __name__ == "__main__":
    main()

