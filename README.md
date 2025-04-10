# FIU eCTF 2025 - Satellite TV System

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Installation and Setup](#installation-and-setup)
  - [Environment Setup](#environment-setup)
  - [Building the Deployment](#building-the-deployment)
  - [Building the Decoder](#building-the-decoder)
- [Usage Instructions](#usage-instructions)
  - [Generating Subscription Updates](#generating-subscription-updates)
  - [Flashing the Decoder](#flashing-the-decoder)
  - [Using the Host Tools](#using-the-host-tools)
    - [List Tool](#list-tool)
    - [Subscription Update Tool](#subscription-update-tool)
    - [Testing Tools](#testing-tools)
        - [Tester Tool](#tester-tool)
        - [Stability Test Tool](#stability-test-tool)
        - [Stress Test Tool](#stress-test-tool)
  - [Running the Complete System](#running-the-complete-system)
    - [1. Uplink](#1-uplink)
    - [2. Satellite](#2-satellite)
    - [3. TV](#3-tv)
- [Troubleshooting](#troubleshooting)

## Overview

This repository contains the implementation of a secure Satellite TV System for the MITRE eCTF 2025 competition. The system consists of three main components: an Encoder, a Satellite, and a Decoder. The Encoder encodes and encrypts TV frames, the Satellite broadcasts the encoded frames, and the Decoder decrypts and decodes the frames for viewing on authorized TVs.

## Repository Structure

- **`decoder/`** - Firmware for the television decoder
  - `project.mk` - Project-specific variables for the Makefile
  - `Makefile` - Invoked by eCTF tools when creating a decoder
  - `Dockerfile` - Build environment description
  - `inc/` - C header files
  - `src/` - C source files
  - `scripts/` - Python scripts for decoder key access
  - `wolfssl/` - WolfSSL cryptographic library

- **`design/`** - Host design elements
  - `ectf25_design/` - Host design source code
    - `encoder.py` - Frame encoding implementation
    - `gen_secrets.py` - Shared secrets generation
    - `gen_subscription.py` - Subscription generation
  - `pyproject.toml` - Python package configuration

- **`frames/`** - Example frame data

- **`tools/`** - Host tools (**DO NOT MODIFY**)
  - `ectf25/` - Tool source code
    - `tv/` - TV-related functionality
    - `uplink/` - Uplink functionality
    - `utils/` - Utility functions
    - `satellite.py` - Satellite functionality
  - `pyproject.toml` - Python package configuration

## Installation and Setup

### Environment Setup

Our system uses Docker for building components and Python for host tools. Follow these steps to set up your environment:

#### Linux:
```bash
# Create a virtual environment
cd <repository_root>
python -m venv .venv --prompt ectf-example

# Enable virtual environment
source ./.venv/bin/activate

# Install host tools
python -m pip install ./tools/

# Install host design elements as an editable module
python -m pip install -e ./design/
```

#### PowerShell:
```powershell
# Create a virtual environment
cd <repository_root>
python -m venv .venv --prompt ectf-example

# Enable virtual environment
.\.venv\Scripts\Activate.ps1

# Install host tools
python -m pip install .\tools\

# Install host design elements as an editable module
python -m pip install -e .\design\
```

### Building the Deployment

First, generate the shared secrets used by the decoder and encoder:

```bash
mkdir secrets
python -m ectf25_design.gen_secrets secrets/secrets.json 1 3 4
```

This will generate a secrets file for channels 1, 3, and 4.

### Building the Decoder

Next, build the decoder with a specific device ID:

#### Linux:
```bash
cd <repository_root>/decoder
docker build -t decoder .
docker run --rm -v ./build_out:/out -v ./:/decoder -v ./../secrets:/secrets -e DECODER_ID=0xdeadbeef decoder
```

#### PowerShell:
```powershell
cd <repository_root>\decoder
docker build -t decoder .
docker run --rm -v .\build_out:/out -v .\:/decoder -v .\..\secrets:/secrets -e DECODER_ID=0xdeadbeef decoder
```

> **Note:** If the build hangs indefinitely, try restarting Docker. If that doesn't help, restart your system.

## Usage Instructions

### Generating Subscription Updates

Use `gen_subscription.py` to generate subscription updates for decoders:

```bash
python -m ectf25_design.gen_subscription secrets/secrets.json subscription.bin 0xDEADBEEF 32 128 1
```

This creates a subscription file targeting a device with ID 0xDEADBEEF, with a subscription window from timestamp 32 to 128 for channel 1.

### Flashing the Decoder

Flash the built firmware to your MAX78000 hardware. The device must be in update mode (flashing blue LED):

#### Linux:
```bash
python -m ectf25.utils.flash ./decoder/build_out/max78000.bin /dev/tty.usbmodem11302
```

#### PowerShell:
```powershell
python -m ectf25.utils.flash .\decoder\build_out\max78000.bin COM12
```

### Using the Host Tools

> **NOTE** All arguments for these tools can be found within their files, within a function titled "parse_args()."

#### List Tool

View the channels currently subscribed on a decoder:

```bash
# Linux
python -m ectf25.tv.list /dev/tty.usbmodem11302

# PowerShell
python -m ectf25.tv.list COM12
```

#### Subscription Update Tool

Update a decoder's subscriptions:

```bash
# Linux
python -m ectf25.tv.subscribe subscription.bin /dev/tty.usbmodem11302

# PowerShell
python -m ectf25.tv.subscribe subscription.bin COM12
```

This will subscribe the decoder on connected to specified port to the subscription written to subscription.bin

#### Testing tools

These are host tools that have been developed to help developers of this system optimize their designs. Use at your own free will.

##### Tester Tool

Test frame decoding functionality:

```bash
# Linux
python -m ectf25.utils.tester --port /dev/tty.usbmodem11302 -s secrets/secrets.json rand -c 1 -f 64

# PowerShell
python -m ectf25.utils.tester --port COM12 -s secrets\secrets.json rand -c 1 -f 64
```

This will encode and decode randomly generated 64-byte frames on channel 1.

##### Stability Test Tool

Test frame encoding and decoding functionality w/ performance statistics (i.e. FPS, timing fails, failure rate, total decodes) through a single channel, in which a subscription is provided:

```bash
# Powershell
python -m ectf25.utils.stability_test -p COM12  -g secrets\secrets.json -c 1 -di 0xdeadbeef -r stab_test.log -d 240 -s 
```

This will encoded random frames (using secrets from secrets.json) on channel 1, for a device named 0xdeadbeef connected to port 12, for 240 minutes (4 hours), and a subscription to channel 1 is provided.

##### Stress Test Tool

Test encoder and decoder seperately. The tool generates frames for decoder to encode and dumps these frames to a chosen JSON file; The tool decodes encoded frames from any given file (JSON list of base64-encoded frames):

###### encode
```bash
# Powershell
python -m ectf25.utils.stress_test --test-size 10000 encode secrets\secrets.json --dump frames\encoded_frames.json
```
This will encode 10,000 random 64-byte frames (using secrets.json) and dump these encoded frames to encoded_frames.json.

###### decode
```bash
# Powershell
python -m ectf.utils.stress_test decode COM12 frames\encoded_frames.json
```
This will decode all frames from encoded_frames.json

### Running the Complete System

To run the full system, you need to start three components in sequence (in order):

#### 1. Uplink

Start the uplink in one terminal:

```bash
# Linux/PowerShell
python -m ectf25.uplink secrets/secrets.json localhost 2000 1:10:frames/x_c0.json
```
> **Note:** This uses one of the sample frame files, and localhost must be used if your are running this locally

#### 2. Satellite

Start the satellite in another terminal:

```bash
# Linux/PowerShell
python -m ectf25.satellite localhost 2000 localhost 1:2001
```

#### 3. TV

Start the TV for each decoder:

```bash
# Linux
python -m ectf25.tv.run localhost 2001 /dev/tty.usbmodem11302

# PowerShell
python -m ectf25.tv.run localhost 2001 COM12
```

## Troubleshooting

- **Build hangs indefinitely**: Restart Docker or your system
- **Connection issues**: Verify your port settings and device connections
- **Subscription failures**: Check that the device ID and channel numbers match your configuration
- **Decoder not responding**: Ensure the device is properly flashed and in the correct mode
- **Frame decoding issues**: Verify that subscriptions are active and that secrets are properly configured