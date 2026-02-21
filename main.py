import audiotagloader

if __name__ == "__main__":
    app = audiotagloader.App()

    app.get_track_tags_by_artist("Rainbow")
