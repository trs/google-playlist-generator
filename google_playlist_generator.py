from datetime import datetime
from gmusicapi import Mobileclient
from configparser import RawConfigParser

MAX_PLAYLIST_SIZE = 1000
SETTINGS_FILE = 'settings.ini'
SECTION = 'google_playlist_generator'

config = RawConfigParser()
config.read(SETTINGS_FILE)

device_id = config.get(SECTION, 'device_id')
playlist_name = config.get(SECTION, 'playlist_name')

def get_api():
	global device_id
	api = Mobileclient()

	if device_id.strip() == '':
		creds = api.perform_oauth(None, True)
		api.oauth_login(Mobileclient.FROM_MAC_ADDRESS, creds)

		devices = api.get_registered_devices()
		device_id = devices[0]["id"]
		
		config.set(SECTION, 'device_id', device_id)
	else:
		api.oauth_login(device_id)

	return api

def purge_existing_playlists(api):
	global playlist_name
	all_playlists = api.get_all_user_playlist_contents()
	generated_playlists = list(filter(lambda p: p['name'].startswith(playlist_name), all_playlists))

	for playlist in generated_playlists:
		for track in playlist['tracks']:
			api.remove_entries_from_playlist(track['id'])

	return list(map(lambda p: p['id'], generated_playlists))

def get_all_song_chunks(api):
	song_chunk = []
	for song in api.get_all_songs():
		song_chunk.append(song['id'])
		if len(song_chunk) == MAX_PLAYLIST_SIZE:
			yield song_chunk
			song_chunk = []

	if len(song_chunk) > 0:
		yield song_chunk
		song_chunk = []

def get_playlist_name(playlist_num):
	global playlist_name
	return playlist_name + ' (' + str(playlist_num) + ')'

def get_available_playlist(api, playlist_num, available_playlists):
	name = get_playlist_name(playlist_num)

	if len(available_playlists) > 0:
		playlist_id = available_playlists.pop(0)
		api.edit_playlist(playlist_id, new_name=name)
		return playlist_id
	else:
		return api.create_playlist(name)

if __name__ == '__main__':
	api = get_api()

	available_playlists = purge_existing_playlists(api)
	playlist_num = 1

	for song_chunk in get_all_song_chunks(api):
		playlist_id = get_available_playlist(api, playlist_num, available_playlists)
		
		api.add_songs_to_playlist(playlist_id, song_chunk)

		playlist_num += 1

	if len(available_playlists) > 0:
		for remaining_playlist in available_playlists:
			api.delete_playlist(remaining_playlist)

	with open(SETTINGS_FILE, 'w') as configfile:
		config.write(configfile)