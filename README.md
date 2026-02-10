# YT-DLP Easy Wrapper

A simple, Python-based wrapper for `yt-dlp` to download YouTube videos effortlessly with high quality, subtitles, and SponsorBlock integration.

## Features

- **Easy UI**: Simple interactive menu to choose quality and features.
- **4K/8K Support**: Downloads the highest resolution available using MKV container.
- **Auto-Config**: Comes with `ffmpeg` configuration for best performance.
- **Advanced Features**:
  - **SponsorBlock**: Automatically removes sponsors, intros, and self-promotions.
  - **Subtitles**: Auto-downloads English and Vietnamese subtitles.
  - **Metadata**: Embeds thumbnails and track info directly into the file.
- **Smart Formatting**: Auto-merges video and audio streams.

## Installation & Usage

1. **Prerequisites**:
   - Ensure you have Python installed.
   - The script will look for `yt-dlp.exe` in the current folder (already included/downloaded).

2. **Run the Tool**:
   - Double-click **`run.bat`**.
   - Paste your YouTube link.
   - Follow the on-screen prompts.

## Configuration

Modify `config.json` to change default behaviors:

- **`settings.download_dir`**: Change where files are saved.
- **`resolutions`**: Add or modify quality presets.
- **`features`**: Add more `yt-dlp` flags as toggleable options.

## Disclaimer

This tool is for educational and personal use only. Please respect copyright laws and YouTube's Terms of Service.
