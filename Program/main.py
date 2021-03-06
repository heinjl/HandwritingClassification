from PIL import Image
import numpy
import sys
import pygame
pygame.init()
from classifier import Classifier
import dbscan
import py_dbscan

import time

# defining some global connstants
black = 0, 0, 0
white = 255, 255, 255
size = 500, 100
image_size = 28, 28
mouse_was_pressed = False
eraser_mode = False
r = 10

threshold_num = 6
eps = 1

prev = pygame.mouse.get_pos()
current = pygame.mouse.get_pos()
save_path = '/home/coleman/Pictures/saved.bmp'


time_both = False
use_c_dbscan = True


def check_input( display, classifier):
    global prev, current, mouse_was_pressed, eraser_mode, save_path

    for event in pygame.event.get():
        # keyboard input
        if event.type == pygame.KEYDOWN:
            # which key?    

            if event.key == pygame.K_RETURN:
                print 'Enter pressed'

                if time_both:
                    c_start = time.time()
                    vectors = py_dbscan.c_get_square_cluster_image_vectors( display, image_size, threshold_num, eps)
                    c_time = time.time() - c_start

                    print  'c clusters: {0}'.format( len(vectors) )

                    python_start = time.time()
                    vectors = py_dbscan.py_get_square_cluster_image_vectors( display, image_size, threshold_num, eps)
                    python_time = time.time() - python_start

                    print 'Python clusters: {0}'.format(len(vectors))
                
                elif use_c_dbscan:
                    c_start = time.time()
                    vectors = py_dbscan.c_get_square_cluster_image_vectors( display, image_size, threshold_num, eps)
                    c_time = time.time() - c_start
                    print  'c clusters: {0}'.format( len(vectors) )
                    print 'Time taken (c): {0:.4f}'.format(c_time)
                else: 
                    python_start = time.time()
                    vectors = py_dbscan.py_get_square_cluster_image_vectors( display, image_size, threshold_num, eps)
                    python_time = time.time() - python_start
                    print 'Python clusters: {0}'.format(len(vectors))
                    print 'Time taken (python): {0:.4f}'.format(python_time)

                    
                title = ''
                for v in vectors:
                    title += str(classifier.predict(v)[0])
                pygame.display.set_caption(title)

                print 'Prediction: {0}'.format(title)
                if time_both:
                    print 'Python time: {0:.4f}\nC time: {1:.4f}\nPython/C: {2:0.4f}'\
                            .format(python_time, c_time, python_time/c_time)

                surf = py_dbscan.color_clusters( display, threshold_num, eps )
                display.blit( surf, (0, 0) )
                pygame.display.update()

            if event.key == pygame.K_e:
                print "'e' pressed"
                display.fill( white )

            if event.key == pygame.K_s:
                print "'s' pressed"
                pygame.image.save(display, save_path)


        # the 'X' arrow
        if event.type == pygame.QUIT:
            exit_application()
       
        if pygame.mouse.get_pressed()[1]:
            eraser_mode = True
        else:
            eraser_mode = False

        if pygame.mouse.get_pressed()[0]:
            prev = current
            current = pygame.mouse.get_pos()
            if eraser_mode:
                c = white
            else:
                c = black
            draw_on_mouse( display, r, c, prev, current )
 
        else:
            mouse_pressed = False
            prev = pygame.mouse.get_pos()
            current = pygame.mouse.get_pos()

def draw_on_mouse( display, radius, color, prev, curr ):
    pygame.draw.line( display, color, prev, curr, radius )    



def exit_application():
    sys.exit()




def main():
    
    classifier = Classifier()
    background_color = white
    display = pygame.display.set_mode(size)
    display.fill(background_color)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        check_input( display, classifier )            
        pygame.display.update()





if __name__ == "__main__":
    main()
