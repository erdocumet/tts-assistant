from assistant import Assistant, ping


def main():
    # Init protocol
    wakewords = ["caroline", "carolyn", "karen", "computer"]
    a = Assistant(wakewords)
    ping()

    # Conversation loop; listens for wakeword, if wakeword present in text, parses for command and returns spoken
    # output (or executes program). To be improved.
    while True:
        alert, command = a.listen_for_wakeword()
        if alert:
            print(f"Command: {command}")
            a.process_command(command)

if __name__ == '__main__':
    main()
