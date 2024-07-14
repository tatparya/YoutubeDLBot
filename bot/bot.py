#!/usr/bin/env python

import os
import youtube_dl
import pickle
import time

class MyLogger(object):
    def debug(self, msg):
        print("Debug:" + msg)

    def warning(self, msg):
        print("Warning:" + msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    # if d['status'] == 'downloading':
    #     print('Downloading video!')
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'wav',
#     }],
#     'logger': MyLogger(),
#     'progress_hooks': [my_hook],
# }
externalDrive = '/Users/tatparyashankar/Desktop/'
# externalDrive = '/Volumes/TatMusicLib/Other Lib/'
externalDriveYT = '/Volumes/TatMusicLib/Youtube Lib/'
externalDriveVJ = '/Volumes/TatMusicLib/VJ Loops/'

ydl_opts = {
    # 'verbose': True,
    'ffmpeg_location': '/usr/local/opt/ffmpeg@4/bin/ffmpeg',
    # 'format': format_string,
    'format': 'bestaudio/best',
    'outtmpl': externalDrive + '%(title)s.%(ext)s',
    # 'outtmpl': externalDriveYT + '%(title)s.%(ext)s',

    # 'download_archive': download_archive,
    # 'outtmpl': outtmpl,
    'default_search': 'ytsearch',
    # 'noplaylist': True,
    # 'no_color': False,
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        },
        {'key': 'FFmpegMetadata'}
    ],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

ydl_playlist_opts = {
    'verbose': True,
    'ffmpeg_location': '/usr/local/opt/ffmpeg@4/bin/ffmpeg',
    # 'format': format_string,
    'format': 'bestaudio/best',
    'outtmpl': externalDriveYT + '%(title)s.%(ext)s',
    # 'outtmpl': externalDriveYT + '%(title)s.%(ext)s',

    'download_archive': externalDriveYT + 'download_archive',
    # 'outtmpl': outtmpl,
    'default_search': 'ytsearch',
    # 'noplaylist': True,
    # 'no_color': False,
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        },
        {'key': 'FFmpegMetadata'}
    ],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

ydl_video_opts = {
    'verbose': True,
    'ffmpeg_location': '/usr/local/opt/ffmpeg@4/bin/ffmpeg',
    # 'format': format_string,
    'format': 'bestvideo/best',
    'outtmpl': externalDriveVJ + '%(title)s.%(ext)s',
    # 'outtmpl': externalDriveYT + '%(title)s.%(ext)s',

    'download_archive': externalDriveVJ + 'download_archive',
    # 'outtmpl': outtmpl,
    'default_search': 'ytsearch',
    # 'noplaylist': True,
    # 'no_color': False,
    'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        },
    ],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

'''
* Try downloading a given file
* After download finishes, move it to the right folder
* Also save successfully downloaded files to a pickle file to keep track of lib
* Save everything in one folder
* Symlink files into organized libraries??
'''

def downloadPlaylist(name, url):
    folder = externalDriveYT + '/' + name + '/'
    filepath = folder + '%(title)s.%(ext)s'
    archive = folder + 'download_archive'
    if not os.path.exists(folder):
        os.makedirs(folder)

    ydl_playlist_opts['outtmpl'] = filepath
    ydl_playlist_opts['download_archive'] = archive

    tryDownload = True
    tries = 0
    timeout = time.time() + 60 * 5

    while tryDownload and tries < 1000:
        tries += 1
        tryDownload = False

        try:
            with youtube_dl.YoutubeDL(ydl_playlist_opts) as ydl:
                ydl.extract_info(url)
        except Exception as e:
            tryDownload = True
            print(e)


def downloadSong(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)

def downloadVJLoops():
    with youtube_dl.YoutubeDL(ydl_video_opts) as ydl:
        ydl.extract_info("https://youtube.com/playlist?list=PLMEi2ySjhqKOjmUDQt8bI9o1KQf4uDfjR")

def downloadVisualVideos():
    with youtube_dl.YoutubeDL(ydl_video_opts) as ydl:
        ydl.extract_info("https://youtube.com/playlist?list=PLMEi2ySjhqKOjmUDQt8bI9o1KQf4uDfjR")

def downloadLibPlaylists():

    '''
    HOUSE PLAYLISTS
    '''

    # Lib deep house
    downloadPlaylist("House - Deep House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffacoq4fNZMiRjTL9LBNkbi")
    # Lib deep house
    downloadPlaylist("House - Deep House - Remix Mash",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffidENQ5FlZD-WwAFDWfh3t")
    # Lib deep house
    downloadPlaylist("House - Slap Bass",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcc9I1JruWR9NN5lzKBcfRi")

    # Lib House Tech house
    downloadPlaylist("House - Tech House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfft_s3L4yHTxr-C2C3lIsGw")
    # Lib House Tech house
    downloadPlaylist("House - Afro Latin Tech House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAff0mkh3q5CTIOc4pGJb8Y7G")
    # Lib House Tech house
    downloadPlaylist("House - Tech House - Remix Mash",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffnbf2B5fCaitsACFBrW3uC")

    # Lib House - Bass House
    downloadPlaylist("House - Bass House",
                     "https://www.youtube.com/playlist?list=PL52JIFTmqtiXLqPAwiJ-s9schx2x1deDR")
    # Lib House - Bass House
    downloadPlaylist("House - Bass House - Remix Mash",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffXAwUrRpj_ZA_bXDOtdO9J")

    # Lib House - Future House
    downloadPlaylist("Alnab - Future House",
                     "https://www.youtube.com/playlist?list=PL7kDOF7v0GUZlFJMKGZ9wMWmDKkP62dZz")

    # Lib House - Future House
    downloadPlaylist("Alnab - Bass House New",
                     "https://youtube.com/playlist?list=PL7kDOF7v0GUaMC9lIm-ch383jax8HpijQ")

    # Lib House - Future House
    downloadPlaylist("Alnab - Bass House 2",
                     "https://youtube.com/playlist?list=PL7kDOF7v0GUahv14W-2xGEns9Rl-1LlIB")

    # Lib House - Progressive House
    # downloadPlaylist("House - Progressive House",
    #                  "https://www.youtube.com/playlist?list=PL52JIFTmqtiVW6kN_JoyQH8717MalvKgP")
    # Lib Techno
    downloadPlaylist("House - Techno",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdWfM2gtkqPDfYc31mUeabZ")
    # Lib Techno
    downloadPlaylist("House - Mnimal Deep Techno",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeVV1xLUe09i6dHtdGlb3DL")
    # Lib Underground Techno
    downloadPlaylist("House - Underground Techno",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcZ_UWoGteM9egrWDL-varc")


    # Lib House - G House
    downloadPlaylist("House - G House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAff_ce5x58PK2N6SKLi13wHs")

    # Lib minimal
    downloadPlaylist("House - Minimal Progressive House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdAe5Td4lkNRsFN6GwhWTBe")
    # Lib minimal
    downloadPlaylist("House - Melodic House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfekdQwsKLejNB5gyJ8TbkSB")
    # Lib minimal
    downloadPlaylist("House - Melodic Techno",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfe5UrJNKv1KlaVboqShecWx")
    # Lib minimal
    downloadPlaylist("House - Melodic Techno - Minimal Groovy",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfenWe8aOAkQp-cu1KlvfQrf")
    # Lib minimal
    downloadPlaylist("House - Melodic Techno - Afters",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdRAnzFClWLsadzzyS5lNhV")

    # Lib Qilla
    downloadPlaylist("House - Qilla",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdqXkaiQ_6j2aFFdrjFH7ls")

    # Lib minimal tech afro
    downloadPlaylist("House - Minimal Tech Afro",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffN2lm99UIVMorJ9fP-tYEK")

    # Lib afro house
    downloadPlaylist("House - Afro House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdLexKYMfnoxrj8aFJhlh6n")
    # Lib afro house
    downloadPlaylist("House - Downtempo Tulum",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcI6LwXJmg-9IJYECe_ohI5")
    # Lib indo house
    downloadPlaylist("House - Indo Warehouse",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcpCJeoBIS9QCl3IVjnW_VG")
    # Lib indo house
    downloadPlaylist("House - Indo House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffMjq4U5IQilNxa_xnZjevs")
    # Lib indo bass
    downloadPlaylist("House - Indo Bass",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffmT54t9kBY_RJd3v7bfwns")
    # # Lib Organic
    downloadPlaylist("House - Organic House",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffn9jslU7R5NHc6CAAQwyz6")

    # Lib Bigroom / Rave
    # downloadPlaylist("House - Bigroom Mainstage",
    #                  "https://www.youtube.com/playlist?list=PL52JIFTmqtiV__i2IDhbdXXud6KPD32C4")

    # Lib House Pop
    # downloadPlaylist("House - House Pop",
    #                  "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcMEOf1bJR8AwE_CX8xYQ6O")

    '''
    FUTURE PLAYLISTS
    '''

    # Lib Bigroom / Rave
    # downloadPlaylist("House - Future Bass",
    #                  "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcMEOf1bJR8AwE_CX8xYQ6O")

    # Lib Pop
    downloadPlaylist("House - Fk Genz",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdtUqOKZezGHxDs5RZ2f035")


    # Lib Pop
    downloadPlaylist("House - Pop",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffUkP6j_7nd4j_5Mi2tVeWu")
    # Lib Pop
    downloadPlaylist("House - Future Bass",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfciCNsYQT9zScFRwtiu-w0t")
    # Lib Pop
    downloadPlaylist("House - Future Electronic",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcWeY1Aufmag1pU5smhSWBx")
    # Lib Pop
    downloadPlaylist("House - Acapella",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeQAVV0I0qdKWKxPQ5PoZWm")
    # Lib Pop
    downloadPlaylist("House - Samples",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAffWraIBhzAjAx3KpsB1GFUv")

    # OLDIES
    downloadPlaylist("Oldies",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcvi01KPGfPssN-VFzpEzQp")

    #
    # # Lib Bigroom / Rave
    # downloadPlaylist("House - Future Electronica",
    #                  "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcMEOf1bJR8AwE_CX8xYQ6O")

    '''
    HIP HOP PLAYLISTS
    '''

    # Lib Hip hop
    downloadPlaylist("Hip Hop",
                     "https://www.youtube.com/playlist?list"
                     "=PLjDKD6CQUAfdMn_rWnn_btnCSaQOSOrmi")
    # # Trap
    downloadPlaylist("Trap",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeUScKEFB8eTG4YWJm3wIia")
    # Lib DNB
    downloadPlaylist("Drum And Bass",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeyHKncoWH9cDRhZdfbIwBj")

    '''
    DESI PLAYLISTS
    '''

    # # Desi
    downloadPlaylist("To mix general",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfe5FN5Eh_S66Zme3d4nj51-")
    # # Desi
    downloadPlaylist("Techno Mix",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfesnw5qw2Eo0eLBLLTzkRLb")
    # # Desi
    downloadPlaylist("Indo To Mix",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfdjX0LCoOUSoq5AeDj75kIo")
    # # Desi
    downloadPlaylist("Desi",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeC9FJLMinhjBzgQwD3GSks")
    # # Desi
    downloadPlaylist("Desi Punjabi",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfcrLKulGXk6RaltttXTtWTv")
    # # Desi
    downloadPlaylist("Desi Party",
                     "https://www.youtube.com/playlist?list=PLjDKD6CQUAfckHY8MfTh4BGIFdoai-sJz")

    '''
    OTHER PLAYLISTS
    '''

    # # downloadPlaylist()
    # Lib Acapellas
    # downloadPlaylist("House - Fav Acapellas",
    #                  "https://www.youtube.com/playlist?list=PLjDKD6CQUAfeQAVV0I0qdKWKxPQ5PoZWm")
    # # Lib iconic
    # downloadPlaylist("House - Iconic",
    #                  "https://www.youtube.com/playlist?list=PL52JIFTmqtiVnDGGrANH8qi-loz7wkKjC")


    # # Lib bass house
    downloadPlaylist("House - Bass House - Arnav",
                     "https://music.youtube.com/playlist?list=PL7kDOF7v0GUYiYIwJC1Grt1Jh5xQiMZn5")
    # Mixing Vibey
    downloadPlaylist("Mixing Vibey",
                     "https://music.youtube.com/playlist?list=PL7kDOF7v0GUYflI1bDY1fTBrj2_0ITTp4")
    # Arushi
    downloadPlaylist("Arushi Indo Set",
                     "https://youtube.com/playlist?list=PLcD_O4UUlLX8vkWnGo47xRYLQIDLrCcIt&si=N6GWse3Io0WXKkLf")

if __name__ == '__main__':

    downloadLibPlaylists()
    # downloadVJLoops()
    # downloadSong("https://www.youtube.com/watch?v=yiMtAmH0_vU&ab_channel=6LACKVEVO")
    # downloadSong("https://www.youtube.com/watch?v=8nKZrsFIy3s&ab_channel=DropUnited")
    # downloadSong("https://www.youtube.com/watch?v=unfzfe8f9NI&ab_channel=AbbaVEVO")
    # downloadSong("https://www.youtube.com/watch?v=oNJZGYrEWhA&list=RDQM0prkTnexBJg&index=12&ab_channel=Acappella")

    # outtmpl = f"{file_path}.%(ext)s"

    # SCBot = SoundCloudBot()
    # tracks = SCBot.tracks
    # indexFile = externalDrive + 'lib_index.pickle'

    # downloadSong("https://open.spotify.com/playlist/7uduCezmhUPSvS4597Aqmu?si=09d2a162d1814dab")

    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     # infile = None
    #     # written_titles = set()
    #     # try:
    #     #     with open(indexFile, 'rb') as infile:
    #     #         written_titles = pickle.load(infile)
    #     # except (FileNotFoundError, EOFError, TypeError, ValueError) as e:
    #     #     print(e)
    #     #     written_titles = set()
    #     #
    #     # titles = list(map(lambda t: tracks[t]['user'] + ' ' +
    #     #                             tracks[t]['title'] + ' Radio Edit', tracks))
    #     # print(titles)
    #     # # titles = track['user'] + ' ' + track['title']
    #     ydl.extract_info("https://www.youtube.com/watch?v=ziDHaXj4IkE&ab_channel=Spinnin%27Records")
        # to_download = set()
        # for title in titles:
        #     if title in written_titles:
        #         continue
        #     else:
        #         to_download.add(title)
        #
        # for ind, title in enumerate(to_download):
        #     print("Downloading", ind + 1, "of", len(to_download))
        #     if title in written_titles:
        #         continue
        #
        #     try:
        #         ie_res = ydl.extract_info(title, False)
        #         if not(len(ie_res['entries']) > 0 and 'duration' in ie_res[
        #             'entries'][0] and ie_res['entries'][0]['duration'] < 500):
        #             continue
        #
        #         dl_res = ydl.extract_info(title)
        #         time.sleep(2)
        #
        #         written_titles.add(title)
        #     except Exception as e:
        #         print(e)

        # with open(indexFile, 'wb') as outfile:
        #     print(written_titles)
        #     pickle.dump(written_titles, outfile)

        # result = ydl.extract_info(
        #     # 'Swedish House Mafia - 19.30'
        # #         'https://open.spotify.com/track/5aOpzm8W8zysk4asB9hxJw?si=361183683c6f41aa',
        #         'https://soundcloud.com/officialswedishhousemafia/swedish-house-mafia-19-30',
        # #         download=False # We just want to extract the info
        #     )

        # print(result.keys())
        # if 'entries' in result:
        #     # Can be a playlist or a list of videos
        #     video = result['entries'][0]
        #     print(result['entries'])
        # else:
        #     # Just a video
        #     video = result
        #
        # if 'uploader' in result:
        #     print(result['uploader'])
        # if 'title' in result:
        #     print(result['title'])
