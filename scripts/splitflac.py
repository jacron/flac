import glob

from flac.lib.color import ColorPrint
from flac.services import get_full_cuesheet
import os
import subprocess


"""
er van uitgaande dat een cuesheet een enkel muziekbestand adresseert dat het in 
stukken verdeelt laten we in dit script ffmpeg zorgen dat de afzonderlijke 
stukken in flac files worden weggeschreven

dit is de enige methode om albums werkelijk op te delen in muziekstukken, 
bijv. concerten omdat een cuesheet dat een paar delen bevat nooit perfect kan 
werken op een enkele muziekfile

(je houd 'resten' over omdat een cuesheet alleen begin- en geen eind-tijden 
aan kan geven)

om verdere verwerking (combineren tot cuesheets) makkelijker te maken worden
de bestanden genummerd; soms zijn er meerdere cuesheets die gebruikt worden
voor splitsing en ook dat wordt verdisconteerd

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
    try:
        hh = int(t[0]) / 60
        mm = int(t[0]) % 60
        ss = t[1]
        ms = float(t[2]) / 75 * 1000
    except:
        return None
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
    duration = to_duration(flac['time'])
    if not duration:
        return
    cmd = [FFMPEG, '-i', filepath,
           '-ss', duration]
    if flac['duration']:
        duration = to_duration(flac['duration'])
        if duration:
            cmd += ['-t', duration,]
        else:
            print 'found no duration for ', flac['path']
    cmd.append(flac['path'])
    ColorPrint.print_c(flac['path'], ColorPrint.CYAN)
    # try:
    # print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    # except TypeError as type_err:
    #     print type_err
    # print 'STDOUT:{}'.format(out)
    # print 'ERR:{}'.format(err)


def get_flac(strnr, index, track, basedir, tracks, file_duration):
    track_title = track['title'].replace('/', '_')
    filename = u'{} {}.flac'.format(strnr, track_title)
    outfile = os.path.join(basedir, filename)
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


def filename(filepath):
    name = filepath.split('/')[-1]
    return name  # .replace("_", " ")


def tidy_nr(nr):
    strnr = str(nr)
    if nr < 10:
        strnr = '0' + strnr
    if nr < 100:
        strnr = '0' + strnr
    return strnr


def get_max_nr(basedir):
    nr = 0
    files_path = u"{}{}".format(basedir, "/*.flac")
    for f in glob.iglob(files_path):
        fname = filename(f)
        w = fname.split(' ')[0]
        try:
            i = int(w)
            # make nr the max
            if i > nr:
                nr = i
        except ValueError:
            pass
    return nr


def incr_nr(nr):
    # maak een kleine sprong van tien, om de afzonderlijke bron cuesheets te
    # onderscheiden - tenzij we helemaal aan het begin staan
    if nr == 0:
        nr += 1
    else:
        nr += 10
    return nr


def split_flac(cuepath):
    """
    Splits een groot flac of ape bestand aan de hand van een cuesheet
    (het cuesheet heeft een verwijzing naar het te splitsen bestand in een
    relatief pad).
    Om de volgorde te bewaren begint elk doelbestand met een nummer.
    Het nummer krijgt tot twee voorloopnullen zodat we tot bijna duizend
    bestanden in volgorde kunnen houden (sorteerbaar alfabetisch).
    Meerdere splitsacties na elkaar zijn mogelijk, het rangnummer
    wordt na een sprongetje van tien voortgezet.
    Aangenomen wordt dat normale flac bestanden niet met een nummer beginnen.
    :param cuepath:
    :return:
    """
    cuesheet = get_full_cuesheet(cuepath, 0)
    basedir = os.path.dirname(cuepath)
    nr = get_max_nr(basedir)
    nr = incr_nr(nr)

    for cfile in cuesheet['cue']['files']:
        filepath = os.path.join(basedir, cfile['name'])
        file_duration = get_duration(filepath)
        if not file_duration:
            print('unknown duration for: ' + filepath)
        flacs = []
        tracks = cfile['tracks']
        for index, track in enumerate(tracks):
            strnr = tidy_nr(nr)
            flacs.append(get_flac(strnr, index, track, basedir, tracks, file_duration))
            nr += 1
        for flac in flacs:
            split_file(flac, filepath)


def main():
    split_flac(cuepath)


if __name__ == '__main__':
    main()
