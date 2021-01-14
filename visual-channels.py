#!/usr/bin/env python3

import os
import json
import cryptocompare
from os.path import join
from lightning.lightning import LightningRpc
from lightning.plugin import Plugin


plugin = Plugin(autopatch = True)

# Mappings for the units to display:

units = {
    "BTC": "sat",
    "bitcoin": "sat",
    "satoshi": "sat",
    "satoshis": "sat",
    "btc": "sat",
    "EUR": "EUR",
    "eur": "EUR",
    "euro": "EUR",
    "euros": "EUR",
    "dollar": "USD",
    "dollars": "USD",
    "USD": "USD",
    "usd": "USD",
}



def header(own, counterparty, unit):
    own = " ->   OWN FUNDS: " + "{:.2f}".format(own) + f" {unit}"
    counterparty = "COUNTERPARTY FUNDS: " + "{:.2f}".format(counterparty) + f" {unit}"
    header = own.ljust(35, " ") + counterparty.rjust(42, " ")
    return header


def imbalance_bar(own, counterparty):
    bar_len = 70
    left = '['
    right = ']'
    total = own + counterparty
    own_share = own / total
    own_share = int(own_share * bar_len)
    counterparty_share = int(bar_len - own_share)
    imbalance_bar = " ->   " + left.ljust(own_share, "=") + "|" + right.rjust(counterparty_share, '-')
    return imbalance_bar


def distribution(own, counterparty, unit):
    distribution = []
    head = header(own, counterparty, unit)
    bar = imbalance_bar(own, counterparty)
    distribution = [" ", " ", head, " ", bar, " "]
    return distribution



def compute_metrics(channels, unit, rate):
    channels_list = []
    channel_count = 0
    for channel in channels:
        channel_count += 1

        # Compute Metrics to be Displayed: 
        separator = "=" * 76
        channel_id = " ({})".format(channel_count)
        peer_id = " " + channel['peer_id']
        status = (" connected" if channel['connected'] == True else " not connected")
        channel_capacity = int(channel['channel_total_sat']) * rate

        own_funds = int(channel['our_amount_msat'] / 1000) * rate
        counterparty_funds = channel_capacity - own_funds

        channels_dict = {
            '': separator,
            'CHANNEL ': channel_id,
            'PEER ': peer_id,
            'STATUS ': status,
            'CHANNEL CAPACITY ': " " + "{:.2f}".format(channel_capacity) + f" {unit}",
            'FUNDS DISTRIBUTION ': distribution(own_funds, counterparty_funds, unit)}

        channels_list.append(channels_dict)
    return channels_list


@plugin.method("visualchannels")
def visualchannels(unit = None):

    """ List the channels of the nodes with the respective capacities
        and imbalances between the two counterparties.

        The displayed balances are in {unit}, which can take as values:
         - btc, BTC, bitcoin, sathosi, satoshis for "sat"
         - eur, EUR, euro, euros for "EUR"
         - usd, USD, dollar, dollars for "USD"

        If unit is not provided, the funds are displayed in sats."""

    if unit is None:
        unit = plugin.get_option("display_unit")
    else:
        unit = units.get(unit, "sat")

    # Set Exchange Rates:
    if unit == "EUR":
        exchange_rate = cryptocompare.get_price('BTC', curr = "EUR")
        exchange_rate = exchange_rate['BTC']['EUR'] / (10 ** 7)
    elif unit == "USD":
        exchange_rate = cryptocompare.get_price("BTC", curr = "USD")
        exchange_rate = exchange_rate['BTC']['USD'] / (10 ** 7)
    else:
        exchange_rate = 1

    funds = rpc_interface.listfunds()
    channels = funds['channels']
    channels_list = compute_metrics(channels, unit, exchange_rate)
    return channels_list


@plugin.init()
def init(options, configuration, plugin):
    global rpc_interface
    plugin.log("Initialization of the Visual Channels Plugin", level = "debug")
    lightning_dir = configuration['lightning-dir']
    rpc_file = configuration['rpc-file']
    path = join(lightning_dir, rpc_file)
    plugin.log("RPC interface located at {}".format(path))
    rpc_interface = LightningRpc(path)
    plugin.log("Plugin Successfully Initializated.")


plugin.add_option("display_unit", "sat",
                                "Default display unit is: sat")

plugin.run()
