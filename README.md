# Webshare Terminal (WIP)
for now just a placeholder name

## What is this?
'Webshare Terminal' is CLI tool for searching webshare.cz focused mainly on videos. Inspired by streamcinema.
With this tool, you can easily search the contents of webshare and open them in VLC (again video related).

### Support for other files and other functions? (Zips, Docs, Downloading, etc.)
I will try to add more features including downloading files and working on a better interface.
More in TODO list

### Why use this and not streamcinema? 
Well, streamcinema has a manual database with movies, so some things aren't there immediately, but they can be on webshare.
Also in my opinion it feels quicker.


# Requirements

### VLC
You'll need the VLC folder in the path, because 'Webshare Terminal' uses VLC cmd commands.
If you don't know how to do so [here](https://www.vlchelp.com/add-vlc-command-prompt-windows/) is a step-by-step guide.

*I'm not using the VLC library because I find this more simple.*

### Libraries
all libraries will be in requirements.txt for now
- later there will be a setup function.


# Usage
Using 'Webshare Terminal' (just WT after)  is quite simple.

The first time you open WT you'll be asked for your webshare credentials.
After you, login username and your salted password hash will be stored in 'data.db', so you don't have to log in every time you open WT.

![Login preview](https://i.imgur.com/mdUsdnd.png)

After you logged in, you will see two search options:

![Search preview](https://i.imgur.com/Hw6t8cX.png)

Default Search is preconfigured with some parameters, except search query of course.
These parameters are:
- limit of results = 25
- category = video
- sort = largest

*NOTE You will be able to expand the search with the `more` command after your search*

Advanced Search can search anything on webshare, all categories, all sortings, and custom search limit.

If you select Advanced Search these are inputs you will be asked for:

- name = search query
- limit = number of returned results
- category = you can select from 7 categories (video, audio, images, archives, docs, software, adult)
- sort = you can select from 5 categories (largest, smallest, recent, relevance, rating)

Selecting any of these search options will bring a table with results.
![Result table for advanced search](https://i.imgur.com/7S8s5hH.png)

This part is quite self-explanatory, to select a specific movie just type the index number of it and it will instantly trigger VLC to open with that specific file.

If can't find what you have been looking for, you can try command `more` for more results, or just try other filters in Advanced Search.

# TODO
## Finished

- [x] Fix 'more' command (implementing offset)
- [x] Add more data to the table (rating, etc.)
- [x] Error handling

## In progress

- [ ] Add multi-account support
- [ ] Add download option
- [ ] Improve interface
- [ ] Add option for user to select custom colors
