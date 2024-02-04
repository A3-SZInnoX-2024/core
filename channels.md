# Channels

1. `location`: send the location. The `location` channel is the channel transfers the location data from the `CV` to the core. Then, the core will send the location data to the `RC` (Robot Controller) to make decisions based on the location data.

## `location-cv`

The `location-cv` channel is the channel that transfers the location data from the `CV` to the core. It is normally a 3-element array, which contains the x, y coordinates and the angle of the robot (yaw).

## `location-rc`

The `location-rc` channel is the channel that transfers the location data from the core to the `RC` (Robot Controller). It is normally a 3-element array, which contains the x, y coordinates and the angle of the robot (yaw).

2. `block`: send colored block information. The `block` channel is the channel transfers the block information from the `CV` to the core. Then, the core will send the block information to the `RC` (Robot Controller) to make decisions based on the block information.

## `block-cv`

The `block-cv` channel is the channel that transfers the block information from the `CV` to the core. It is normally a 3-element array, which contains the x, y coordinates and the color of the block.

## `block-rc`

The `block-rc` channel is the channel that transfers the block information from the core to the `RC` (Robot Controller). It is normally a 3-element array, which contains the x, y coordinates and the color of the block.
