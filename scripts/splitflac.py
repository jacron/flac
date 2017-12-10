from flac.lib.color import ColorPrint
from flac.services import get_full_cuesheet
import os, subprocess


"""
er van uitgaande dat een cuesheet een enkel muziekbestand adresseert dat het in stukken verdeelt
laten we in dit script ffmpeg zorgen dat de afzonderlijke stukken in flac files worden weggeschreven

dit is de enige methode om albums werkelijk op te delen in muziekstukken, bijv. concerten
omdat een cuesheet dat een paar delen bevat nooit perfect kan werken op een enkele muziekfile

(je houd 'resten' over omdat een cuesheet alleen begin- en geen eind-tijden aan kan geven)

november 2017 - jan h croonen
"""

cuepath = "/Volumes/Media/Audio/Klassiek/Collecties/BBC Legends/BBCL4015 - Gilels - Schumane, Scarlatti, Bach/Emil Gilels - Gilels (BBC legends).cue"
FFMPEG = 'ffmpeg'


def pad(t):
    if t < 10:
        return '0{}'.format(t)
    return t


def normtime(t):
    # duration
    # hh:mm:ss.ms
    ttt = t.split('.')
    ms = int(ttt[1])
    tt = ttt[0].split(':')
    mm = int(tt[1]) + 60 * int(tt[0])
    return '{}:{}:{}'.format(pad(mm), pad(tt[2]), ms)


def to_duration(time):
    # mm:ss:ff
    t = time.split(':')
    hh = int(t[0]) / 60
    mm = int(t[0]) % 60
    ss = t[1]
    ms = float(t[2]) / 75 * 1000
    return '{}:{}:{}.{}'.format(hh, mm, ss, int(ms))


def timedif(time2, time1):
    # mm:ss:ff
    # 75 frames per second
    t2 = time2.split(':')
    t1 = time1.split(':')
    ff = int(t2[2]) - int(t1[2])
    borrow = 0
    if ff < 0:
        borrow = 1
        ff += 75
    seconden = int(t2[1]) - int(t1[1]) - borrow
    borrow = 0
    if seconden < 0:
        borrow = 1
        seconden += 60
    minuten = int(t2[0]) - int(t1[0]) - borrow
    ms = float(ff) / 75 * 1000
    ms = int(ms) / 10
    return '{}:{}:{}'.format(pad(minuten), pad(seconden), pad(ms))


def split_file(flac, filepath):
    cmd = [FFMPEG, '-i', filepath,
           '-ss', to_duration(flac['time'])]
    if flac['duration']:
        cmd += ['-t', to_duration(flac['duration']),]
    cmd.append(flac['path'])
    ColorPrint.print_c(flac['path'], ColorPrint.CYAN)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # print 'STDOUT:{}'.format(out)
    # print 'ERR:{}'.format(err)


def get_flac(index, track, basedir, tracks, file_duration):
    outfile = os.path.join(basedir, track['title'] + '.flac')
    time = track['index']['time']
    if index < len(tracks) - 1:
        time2 = tracks[index + 1]['index']['time']
        duration = timedif(time2, time)
    else:
        if file_duration:
            duration = timedif(file_duration, time)
        else:
            duration = None
    return {
        'path': outfile,
        'time': time,
        'duration': duration,
    }


def get_duration(filepath):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', '-sexagesimal', filepath]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if len(out) == 0:
        return None
    return normtime(out)


def split_flac(cuepath):
    cuesheet = get_full_cuesheet(cuepath, 0)
    basedir = os.path.dirname(cuepath)
    for cfile in cuesheet['cue']['files']:
        # cfile = cuesheet['cue']['files'][0]
        filename = cfile['name']
        tracks = cfile['tracks']
        filepath = os.path.join(basedir, filename)
        file_duration = get_duration(filepath)
        if not file_duration:
            print('unknown duration for: ' + filepath)
            # return
        flacs = []
        for index, track in enumerate(tracks):
            flacs.append(get_flac(index, track, basedir, tracks, file_duration))
        for flac in flacs:
            split_file(flac, filepath)


def main():
    split_flac(cuepath)


if __name__ == '__main__':
    main()
