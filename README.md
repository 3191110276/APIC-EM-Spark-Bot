# Cisco APIC-EM Spark Bot
This is a Spark chat bot, which allows to interact with Cisco's APIC-EM platform through natural language. Users can ask questions to the bot, and receive graphical answers back in the chat client.

This script is currently a proof of concept and is not intended for production usage!

Table of Contents
=================

   * [Features](#features)
      * [Installation](#installation)
      * [Usage](#usage)
      * [Development](#development)

## Features

This implementation of the Spark Bot allows for answering the following questions:
* Checking of the network status (for example: “What is my network status?“)
* Find out errors with the network devices. (for example: “What is wrong with my network devices?“)
* Finding of host connections based on IP or MAC (for example: “Where is 10.1.15.117 connected?“)
* Helping with the expansion of the network (for example: “I want to expand my network”)
* Get a list of network devices (for example: “What are my network devices?“)

## Installation

The script itself only provides the backend for the bot. It can either be started using a Docker container via the provided Dockerfile, or by running the Python script natively. If you decide to natively run the Python script, it would be recommended to install all the requirements using pip:
```
pip install -r requirements.txt
```

## Usage



## Development




WARNING:

This scripts are meant for educational/proof of concept purposes only. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
