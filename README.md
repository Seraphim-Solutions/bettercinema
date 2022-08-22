# Bettercinema
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Seraphim-Solutions/bettercinema?style=for-the-badge) ![GitHub repo file count](https://img.shields.io/github/directory-file-count/Seraphim-Solutions/bettercinema?style=for-the-badge)
## What is this?

‘BetterCinema’ is a CLI tool for searching webshare.cz focused mainly on videos. Inspired by [Stream Cinema Community](https://gitlab.com/stream-cinema-community).

With this tool, you can easily search the contents of webshare and open them in VLC (again video related).

![better-cinema](https://user-images.githubusercontent.com/34968650/185767066-e4d6ed7f-7795-4492-b643-62ae47e861ad.gif)

### Why use this and not stream cinema? 

Well, stream cinema has a manual database with movies, so some things aren’t there immediately, but they can be on webshare.

Also, it feels quicker.

# Requirements

### VLC

You’ll need the VLC media player installed. And it has to be in its default directory(Program Files/VideoLAN/VLC/). (for now)

*I’m not using the VLC library because I find this more simple.*

### Libraries

All libraries will be in requirements.txt for now

- later there will be a setup function.

# Usage

Using ‘BetterCinema’ (or just BC in short) is quite simple.

The first time you open BC you’ll be asked for your webshare credentials.

After you login, username and your salted password hash will be stored in ‘data.db’, so you don’t have to log in every time you open BC.

![Login preview](https://i.imgur.com/mdUsdnd.png)

After you logged in, you will see two search options:

![Search preview](https://i.imgur.com/Hw6t8cX.png)

Default Search is pre-configured with some parameters, except search query of course.

These parameters are:

- limit of results = 25

- category = video

- sort = largest

*NOTE You will expand the search with the `more` command after your search*

Advanced Search can search anything on webshare, all categories, all sortings, and custom search limit.

If you select Advanced Search these are inputs, the tool will ask you for:

- name = search query

- limit = number of returned results

- category = you can select from 7 categories (video, audio, images, archives, docs, software, adult)

- sort = you can select from 5 categories (largest, smallest, recent, relevance, rating)

Selecting any of these search options will bring a table with results.

![Result table for advanced search](https://i.imgur.com/VyB7uWP.png)

*`Name` color is selected by upvotes(green) / downvotes(red), white color is for neutral votes 50/50*

This part is quite self-explanatory, to select a specific movie just type the index number of it and it will instantly trigger VLC to open with that specific file.

If can’t find what you have been looking for, you can try command `more` for more results, or just try other filters in Advanced Search.

# TODO

## Finished

- [x] Fix ‘more’ command (implementing offset)

- [x] Add more data to the table (rating, etc.)

- [x] Add download option

- [x] Error handling

- [x] Add option for user to customize colors

- [x] Add multi-account support

- [x] Play direct link option  

- [x] Recoded md5crypt

## In progress

- [ ] Improve interface (long term goal)

- [ ] Implement Trakt.tv
  - [ ] Trendings
  - [ ] Serials (Series / Episodes)
  - [ ] Watchlist
  - [ ] Watched and Watching tracking

- [ ] Option to download subtitles

# Bug Fixes

- [x] Fixed crashing when a file was private / password protected

- [x] Fixed VLC not opening on windows


## Have any suggestions? Use [Discussion](https://github.com/Seraphim-Solutions/bettercinema/discussions/categories/ideas) or contact me on Discord Danni#1965
