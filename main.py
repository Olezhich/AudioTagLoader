import audiotagloader


if __name__ == "__main__":
    try:
        audiotagloader.cli.cli_app()
    except KeyboardInterrupt:
        print("Program terminates")
