from datetime import datetime
from gmusicapi import Mobileclient

class PlaylistGenerator:

    def __init__(self, device_id, min_track_date, is_dry_run=False, do_logging=True):
        self.min_track_date = min_track_date
        self.is_dry_run = is_dry_run
        self.do_logging = do_logging
        
        self.api = Mobileclient()
        self.api.oauth_login(device_id)      

        self.playlist_tracks = []
        self.playlist_track_count = 0
        self.playlist_count = 0
        self.total_track_count = 0

        
    def generate_playlists(self, playlist_prefix, playlist_suffix, max_tracks_per_playlist, since):

        self.library = self.api.get_all_songs(incremental=True,
                                              include_deleted=None)
               
        for partial_tracklist in self.library:
            for track in partial_tracklist:
                self._add_track(track)
                if(self.playlist_track_count == max_tracks_per_playlist):
                    self._finish_current_playlist(playlist_prefix, playlist_suffix)
            
        if (self.playlist_track_count > 0):
            self._log('Have some tracks left over; making smaller playlist\n')
            self._finish_current_playlist(playlist_prefix, playlist_suffix)

        self._log('Done; created '
                  + str(self.playlist_count)
                  + ' lists with '
                  + str(self.total_track_count)
                  + ' tracks total\n')


    def _finish_current_playlist(self, prefix, suffix):
        name = (prefix + '_' + str(self.total_track_count - self.playlist_track_count) 
                + '_' + str(self.total_track_count - 1) + suffix)
        
        self._log('Done with playlist ' + name + '\n')

        if not self.is_dry_run:

            self._log('Uploading playlist ' + name + ' with '
                      + str(len(self.playlist_tracks)) + ' tracks\n')
            
            playlist_id = self.api.create_playlist(name)
            results = self.api.add_songs_to_playlist(
                playlist_id, self.playlist_tracks)
            
            self._log('Upload has ' + str(len(results))
                      + ' playlist entries; first one is:'
                      + results[0])

        self.playlist_tracks.clear()
        self.playlist_count += 1
        self.playlist_track_count = 0
        

    def _add_track(self, track):
        track_date = track['creationTimestamp']
        track_date = datetime.utcfromtimestamp(int(track_date) / 1000000)
        if track_date > self.min_track_date:
            #self._log('track is new; adding it');                 
            self.playlist_tracks.append(track['id'])
            self.total_track_count += 1
            self.playlist_track_count += 1

    def _log(self, text):
        if(self.do_logging):
            print(text)

            
if __name__ == '__main__':

    from configparser import RawConfigParser
    config = RawConfigParser()
    config.read('settings.ini')
    section = 'google_playlist_generator'

    device_id = config.get(section, 'device_id')

    last_sync_time = config.get(section, 'last_sync_time')
    update_last_sync_time = config.getboolean(section, 'update_last_sync_time')
    
    if last_sync_time.strip() != '':
        last_sync_time = datetime.strptime(last_sync_time, '%Y-%m-%d %H:%M:%S.%f')
    else:
        last_sync_time = datetime.utcfromtimestamp(0)

    
    is_dry_run = config.getboolean(section, 'is_dry_run')
    do_logging = config.getboolean(section, 'do_logging')

    pg = PlaylistGenerator(device_id, last_sync_time, is_dry_run, do_logging)

    now = datetime.now()
    playlist_prefix = now.strftime(config.get(section, 'playlist_prefix'))
    playlist_suffix = now.strftime(config.get(section, 'playlist_suffix'))
    tracks_per_playlist = config.getint(section, 'tracks_per_playlist')

    pg.generate_playlists(playlist_prefix, playlist_suffix, tracks_per_playlist, last_sync_time)

    if update_last_sync_time:
        if do_logging:
            print('Updating last_sync_time to %s' % now)
            
        config.set(section, 'last_sync_time', now)
        
        if not is_dry_run:
            with open('settings.ini', 'w') as configfile:
                config.write(configfile) #goodbye comments :(
