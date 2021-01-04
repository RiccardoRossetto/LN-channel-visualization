# visual-channels: A c-lightning Plug-in for a more interpretable overview of the channels of a Lightning Network's node.

The plug-in adds the visualchannel command to the lightning command line interface, it will return a pretty-print of the list of the node's channels containing the following informations:

* *Channel ID*: an integer representing the order of appearance in the channels list.

* *Peer ID*: the ID of the channel's counterpart.
* *Status*: *connected* / *not connected* depending whether the counter-party is on-line or not.
* *Channel Capacity*: The amount (either in sats, EUR, or USD) locked in the payment channel.
* *Funds Distribution*: Displays how the funds are distributed between the two counter-parties, aided by a visual representation.

Here's a sample output where the unit chosen to display the amounts is in $ USD. 

![](/home/joukowski/Documents/Fintech/LightningNetwork/plugins/imgs/sample_output.png)



## Getting Started:

