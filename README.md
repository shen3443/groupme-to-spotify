# groupme-to-spotify
Python script that parses through messages in a GroupMe group chat, finds links to Spotify tracks, and adds those tracks to a Spotify playlist.
Built using Groupy and Spotipy

# Inputs
When you run groupme_to_spotify.py you will be prompted to enter some information needed to access Groupme and Spotify, the following is a guide to help you navigate those requests.

It is highly recommended that you use copy+paste to make sure you accurately represent the information. I also recommend using a file like my_inputs.txt to save the inputs you frequently use.

## gm_token
Your GroupMe developer token. It can be aquired from https://dev.groupme.com/ 
Log in to your GroupMe account, then click **Access Token** in the top right corner of the window and copy+paste the token.
**DO NOT** Share your token. Anyone with the token will be able to access your Groupme account via the API.

## group_name
The name of your GroupMe group chat. Make sure the name you enter matches the groups name exactly.

## log_file
The name of the file you want to use to log the message ID of the last message thats been parsed. This allows you to run the file again without parsing old messages (which would cause songs that are already in the playlist to be added again). The file name must end in .txt

*Example*
log.txt

## sp_client_id
Your Spotify developer client ID. It can be aquired from https://developer.spotify.com/dashboard/
Log in to your Spotify account, then click **Create an App**. When you enter the app, your Client ID will be presented on the screen. Copy+paste the ID.

## sp_client_secret
Your Spotify developer client secret. Click on **Show Client Secret** underneath the client ID to access the code. Copy+paste the code.

## sp_redirect
Your Spotify App's Redirect URI
On your spotify app's page, click on **Edit Settings** and add a URI to **Redirect URIs**. Any valid URI (does not need to be accessible) works, but the URI you enter as input must match the URI in your App Settings

##sp_username
Your Spotify username. Find your name in the top right corner of your spotify, click on it, and then click on **Account** in the dropdown menu. This will take you to a page that includes your Spotify username.

## sp_user_id
Your Spotify user ID. Under the options to share your Spotify profile, click **Copy Spotify URI**. Paste this directly into the command prompt, or paste it into a text file to save it.

## sp_playlist_id
Your Spotify playlist's playlist ID. Under the options to share your Spotify playlist, click **Copy Spotify URI**. Paste this directly into the command prompt, or paste it into a text file to save it.

## playlist_name
The name of your Spotify playlist. Type it directly as it appears in your Spotify.


# To Do
- [ ] Finish README
- [ ] Create a requirements.txt for pip install
- [ ] Test with more groups/playlists
- [ ] Add functionality to log inputs with JSON to a .txt file, so they don't require repeated user input
