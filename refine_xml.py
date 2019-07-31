# /!/usr/bin/python

# -*-coding:utf-8-*-

import os
import sys
import re
from xml.etree import ElementTree


def refine_xml(input_path, output_path):

    open_dir = os.listdir(input_path)
    with open(os.path.join(output_path, "output.txt"), 'w') as new_file:
        for input_fname in open_dir:
            with open(os.path.join(input_path, input_fname), 'r') as file:
                xml = file.read()
            xml = xml.replace('\n', '')

            extract_filename = re.compile(r'<filename>(.*?)\<\/filename\>')
            extract_check_ai = re.compile(r'<result>(.*?)\<\/result\>')
            extract_check_human = re.compile(r'<groundtruth>(.*?)\<\/groundtruth\>')

            match_filename = re.search(extract_filename, xml)
            match_ai = re.search(extract_check_ai, xml)
            match_human = re.search(extract_check_human, xml)
            
            if not match_filename:
                continue
                
            filename = match_filename.group(1)
            if match_ai:
                check_ai = match_ai.group(1)
            else:
                check_ai = "@ai_empty"

            if match_human:
                check_human = match_human.group(1)
            else:
                check_human = "@human_empty"

            new_file.write('{}\t{}\t{}\n'.format(filename, check_ai, check_human))

    return new_file


def count_correct(output_path):
    refine_xml(sys.argv[1], sys.argv[2])

    with open(os.path.join(output_path, "output2.txt"), 'w') as new_file:
        with open(os.path.join(output_path, "output.txt"), 'r') as input_file:
            lines = input_file.readlines()

            for line in lines:
                col = line.split('\t')
                camera_id = col[0].split('.')[0].split('_')[1]
                check_ai = col[1].replace(' ', '').strip()
                check_human = col[2].replace(' ', '').strip()
                correct = ''

                if check_ai == '@ai_empty':
                    correct = 'ai_empty'

                if check_ai == check_human:
                    correct = 'True'
                else:

                    if check_human == '@':
                        correct = '@'
                    elif check_human == '&#45432;&#45432;&#45432;' or check_human == "@human_empty":
                        correct = 'no'
                    else:
                        if not check_ai == '@ai_empty':
                            correct = 'False'

                new_file.write('{}\t{}\t{}\n'.format(camera_id, check_human, correct))

    return new_file


def make_check_ai_file(output_path):
    count_correct(sys.argv[2])

    with open(os.path.join(output_path, "result.txt"), 'w') as check_ai_file:
        check_ai_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format("camera_ID", "OK", "@", "nonono", "x",
                                                                      "ai_empty", "sum", "검지차량"))

    with open(os.path.join(output_path, "output2.txt"), 'r') as input_file:
        lines = input_file.readlines()

        camera_list = []
        for line in lines:
            col = line.split('\t')
            camera_id = col[0]
            if camera_id not in camera_list:
                camera_list.append(camera_id)

        for camera in camera_list:

            ok_num = 0
            at_num = 0
            no_num = 0
            x_num = 0
            ai_empty_num = 0
            detect_vehicle_num = 0

            check_human_list = []
            for line in lines:
                col2 = line.split('\t')
                camera_id2 = col2[0]
                check_human = col2[1]
                correct = col2[2].strip()

                if camera_id2 == camera:

                    if correct == 'True':
                        ok_num += 1
                    elif correct == 'False':
                        x_num += 1
                    elif correct == '@':
                        at_num += 1
                    elif correct == 'no':
                        no_num += 1
                    elif correct == 'ai_empty':
                        ai_empty_num += 1

                if camera_id2 == camera:

                    if check_human not in check_human_list:
                        check_human_list.append(check_human)
                        if correct == 'True' or correct == 'False':
                            detect_vehicle_num += 1

            sum_num = ok_num + at_num + no_num + ai_empty_num + x_num

            with open(os.path.join(output_path,"result.txt"), 'a+') as check_ai_file:
                check_ai_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(camera, ok_num, at_num, no_num, x_num,
                                                                              ai_empty_num, sum_num,
                                                                              detect_vehicle_num))


if __name__ == '__main__':
    make_check_ai_file(sys.argv[2])
