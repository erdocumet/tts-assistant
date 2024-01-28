from assistant import Assistant, ping


def main():
    # Init protocol
    wakewords = ["caroline", "carolyn", "karen", "computer"]
    assistant = Assistant(wakewords)

    ping()
    assistant.speak(f"Carolyn online.")

    # Conversation loop; listens for wakeword, if wakeword present in text, parses for command and returns spoken
    # output (or executes program).
    while not assistant.shutdown:
        alert, command = assistant.listen_for_wakeword()
        if alert:
            assistant.speak(command)
        # TODO: Create skill object, figure out logics involved (importing list of skills and associated keywords,
        #  executing skills, etc.) Note: Perhaps we format the skills and keywords as a dict where the keys are a
        #  list of keywords and the values are the skill objects.

        # TODO: Create some basic skills:
        #   - Wikipedia
        #   - Time and date
        #   - Alarm
        #   - DJ
        #   - Therapy mode


if __name__ == '__main__':
    main()
