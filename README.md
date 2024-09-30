# Candy Home Assistant component

[comment]: <> [![Run tests](https://github.com/hatoris/home-assistant-candy/actions/workflows/test.yml/badge.svg)](https://github.com/hatoris/home-assistant-candy/actions/workflows/test.yml)
[comment]: <> [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[comment]: <> [![codecov](https://codecov.io/gh/hatoris/home-assistant-candy/branch/main/graph/badge.svg?token=HE0AIQOGAD)](https://codecov.io/gh/hatoris/home-assistant-candy)

Custom component for [Home Assistant](https://homeassistant.io) that integrates Candy/Haier/Simply-Fi home appliances.

This is a fork of the excellent work of [ofalvai](https://github.com/ofalvai): [https://github.com/ofalvai/home-assistant-candy](https://github.com/ofalvai/home-assistant-candy)


## Features
- Supported appliances:
   - washing machine 
   - tumble dryer
   - oven
   - dishwasher
- Uses the local API and its status endpoint
- Creates various sensors, such as device state and remaining time. Everything else is exposed as sensor attributes

## Installation

1. Install [HACS](https://hacs.xyz/)
2. Go to the integrations list in HACS and search for `Candy Simply-Fi`
4. Restart Home Assistant
5. Go to the Integrations page, click Add integrations and select `Candy`
6. Complete the config flow

## Configuration

You need the IP address of the machine and the encryption key. This can be guessed with [CandySimplyFi-tool](https://github.com/MelvinGr/CandySimplyFi-tool).

## This repo add the possibility to control the DishWasher (start/stop)

Control has been included to allow to send program + option to start the dishwasher or stop it. 