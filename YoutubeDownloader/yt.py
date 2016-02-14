#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import os
import sys
import subprocess
import re
from itertools import imap, ifilter
from collections import defaultdict


def get_rows(spreadsheet_name, skip_first_row=True):
    ret = None
    with open(spreadsheet_name, 'r') as fp:
        reader = csv.reader(fp)
        if skip_first_row:
            next(reader)
        ret = filter(lambda row: row[3].strip() != '', reader)
    if not ret:
        raise IOError('Can\'t read csv filename %s' % spreadsheet_name)
    return ret


# def get_best_video_audio_quality(video_url):
#     command = 'youtube-dl -F %s' % video_url
#     process = subprocess.Popen(command, stdout=subprocess.PIPE,
#                                stderr=subprocess.PIPE, shell=True)
#     output = process.communicate()
#     lines = ifilter(lambda line: re.match('^\d', line), output[0].split('\n'))

#     # remove dirty pieces like spaces, tabs and etc.
#     formatted = []
#     for line in lines:
#         l = filter(lambda x: x, line.split(' '))
#         formatted.append(l)

#     audio_opts = ifilter(lambda line: 'audio' in line, formatted)
#     video_opts = ifilter(lambda line: 'video' in line,
#                          ifilter(lambda x: 'mp4' in x, formatted))

#     # video
#     max_by_res = lambda opt: int(opt[2].split('x')[0])
#     max_quality_video = max(video_opts, key=max_by_res)

#     # audio
#     max_by_kbits = lambda opt: int(opt[6].split('k')[0])
#     max_quality_audio = max(audio_opts, key=max_by_kbits)

#     # return codes only
#     return max_quality_video[0], max_quality_audio[0]


# def download_video(video_url, video_code, audio_code):
#     command = 'youtube-dl -f bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]'
#     # command = 'youtube-dl -f %s+%s --merge-output-format mp4 %s' % (video_code,
#     #                                                                 audio_code,
#     #                                                                 video_url)
#     # process = subprocess.Popen(command, stdout=subprocess.PIPE,
#     #                            stderr=subprocess.PIPE, shell=True)
#     # output = process.communicate()

def download_video(video_url, output_path):
    command = 'youtube-dl -f bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm] -o "{0}.%(ext)s" {1}'.format(output_path, video_url)
    print '%s \t is processing.' % video_url
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    output = proc.communicate()
    is_err = 'ERROR' in output[-1]
    return not is_err                       # is success?


if __name__ == '__main__':
    # -f bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]
    INFILENAME, OUTFILENAME = 'in.csv', 'out.csv'
    PATTERN = 'https://www.youtube.com/watch?v={}'
    rows = get_rows(INFILENAME)

    d = defaultdict(int)
    # START, END = 900, 903                   # lady gaga is downloaded

    # for rownum, row in enumerate(rows[START:END]):
    for rownum, row in enumerate(rows):
        video_url = PATTERN.format(row[-1])
        date      = row[-2]
        dir_name  = row[0]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        output_path = './{0}/Videos/{1}'.format(dir_name, date)
        d[output_path] += 1
        if d[output_path] != 1:
            output_path += '_(%s)' % str(d[output_path])

        print '%s of %s' % (rownum+1, len(rows))
        success = download_video(video_url, output_path)
        if not success:
            print 'couldnt download %s' % video_url
        print '%s\tis successfully downloaded' % video_url
        print len(rows)
