# BetterCinema
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Seraphim-Solutions/bettercinema?style=for-the-badge)](https://github.com/Seraphim-Solutions/bettercinema/releases)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Seraphim-Solutions/bettercinema?style=for-the-badge)](https://github.com/Seraphim-Solutions/bettercinema) 
[![GitHub repo file count](https://img.shields.io/github/directory-file-count/Seraphim-Solutions/bettercinema?style=for-the-badge)](https://github.com/Seraphim-Solutions/bettercinema) 
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/Seraphim-Solutions/bettercinema?style=for-the-badge)](https://codeclimate.com/github/Seraphim-Solutions/bettercinema/) 
[![Code Climate issues](https://img.shields.io/codeclimate/issues/Seraphim-Solutions/bettercinema?style=for-the-badge)](https://codeclimate.com/github/Seraphim-Solutions/bettercinema/)
## What is this?

‘BetterCinema’ is a CLI tool for searching webshare.cz focused mainly on videos. Inspired by [Stream Cinema Community](https://gitlab.com/stream-cinema-community).

With this tool, you can easily search the contents of webshare and open them in VLC (again video related).

![better-cinema](https://user-images.githubusercontent.com/34968650/185767066-e4d6ed7f-7795-4492-b643-62ae47e861ad.gif)

### Why use this and not stream cinema? 

Well, stream cinema has a manual database with movies, so some things aren’t there immediately, but they can be on webshare.

Also, it feels quicker.

## Installation
Download release for your operation system of choice [here](https://github.com/Seraphim-Solutions/bettercinema/releases)

### Build instructions
```BASH
git clone https://github.com/Seraphim-Solutions/bettercinema.git
cd bettercinema
python3 -m pip install -r requirements.txt
python3 app.py
```
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

After you logged in, you will see few options:
- Default Search 
- Advanced Search
- Open Link
- Trakt.tv
- Settings

![Search preview](https://i.imgur.com/YhCveaD.png)

Default Search is pre-configured with some parameters, except search query of course.

These parameters are:

- limit of results = 25

- category = video

- sort = relevance (Webshare uses empty string for Relevace)

*NOTE You will expand the search with the `more` command after your search*

Advanced Search can search anything on webshare, all categories, all sortings, and custom search limit.

If you select Advanced Search these are inputs, the tool will ask you for:

- name = search query

- limit = number of returned results

- category = you can select from 7 categories (video, audio, images, archives, docs, software, adult)

- sort = you can select from 5 categories (largest, smallest, recent, relevance, rating)

Selecting any of these search options will bring a table with results.

![Result table for advanced search](https://i.imgur.com/6JqRGZx.png)

*`Name` color is selected by upvotes(green) / downvotes(red), white color is for neutral votes 50/50*

This part is quite self-explanatory, to select a specific movie just type the index number of it and it will instantly trigger VLC to open with that specific file.

For more options when browsing the result table, type `help`. 

## Have any suggestions? Use [Discussion](https://github.com/Seraphim-Solutions/bettercinema/discussions/categories/ideas) or contact me on Discord Danni#1965
