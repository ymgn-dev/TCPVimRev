# -*- coding:utf-8 -*-
import sys
import socket
from contextlib import closing
import pickle
import time
import random
import argparse

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 4096


def main():
    # parser
    parser = argparse.ArgumentParser(description='VimRev')
    parser.add_argument('-m', '--move', help='select first move or passive move.', choices=['Black', 'White'], required=True)

    # コマンドライン引数の解析
    args = parser.parse_args()

    with closing(sock):
        sock.connect((host, port))

        board = None
        place_candidates = []
        game_turn = None
        my_turn = args.move
        placeloc = -1

        while True:

            time.sleep(2) # sleep 2 seconds

            """ send """
            try:
                if(game_turn == my_turn):
                    random.shuffle(place_candidates) # select the place location
                    placeloc = place_candidates[0]
                else:
                    print('not my turn')
                    placeloc = -1 # not my turn
            except:
                print('catch exceptions')
                placeloc = -1 # catch exceptions
            finally:
                snd_msg = {}
                snd_msg['turn'] = my_turn
                snd_msg['placeloc'] = placeloc
                snd_msg = pickle.dumps(snd_msg) # dump pickle
                sock.send(snd_msg)

            """ receive """
            msg = sock.recv(bufsize)
            msg = pickle.loads(msg)
            print(msg['candidate_move'], msg['turn'])

            # if receive message is valid
            try:
                board = msg['board']
                place_candidates = msg['candidate_move']
                game_turn = msg['turn']
            except:
                sock.close()


if __name__ == '__main__':
    main()