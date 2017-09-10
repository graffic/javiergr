title: Downloading steam games via cli
date: 2017-09-10
category: technical
published: true
summary: When my internet line is not enough to download a 60GiB game.

With almost no bandwidth at home, I needed a way to download `DOOM` that didn't involve blocking the home internet line for two days. Besides finding a friend with a good internet line, I also found that using [steamcmd](https://developer.valvesoftware.com/wiki/SteamCMD) you can use any computer to download steam games. No need to bring your gaming rig to your friend house to download the game, they can download it for you or you can use a laptop without steam.


## Downloading the game

1. Install `steamcmd` following the [official instructions](https://developer.valvesoftware.com/wiki/SteamCMD#Downloading_SteamCMD).
2. Open it and log-in with your username and password: `login username password`
3. Set the operating system and  bitness (32/64 bits) for the game. For example, I downloaded `DOOM` from a mac for a `64bit Windows`
  * `@sSteamCmdForcePlatformType windows`
  * `@sSteamCmdForcePlatformBitness 64`
4. Choose a folder name: `force_install_dir ./DOOM`
5. Go to https://steamdb.info/ and find the `APPID` of the game you want to download.
6. Start the download: `app_update 379720 validate`

This will generate a folder called `DOOM` with the game inside and one extra folder: `steamapps` where an `appmanifest_xxx.vcf` file will be created. We will use that file later to add the game to the steam library.

## Installing the game back at your gaming station

1. Close steam.
2. Find your steam folder.
3. Copy the game where the other games are. Usually the `steamapps\common` folder. Leave the name of the folder unchanged
4. From the game, you've just copied, move the appmanifest file to the `steamapps` folder (Where other manifest files are).
5. Open steam and you should see your game as installed in your library.
6. You can verify that your game is ok following [these instructions](https://support.steampowered.com/kb_article.php?ref=2037-QEUH-3335).