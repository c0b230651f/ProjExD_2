import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5),
         pg.K_DOWN:(0, +5),
         pg.K_LEFT:(-5, 0),
         pg.K_RIGHT:(+5, 0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def roto_zoom(kk_img: pg.Surface, tpl: tuple) -> pg.Surface:
    """
    引数：kk_img、押下キーに対する移動量の合計値タプル
    戻り値：回転、反転処理後のこうかとんSurface
    こうかとん画像の切り替え処理を行う関数
    """
    fl_kk_img = pg.transform.flip(kk_img, True, False)
    roto_dic = {(0, -5):pg.transform.rotozoom(fl_kk_img, 90.0, 1.0),
                (+5, -5):pg.transform.rotozoom(fl_kk_img, 45.0, 1.0),
                (+5, 0):fl_kk_img,
                (+5, +5):pg.transform.rotozoom(fl_kk_img, -45.0, 1.0),
                (0, +5):pg.transform.rotozoom(fl_kk_img, -90.0, 1.0),
                (-5, +5):pg.transform.rotozoom(kk_img, 45.0, 1.0),
                (-5, -5):pg.transform.rotozoom(kk_img, -45.0, 1.0),
                (-5, 0):kk_img,
                (0, 0):fl_kk_img,
                }
    return roto_dic[tpl]

def game_over(screen):
    """
    引数：screen
    戻り値：なし
    ゲームオーバー時の描画を行う関数
    """
    go_bg = pg.Surface((WIDTH, HEIGHT))
    go_kk_img = pg.image.load("fig/8.png")
    go_kk_l_rct = (WIDTH/2 - 200, HEIGHT/2)
    go_kk_r_rct = (WIDTH/2 + 200, HEIGHT/2)
    go_rct = pg.Rect(0, 0, WIDTH, HEIGHT)
    pg.draw.rect(go_bg, (0, 0, 0), go_rct)
    go_bg.set_alpha(156)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER",
                       True, (255, 0, 0))
    screen.blit(go_bg, (0, 0))
    screen.blit(go_kk_img, go_kk_l_rct)
    screen.blit(go_kk_img, go_kk_r_rct)
    screen.blit(txt, [WIDTH/2-150, HEIGHT/2])
    pg.display.update()
    pg.time.wait(5000)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん　または　爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾が重なっていたら
            print("GAME OVER")
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(roto_zoom(kk_img, tuple(sum_mv)), kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
