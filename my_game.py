# 게임 생성을 위한 pygame 임포트
import pygame
import random
from enemy_class import Enemy

# 게임 생성을 위한 초기화(필수)
pygame.init()

# 게임 화면 설정 / 게임 타이틀 설정
screen_w = 800 # 가로
screen_h = 640 # 세로
screen = pygame.display.set_mode((screen_w, screen_h))  # 가로, 세로 크기의 게임창 생성
background = pygame.image.load('img/back2.png')         # 게임 창의 배경화면
pygame.display.set_caption("RUN") # 게임 이름

# FPS 설정
clock = pygame.time.Clock()

# 나의 메인 캐릭터
hero = pygame.image.load('img/hero.png')
# 캐릭터의 경우, 나중에 적과 부딪히거나 무기를 발사하는 이벤트때문에 정확한 크기 재야함
hero_size = hero.get_rect().size # 이미지의 크기를 구해옴;
hero_w = hero_size[0] # 캐릭터 가로 길이
hero_h = hero_size[1] # 캐릭터 세로 길이
hero_x_pos = (screen_w / 2) - (hero_w / 2)      # 캐릭터의 x 좌표
hero_y_pos = screen_h - hero_h                    # 캐릭터의 y 좌표

# 캐릭터가 이동할 좌표
move_x = 0
move_y = 0

#  적 캐릭터
enemies = [
    pygame.transform.scale(pygame.image.load('img/enemy 1.png'), (80, 80)),
    pygame.transform.scale(pygame.image.load('img/enemy 2.png'), (80, 80)),
    pygame.transform.scale(pygame.image.load('img/enemy 3.png'), (80, 80)),
    pygame.transform.scale(pygame.image.load('img/enemy 4.png'), (80, 80)),
    pygame.transform.scale(pygame.image.load('img/enemy 5.png'), (80, 80))
]

# enemies에서 랜덤하게 적 꺼내오기
enemy = random.choice(enemies)
enemy_size = enemy.get_rect().size
enemy_w = enemy_size[0]
enemy_h = enemy_size[1]

# 캐릭터가 바닥에 닿고 위로 올라가게 되면 y값이 작아지므로 마이너스 적용
enemy_speed = [-18, -15, -12, -15, -16]

# 적의 랜덤한 위치 좌표
coor_x = random.randrange(0, screen_w - enemy_w) # 적의 x 좌표
coor_y = random.randrange(0, screen_h - enemy_h) # 적의 y좌표

# 적 캐릭터들이 들어올 리스트
enemy_li = []
# Enemy(랜덤한 x좌표, 랜덤한 y좌표, 인덱스번호, 적의 x축 이동방향(왼:-3, 오:3), 적의 y축 이동방향, 적 속도)
enemy_li.append(Enemy(coor_x, coor_y, 0, 3, -6, enemy_speed[0]))
enemy_li.append(Enemy(coor_x, coor_y, 1, -3, -6, enemy_speed[1]))
enemy_li.append(Enemy(coor_x, coor_y, 2, 3, -6, enemy_speed[2]))
enemy_li.append(Enemy(coor_x, coor_y, 3, -3, -6, enemy_speed[3]))
enemy_li.append(Enemy(coor_x, coor_y, 4, 3, -6, enemy_speed[4]))

# 게임 폰트 정의
game_font = pygame.font.Font(None, 40)

# 총 게임시간
total_time = 60
# 시작 시간
start_ticks = pygame.time.get_ticks()

# 게임 종료 메세지
game_result = "GAME OVER!!!!!"

# 이벤트 루프를 통해 게임이 혼자 종료되지 않고 대기할 수 있도록 함
running = True  # 이 상태는 게임이 진행되고 있는 상태
while running:
    # 게임 화면의 초당 프레임 수 설정
    frame_ps = clock.tick(60)

    for event in pygame.event.get():    # 파이게임의 이벤트들 중에서
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생한다면
            running = False                   # 게임을 종료해라

        # pygame의 키보드 이벤트를 정의하는 부분
        if event.type == pygame.KEYDOWN: # 내가 키보드를 눌렀어 만약에
            if event.key == pygame.K_LEFT:  # 내가 누른게 왼쪽 방향키라면
                move_x -= 3                         # 왼쪽으로 가야되니까 까줘야지
            elif event.key == pygame.K_RIGHT: # 내가 누른게 오른쪽 방향키라면
                move_x += 3                         # 오른쪽으로 가니까 더하기
            elif event.key == pygame.K_UP:      # 내가 누른게 위 방향키라면
                move_y -= 3                               # 위로 가니까 까줘야지
            elif event.key == pygame.K_DOWN:    # 내가 누른게 아래 방향키라면
                move_y += 3                             # 아래로 가니까 더하기
        # 만약 게임하다가 방향키를 떼면 멈춤
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                move_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                move_y = 0

    # 캐릭터가 움직인 좌표 계산이 끝나면 여기서 캐릭터의 위치 적용
    # for 문 안에서 이 작업을 하게 되면 for문이 돌 때마다 값이 변할 수 있음
    hero_x_pos += move_x * frame_ps
    hero_y_pos += move_y * frame_ps

    # 가로 경곗값 처리 (화면 좌우로 나가지 못하도록)
    if hero_x_pos < 0:  # 화면의 가장 왼쪽 밖으로 나가게 되면
        hero_x_pos = 0  # 못 나가게 x좌표를 0으로 준다.
    elif hero_x_pos > screen_w - hero_w:    # 화면의 가장 오른쪽 밖으로 나가게 되면
        hero_x_pos = screen_w - hero_w  # hero의 사진이 딱 벽에 닿을 때의 x좌표를 준다.

    # 세로 경곗값 처리 (화면 위아래로 나가지 못하도록)
    if hero_y_pos < 0:  # 화면의 가장 위쪽 밖으로 나가게 되면
        hero_y_pos = 0  # 못 나가게 y좌표를 0으로 준다.
    elif hero_y_pos > screen_h - hero_h:  # 화면의 가장 아래쪽 밖으로 나가게 되면
        hero_y_pos = screen_h - hero_h  # hero의 사진이 딱 바닥에 닿을 때의 y좌표를 준다.

    # 적 위치 정의
    for enemy in enemy_li: # enemy_li 안에 들어있는 요소들은 클래스! 클래스의 값을 불러올 때는 클래스.값으로 불러옴!!
        # 가로벽에 닿았을 때 적의 이동위치를 변경해주자
        if enemy.pos_x < 0 or enemy.pos_x > (screen_w - enemy_w):
            enemy.enemy_move_x = enemy.enemy_move_x * -1

        # 밑바닥에서 튕겨 올라가는 처리
        if enemy.pos_y >= screen_h - enemy_h:
            enemy.enemy_move_y = enemy.init_speed_y
        else:
            # 그 외의 모든 경우에는 속도를 증가(시작값이 원래 음수) -> 포물선 효과
            enemy.enemy_move_y += 0.5

        enemy.pos_x += enemy.enemy_move_x
        enemy.pos_y += enemy.enemy_move_y

    # 충돌 처리
    # 캐릭터 rect 정보
    hero_rect = hero.get_rect()
    hero_rect.left = hero_x_pos
    hero_rect.bottom = hero_y_pos

    for enemy in enemy_li:
        enemy_pos_x = enemy.pos_x
        enemy_pos_y = enemy.pos_y
        enemy_index = enemy.e_idx

        # 적 rect 정보
        enemy_rect = enemies[enemy_index].get_rect()
        enemy_rect.left = enemy_pos_x
        enemy_rect.bottom = enemy_pos_y

        # 충돌한다잉~
        if hero_rect.colliderect(enemy_rect):
            running = False
            break

    screen.blit(background, (0, 0)) # 배경을 그림; 위에서 설정한 백그라운드를 게임창의 (0, 0) 위치에 그려줌
    screen.blit(hero, (hero_x_pos, hero_y_pos)) # 메인 캐릭터를 그림
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(f"Time : {int(total_time - elapsed_time)}", True, (255, 255, 255))

    # 적 캐릭터를 그림
    if elapsed_time < 10:
        screen.blit(enemies[0], (enemy_li[0].pos_x, enemy_li[0].pos_y))
    if elapsed_time > 10:
        screen.blit(enemies[0], (enemy_li[0].pos_x, enemy_li[0].pos_y))
        screen.blit(enemies[1], (enemy_li[1].pos_x, enemy_li[1].pos_y))
    if elapsed_time > 20:
        screen.blit(enemies[0], (enemy_li[0].pos_x, enemy_li[0].pos_y))
        screen.blit(enemies[1], (enemy_li[1].pos_x, enemy_li[1].pos_y))
        screen.blit(enemies[2], (enemy_li[2].pos_x, enemy_li[2].pos_y))
    if elapsed_time > 30:
        screen.blit(enemies[0], (enemy_li[0].pos_x, enemy_li[0].pos_y))
        screen.blit(enemies[1], (enemy_li[1].pos_x, enemy_li[1].pos_y))
        screen.blit(enemies[2], (enemy_li[2].pos_x, enemy_li[2].pos_y))
        screen.blit(enemies[3], (enemy_li[3].pos_x, enemy_li[3].pos_y))
    if elapsed_time > 40:
        screen.blit(enemies[0], (enemy_li[0].pos_x, enemy_li[0].pos_y))
        screen.blit(enemies[1], (enemy_li[1].pos_x, enemy_li[1].pos_y))
        screen.blit(enemies[2], (enemy_li[2].pos_x, enemy_li[2].pos_y))
        screen.blit(enemies[3], (enemy_li[3].pos_x, enemy_li[3].pos_y))
        screen.blit(enemies[4], (enemy_li[4].pos_x, enemy_li[4].pos_y))

    screen.blit(timer, (10, 10))
    # 시간이 초과됐다면
    if total_time - elapsed_time <= 0:
        game_result = "YOU WIN!!!!"
        running = False

    pygame.display.update() # pygame에서는 배경화면을 매번 그려줘야 함! 수시로 업뎃한다고 생각하자!

# 게임오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_w/2), int(screen_h/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 메시지를 보여주기위해서 3초 대기합니다
pygame.time.delay(3000)

# pygame.종료
pygame.quit()