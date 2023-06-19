# Discord Spin Bot

This is a Discord bot that allows users to spin a virtual wheel and win prizes. The bot keeps track of the number of spins a user has made and awards prizes based on the outcome of each spin.

## Features

- Spin the wheel: Users can use the `!spin` command to spin the virtual wheel and have a chance to win prizes.
- Prize system: The bot randomly selects prizes from a predefined list based on their probabilities.
- Prize claiming: Users can claim their prizes by sending a direct message (DM) to the bot admin.
- User stats: Users can check their spin statistics, including the number of spins, last spin time, reset count, and prizes won, using the `!stats` command.

## Prerequisites

Before running the Discord Spin Bot, ensure that you have the following prerequisites:

- Python 3.7 or higher
- `discord.py` library (install using `pip install discord.py`)
- SQLite database

## Installation

1. Clone the repository or download the script file.

2. Install the necessary dependencies using the following command:

pip install discord.py

3. Create an SQLite database named `mydb.db` in the same directory as the script.

4. Replace the placeholders in the script with your specific configuration:
- Replace the `admin_user_id` variable with the Discord ID of the bot admin.
- Modify the `prizes` list with your desired prizes and their probabilities.
- Replace the placeholder token in the `client.run()` function with your Discord bot token.
- Replace wheel.png with any other png or gif which represents your prizes (if you go with gifs, make sure to replace any instance of 'PNG' in the script to 'GIF').
- Adjust any messages to your own liking in line 60 and 104. 

## Usage

1. Start the bot by running the script:

python spin_bot.py

2. Invite the bot to your Discord server using the Discord bot invitation link.

3. Interact with the bot in your server by using the following commands:
- `!spin`: Spin the virtual wheel and have a chance to win prizes.
- `!stats`: Check your spin statistics and prizes won.

## Contributing

Contributions to the Discord Spin Bot are welcome! If you encounter any issues, have suggestions, or want to add new features, please open an issue or submit a pull request.

## License


