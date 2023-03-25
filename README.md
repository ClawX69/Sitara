# Sitara Bot

Sitara Bot is a star-board bot designed to save starred messages on Discord servers. The bot includes three commands for managing the star-board feature:

## Table of Contents

- [Getting Started](#getting-started)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with Sitara Bot, follow these steps:

1. Invite the bot to your Discord server.
2. Grant the necessary permissions to the bot.
3. Use the commands to configure the star-board feature.

## Commands

The following commands are available with Sitara Bot:

### s.set-starboard/s.sb

This command sets the channel to be used as the star-board. It takes an optional argument for the channel name, channel ID, or mention. If no argument is provided, the command will use the channel in which it was used as the star-board channel.

Example usage: `s.set-starboard #star-board`

### s.star-count/s.sc

This command sets the minimum number of stars required for a message to be saved to the star-board. It takes one required argument for the star count. If a message has at least the specified number of star reactions, it will be saved to the star-board. By default, the star count is set to 5.

Example usage: `s.star-count 3`

### s.starit

This command manually saves a message to the star-board, even if it does not meet the minimum star count requirement. It takes one required argument for the message ID. It can also work if a user replies to the message they want to star without passing the message ID to the command.

Example usage: `s.starit 123456789012345678`

## Contributing

If you would like to contribute to Sitara Bot, please follow these guidelines:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## License

Sitara Bot is released under the [MIT License](https://opensource.org/licenses/MIT). Please see the LICENSE file for more information.
