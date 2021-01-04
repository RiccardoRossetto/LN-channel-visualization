# visual-channels: A c-lightning Plug-in for a more interpretable overview of the channels of a Lightning Network's node.

The plug-in adds the visualchannel command to the lightning command line interface, it will return a pretty-print of the list of the node's channels containing the following informations:

* *Channel ID*: an integer representing the order of appearance in the channels list.

* *Peer ID*: the ID of the channel's counterpart.
* *Status*: *connected* / *not connected* depending whether the counter-party is on-line or not.
* *Channel Capacity*: The amount (either in sats, EUR, or USD) locked in the payment channel.
* *Funds Distribution*: Displays how the funds are distributed between the two counter-parties, aided by a visual representation.

Here's a sample output where the unit chosen to display the amounts is in $ USD. 

![](https://github.com/RiccardoRossetto/LN-channel-visualization/blob/master/imgs/sample_output.png)



## Getting Started:

Once visualchannel.py is downloaded, it should be made executable as follows:

```bash
$ sudo chmod a+x visual-channels.py
```

For clarity and ease of use, you can store it in the c-lightning plug-in directory, which should be in:

```bash
/usr/libexec/c-lightning/plugins/
```

To install the required libraries use the following command:

```bash
$ pip3 install -r requirements.txt
```

Then when running c-lightning, it is sufficient to specify the plug-in directory to have it loaded and ready to be used.

```bash
$ lightningd --plugin-dir=/usr/libexec/c-ligthning/plugins/
```

Note that the plug-in directory must be specified in addition to the options used to run lightningd.

## Instructions

To call the plug-in use the lightning command line interface:

```bash
$ lightning-cli -H visualchannels [unit]
```

Unit can be one of the following:

1. **BTC/btc/bitcoin/satoshi/sathoshis/**: the amounts displayed by the plug-in will be in satoshis.
2. **EUR/eur/euro/euros**: the amounts displayed will be in EUR.
3. **USD/usd/dollar/dollars**: the amounts displayed will be in USD.

In the case in which unit isn't specified, or it's misspelled, the default unit that will be used is **sat**.

