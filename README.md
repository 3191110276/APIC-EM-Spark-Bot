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

Once you have the local client up and running, you can serve requests. For this prototype, the natural language processing (NLP) is done through [Dialogflow](https://dialogflow.com/). This tool receives the Spark message of the user and then matches the message to 'intents' that have been created in the tool. You can either re-create the intents manually, or you can install the provided 'Spark-Cisco-Connector.zip' in your own Dialogflow instance.

In terms of setup, you need to add your Spark Bot account to Dialogflow. Once that is done, you just need to point your Dialogflow instance to the IP or URL of your Python script, and you can start serving requests. Requests will then flow from the Spark client to Dialogflow to the Python script. The Python script then directly replies to the Spark user without going through Dialogflow.

## Development

You can extend the capabilities of the Spark Bot in a two step process. First, you need to add a new intent in Dialogflow. This allows us to differentiate the request in the script and route the request to the corresponding function. Creating this function is the second step, which then allows us to answer a client request. This function has to contain all the logic, which involves parsing the inputs and creating the response.

Contact: Michael Maurer (mimaurer@cisco.com)


WARNING:

This scripts are meant for educational/proof of concept purposes only. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
