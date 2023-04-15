import requests
import time
from functools import reduce

headers = {
    "Accept": r"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": r"gzip, deflate, br",
    "Accept-Language": r"en-US,en;q=0.9",
    "Authorization": r"OAuth 2-292845-123684059-FSc1bAcM2LQopz",
    "Connection": r"keep-alive",
    "Host": r"api-v2.soundcloud.com",
    "Origin": r"https://soundcloud.com",
    "Referer": r"https://soundcloud.com/",
    "sec-ch-ua-mobile": r"?0",
    "sec-ch-ua-platform": r"macOS",
    "Sec-Fetch-Dest": r"empty",
    "Sec-Fetch-Mode": r"cors",
    "Sec-Fetch-Site": r"same-site",
    "User-Agent": r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  r"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
}

params = {
    "limit": "100"
}

class SCPlaylist:
    """SoundCloudPlaylist"""

    def __init__(self, title, id, trackIds):
        """Constructor for SoundCloudPlaylist"""
        self.title = title
        self.id = id
        self.trackIds = trackIds


class SoundCloudBot:
    """SoundCloudBot"""

    def __init__(self, ):
        """Constructor for SoundCloudBot"""
        self.playlists = {}
        self.tracks = {}
        self.trackIds = set()

        self.getUserPlaylists()
        self.getTracksData()

    def getUserData(self, ):
        r = requests.get('https://api-v2.soundcloud.com/me/library/all?limit'
                         '=100', headers=headers)

        print(r.status_code)
        res = r.json()
        print(res.keys())
        print(res['next_href'])

    def getUserPlaylists(self):

        r = requests.get("https://api-v2.soundcloud.com/users/123684059"
                         "/playlists_without_albums",
                         headers=headers,
                         params=params)

        print(r.status_code)
        if r.status_code != 200:
            print("Error getting user playlists:", r.status_code)
            return

        res = r.json()
        playlists = res['collection']
        # for playlist in playlists[:1]:
        playlists_data = []

        for playlist in playlists:
            # Get playlist meta
            playlistId = playlist['id']
            playlistTitle = playlist['title']
            if playlistTitle[:3] == "Lib":
                print(playlist['id'], playlist['title'])
                tracks = playlist['tracks']
                trackIds = set()
                # Get track Ids
                for track in tracks:
                    trackId = track['id']
                    trackIds.add(trackId)
                print(trackIds)
                scPlaylist = SCPlaylist(playlistId, playlistTitle, trackIds)
                self.trackIds.update(trackIds)
                self.playlists[playlistId] = scPlaylist

    def fetchTracksMeta(self, trackIds):
        print(len(trackIds))
        trackIdsParam = reduce(lambda a, b: str(a) + ',' + str(b), trackIds)
        print("Fetching tracks:", trackIdsParam)

        r = requests.get('https://api-v2.soundcloud.com/tracks?' +
                         'ids=' + trackIdsParam, headers=headers)

        if r.status_code != 200:
            print("Error getting tracks meta:", r.status_code)
            print(r.reason)
            print(r.request.url)
            return {}

        tracks = {}
        for trackData in r.json():
            user = trackData['user']['username']
            title = trackData['title']
            id = trackData['id']
            tracks[id] = {'user': user, 'title': title}

        # dict_keys(['artwork_url', 'caption', 'commentable', 'comment_count',
        # 'created_at', 'description', 'downloadable', 'download_count',
        # 'duration', 'full_duration', 'embeddable_by', 'genre',
        # 'has_downloads_left', 'id', 'kind', 'label_name', 'last_modified',
        # 'license', 'likes_count', 'permalink', 'permalink_url',
        # 'playback_count', 'public', 'publisher_metadata', 'purchase_title',
        # 'purchase_url', 'release_date', 'reposts_count', 'secret_token',
        # 'sharing', 'state', 'streamable', 'tag_list', 'title',
        # 'track_format', 'uri', 'urn', 'user_id', 'visuals', 'waveform_url',
        # 'display_date', 'media', 'station_urn', 'station_permalink',
        # 'track_authorization', 'monetization_model', 'policy', 'user'])

        return tracks

    def getTracksData(self):
        print("Getting tracks metadata")
        print(len(self.trackIds), " tracks in total.")
        trackIds = list(self.trackIds)
        print(trackIds)

        offset = 0
        while offset < len(trackIds):
            tracksBatch = trackIds[offset: offset + 50]
            tracksMeta = self.fetchTracksMeta(tracksBatch)
            self.tracks = {**self.tracks, **tracksMeta}

            offset += 50
            time.sleep(2)


if __name__ == '__main__':
    SCBot = SoundCloudBot()
    SCBot.getUserPlaylists()
    SCBot.getTracksData()

    print(SCBot.tracks)
