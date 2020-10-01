'''
Author: Chris Isacs

https://github.com/shen3443/groupme-to-spotify

Last Update: 10/1/2020 : Created class for recieving user input, added save functionality for the input
'''

from groupy.client import Client
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class GroupmeSpotifyPlaylistUpdate:
    '''
    Parses through Groupme Groupchat messages and finds links to Spotify
    songs, then adds those songs to a Spotify playlist
    '''
    def __init__(self, input_dict):
        #Assign paramaters to class attributes
        self.__dict__.update(input_dict)
        self.sp_scope = "playlist-modify-public"

        #Groupme Client
        gp_client = Client.from_token(self.gm_token)

        #Groupme Groupchat
        groupchat = self.find_groupchat(gp_client)

        #Song URLs From Messages
        song_urls = self.get_tracks_from_groupchat(groupchat, self.find_last_checked_message(self.log_file))

        #If there are new songs in the groupchat:
        if song_urls:

            #Login to Spotify
            sp_cred = SpotifyOAuth(client_id=self.sp_client_id, client_secret=self.sp_client_secret, redirect_uri=self.sp_redirect, username=self.sp_username, scope=self.sp_scope)
            self.sp = spotipy.Spotify(client_credentials_manager=sp_cred)

            #Add songs to Spotify playlist
            self.add_songs_to_playlist(song_urls)

    
    def find_groupchat(self, gp_client):
        '''
        Finds the correct groupchat by name and returns a groupy
        group object. Will raise an exception if the group cannot
        be found
        '''
        print("Finding %s Group in GroupMe..." % (self.group_name))

        found = False

        #Iterate through groups the user is a meber of
        for group in gp_client.groups.list_all(omit='memberships'):

            #Find the right group by name
            if group.name == self.group_name:

                #Save that group
                groupchat = group
                found = True
        
        #Raise an exception if there is no group with that name
        if not found:
            raise Exception('Group name not recognized')

        print("Done")

        #Return the group
        return groupchat
    
    def find_last_checked_message(self, log_file):
        '''
        Checks the log file to find the last message that has already
        been checked (the last time the script was run) and returns
        the message ID

        If this is the first time running the script & no log file exists,
        returns False

        If the file is not found because input was incorrect, user is prompted
        to try again with new input
        '''
        print("Finding new messages...")

        #Try opening the file and reading it
        try:
            with open(log_file, 'r') as log:
                last_checked_message = log.read()

            print("Last checked message ID: ", last_checked_message)

        #If the file doesn't exist (ie. first time running the program, or filename miss-entered) exeption will be triggered
        except FileNotFoundError:
            print("Log file not found...")
            log_file = input("Re-enter log file name, or press enter to parse all messages in group")

            #If user passes input, recursively call method with new input
            if log_file:
                return self.find_last_checked_message(log_file)

            #If no input is passed, return False to use all messages
            return False
        
        #Return the ID of the last checked message
        return last_checked_message
    
    def update_log(self, message_id):
        '''
        Overwrites the log file with the message ID of the most
        recent message the script has parsed
        '''
        print("Updating log...")

        #Open the log file in overwrite and write the new message ID
        with open(self.log_file, 'w') as log:
            log.write(message_id)
        
        print("Done")

    def clean_url(self, text):
        '''
        Takes a string that may contain a url link and returns the
        link if it exists.
        '''
        #Iterate through the characters in the text
        for i in range(len(text)):
            #Find the beginning of the https link
            if text[i:i+5] == "https":
                #Trim excess characters from the front
                url = text[i:]
                #Split the text by ' ', trimming anything added after the link
                url_tokens = url.split()
                #Return the URL
                return url_tokens[0]

    def get_tracks_from_groupchat(self, groupchat, last_checked_message):
        '''
        Parses through messages in the group chat to find URLs for
        spotify songs

        Returns a list of song URLs
        '''
        #Create a list to store song URLs
        song_urls = []

        #If a last checked message was identified
        if last_checked_message:
            for message in groupchat.messages.list_after(last_checked_message).autopage():
                #Store the ID of the most recently checked message
                last_message_id = message.id
                if message.text:
                    if 'https://open.spotify.com/track/' in message.text:
                        #Isolate the spotify link
                        track_url = self.clean_url(message.text)
                        song_urls.append(track_url)

        #If no last checked message was identified
        else:
            for message in groupchat.messages.list_all().autopage():
                #Store the ID of the most recently checked message
                last_message_id = message.id
                if message.text:
                    if 'https://open.spotify.com/track/' in message.text:
                        #Isolate the Spotify link
                        track_url = self.clean_url(message.text)
                        song_urls.append(track_url)

        print("Found %d new songs to add to %s" % (len(song_urls), self.playlist_name))

        #Update the log file with the ID of the most recent message in the group that has been checked
        self.update_log(last_message_id)

        return song_urls

    def add_songs_to_playlist(self, song_urls):
        '''
        Takes a list of spotify song URLs and adds them to a
        spotify playlist 
        '''
        print("Adding %d new songs to %s..." % (len(song_urls), self.group_name))

        #Spotify API only accepts 100 songs at a time
        while song_urls:
            temp = song_urls[0:100]
            song_urls = song_urls[100:]
            self.sp.user_playlist_add_tracks(self.sp_user_id, self.sp_playlist_id, temp)
        
        print("Done")

class DataFromUser:
    def __init__(self, required_inputs):
        self.required_inputs = required_inputs
    
    def get_user_data(self):
        '''
        Asks user if they would like to use stored data. Either opens file and returns
        the data, returns a call of get_inputs() to get new data, or returns itself
        if the user input is invalid
        '''
        #Explain to the user what they are being asked
        print("If this is not your first time running this program, you may have a save file with all of the required data...")
        print("If this is your first time, answer 'n' to the following question...")
        answer = input("Would you like to use stored data on login, group and playlist info? (y/n): ")

        if answer == 'y':
            #Get the file name
            data_file = input("Enter the name of the .txt file you would like to use: ")
            try:
                #Open the file, load and return the data
                with open(data_file, 'r') as fp:
                    return json.loads(fp.read())
            #If the file doesn't exist, call get_user_data() again for new input
            except FileNotFoundError:
                print("File not found...")
                return self.get_user_data()

        elif answer == 'n':
            #Get and return new user inputs
            return self.get_inputs()

        else:
            #Invalid inputs trigger a recursive call on the function for new input
            print("Answer not recognized, please answer (y/n)")
            return self.get_user_data()

    def get_inputs(self):
        '''
        Takes a list of required information from user, gets user input for
        each item in the list, then returns a dict where items from the list
        are keys and the corresponding user inputs are values
        '''
        #Get inputs, store to dict
        data = {i: input('Enter %s: ' % i) for i in self.required_inputs}

        #Give user option to save the data
        self.give_save_option(data)

        #Return the data
        return data

    def give_save_option(self, data):
        '''
        Gives the user the option to save the data for future use. Lets user input a filename,
        then writes the dictionary to that file (using json.dumps()). 

        Returns the files name if a file is written, False if not
        Recursively returns a call on itself if input is invalid
        '''

        yn = input("Would you like to save inputs for future use? (y/n): ")

        if yn == 'y':
            valid = False
            #While loop repeats until a valid file name is given
            while not valid:
                print("WARNING: program will overwrite an existing file if you give a file name already in use in this folder")
                filename = input("What would you like to name the save file (must end in .txt): ")

                #Check that file name is valid
                if filename[-4:] == '.txt':
                    print("Saving to %s..." % (filename))

                    #Write data to file
                    with open(filename, 'w') as fp:
                        fp.write(json.dumps(data))

                    #Break out of while loop
                    print("Done")
                    valid = True

                else:
                    #Inform user filename was invalid and cycle back through while loop
                    print("File name must end in .txt")
                    print("Trying again...")

            #Return the file name
            return filename

        elif yn == 'n':
            #User does not want to save, return False
            return False

        else:
            #Input is invalid, return recursive call to let user try again
            print("Answer not recognized, please answer (y/n)")
            return self.give_save_option(data)

def main():
    required_inputs = [
        'gm_token',
        'group_name',
        'log_file',
        'sp_client_id',
        'sp_client_secret',
        'sp_redirect',
        'sp_username',
        'sp_user_id',
        'sp_playlist_id',
        'playlist_name'
    ]
    print('***Please see README file for explanation of required inputs & instructions on how to find them***')
    print('https://github.com/shen3443/groupme-to-spotify/blob/master/README.md')
    GroupmeSpotifyPlaylistUpdate(DataFromUser(required_inputs).get_user_data())

if __name__ == "__main__":
    main()
