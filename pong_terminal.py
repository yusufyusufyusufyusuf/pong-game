import curses
import time
import random

# Game settings
HEIGHT = 20
WIDTH = 60
PADDLE_HEIGHT = 4
BALL_CHAR = 'O'
PADDLE_CHAR = '|'
SPEED = 0.05

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(0)
    sh, sw = HEIGHT, WIDTH

    # Initial positions
    player_y = sh // 2 - PADDLE_HEIGHT // 2
    ai_y = sh // 2 - PADDLE_HEIGHT // 2
    ball_x, ball_y = sw // 2, sh // 2
    ball_vx = random.choice([-1, 1])
    ball_vy = random.choice([-1, 1])
    player_score = 0
    ai_score = 0

    while True:
        stdscr.clear()
        # Draw top/bottom borders
        for x in range(sw):
            stdscr.addch(0, x, '#')
            stdscr.addch(sh - 1, x, '#')
        # Draw paddles
        for i in range(PADDLE_HEIGHT):
            stdscr.addch(player_y + i, 2, PADDLE_CHAR)
            stdscr.addch(ai_y + i, sw - 3, PADDLE_CHAR)
        # Draw ball
        stdscr.addch(ball_y, ball_x, BALL_CHAR)
        # Draw scores
        score_text = f"{player_score} : {ai_score}"
        stdscr.addstr(0, sw // 2 - len(score_text)//2, score_text)
        stdscr.refresh()

        # Input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('w') and player_y > 1:
            player_y -= 1
        elif key == ord('s') and player_y < sh - PADDLE_HEIGHT - 1:
            player_y += 1

        # AI paddle movement
        if ai_y + PADDLE_HEIGHT//2 < ball_y and ai_y < sh - PADDLE_HEIGHT - 1:
            ai_y += 1
        elif ai_y + PADDLE_HEIGHT//2 > ball_y and ai_y > 1:
            ai_y -= 1

        # Ball movement
        ball_x += ball_vx
        ball_y += ball_vy

        # Wall collision
        if ball_y <= 1 or ball_y >= sh - 2:
            ball_vy *= -1

        # Paddle collision - player
        if ball_x == 3 and player_y <= ball_y < player_y + PADDLE_HEIGHT:
            ball_vx *= -1
        # Paddle collision - AI
        elif ball_x == sw - 4 and ai_y <= ball_y < ai_y + PADDLE_HEIGHT:
            ball_vx *= -1

        # Score
        if ball_x <= 0:
            ai_score += 1
            ball_x, ball_y = sw // 2, sh // 2
            ball_vx = random.choice([-1, 1])
            ball_vy = random.choice([-1, 1])
        elif ball_x >= sw - 1:
            player_score += 1
            ball_x, ball_y = sw // 2, sh // 2
            ball_vx = random.choice([-1, 1])
            ball_vy = random.choice([-1, 1])

        time.sleep(SPEED)

if __name__ == "__main__":
    curses.wrapper(main)
