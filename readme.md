# TurtleBot 4 Setup Guide

This guide provides a comprehensive walkthrough for setting up, configuring, and operating the TurtleBot 4, from unboxing to running advanced robotics applications like SLAM, navigation, and object detection with YOLO.

## 1. Unboxing

Upon opening the TurtleBot 4 package, ensure you have all the following components.

**Top Layer:**
- USB to Type-C cable
- Zipper cable

**Middle Layer:**
- TurtleBot 4 Controller

**Bottom Layer:**
- TurtleBot 4 Robot Unit
- Charging Dock
- 360° Omnidirectional Wheel

## 2. Equipment Checklist

Before starting the assembly and setup, verify you have the following items:
- USB to Type-C cable
- Zippers
- Bluetooth controller
- Various cables and connectors
- USB to B charging cable
- C male to two C female connector
- TurtleBot 4 Robot
- 360° omnidirectional wheel
- TurtleBot 4 Docker (Charging Dock)
- JST connector wires
- SD Card Reader

## 3. Assembly

Follow these steps to assemble the hardware.

1.  **Update ROS Version (Optional but Recommended):**
    - Carefully remove the SD card from the TurtleBot 4 to update its ROS (Robot Operating System) version if needed.

2.  **Attach the Front Wheel:**
    - Gently pick up the TurtleBot and tilt it.
    - Have a second person firmly push the 360-degree omnidirectional wheel into its designated slot at the front of the robot.

3.  **Setup the Charging Dock:**
    - Connect the charging dock to an AC power supply.
    - Place the dock in a fixed, accessible location to serve as the robot's charging station.

## 4. Wi-Fi Configuration

### Initial Connection (Hotspot Mode)

By default, the TurtleBot 4 creates its own Wi-Fi access point (hotspot) if it's not connected to another network.

1.  **Connect to the TurtleBot's Wi-Fi:**
    - **Network Name (SSID):** `turtlebot4`
    - **Password:** `turtlebot4`

2.  **SSH into the Robot:**
    - Open a terminal on your computer.
    - Run the following command to connect to the robot:
      ```bash
      ssh ubuntu@10.42.0.1
      ```
    - When prompted for a password, enter: `turtlebot4`
    - If it's your first time connecting, you may be asked to confirm. Type `yes` and press Enter.

### Connecting TurtleBot to Your Wi-Fi Network

To connect the TurtleBot to your local Wi-Fi for internet access and communication with other devices, follow these steps.

1.  **Access the Setup Menu:**
    - SSH into the robot as described above. The IP address might be different if it's already on a network; check the OLED screen on the robot for the current IP.
      ```bash
      # Replace with the IP on the robot's screen if available
      ssh ubuntu@10.42.0.1
      ```
    - Enter the password: `turtlebot4`
    - Run the setup utility:
      ```bash
      turtlebot4-setup
      ```

2.  **Configure Wi-Fi Settings:**
    - Use the arrow keys to navigate the menu.
    - Select **WiFi Setup** and press Enter.
    - Set **WiFi Mode** to **Client** and press Enter.
    - Select **SSID** and type the name of your Wi-Fi network, then press Enter.
    - Select **Password** and type your Wi-Fi password, then press Enter.
    - Select **Band** and choose **Any**, then press Enter.
    - Navigate to **SAVE** and press Enter.
    - Finally, select **Apply Settings** and press Enter. The robot will configure the new settings and connect to your network. A warning screen may appear, which is normal.

## 5. Software Installation

### Install Ubuntu 24.04
- Follow a standard procedure to install Ubuntu 24.04 on your primary computer (the one you will use to control the robot).

### Install ROS 2 Jazzy on your PC
- Follow the official ROS 2 Jazzy installation documentation. A helpful script and guide can often be found on the official ROS or TurtleBot websites.

### Install TurtleBot 4 Packages

1.  **Install from APT:**
    - First, install the pre-built TurtleBot 4 packages for ROS 2 Jazzy.
      ```bash
      sudo apt-get update && sudo apt install ros-jazzy-turtlebot4*
      ```

2.  **Build from Source (for latest updates):**
    - Create a workspace and clone the repository.
      ```bash
      # Create a workspace directory
      mkdir -p ~/turtlebot4_ws/src
      cd ~/turtlebot4_ws/src

      # Clone the correct branch for your ROS version (e.g., jazzy)
      git clone [https://github.com/turtlebot/turtlebot4.git](https://github.com/turtlebot/turtlebot4.git) -b jazzy
      ```
    - Build the packages:
      ```bash
      cd ~/turtlebot4_ws
      source /opt/ros/jazzy/setup.bash
      colcon build --symlink-install
      ```

## 6. SLAM (Simultaneous Localization and Mapping)

SLAM is used to create a map of an unknown environment.

-   **Run Synchronous SLAM:** (Recommended for better map quality)
    ```bash
    ros2 launch turtlebot4_navigation slam.launch.py
    ```

-   **Run Asynchronous SLAM:**
    ```bash
    ros2 launch turtlebot4_navigation slam.launch.py sync:=false
    ```

## 7. Navigation

This section guides you through controlling the robot, creating a map, and navigating autonomously.

1.  **Connect to the Robot:**
    - Ensure your computer is on the same Wi-Fi network as the TurtleBot.
    - Open a terminal and SSH into the robot using its IP address (displayed on the OLED screen).
      ```bash
      ssh ubuntu@<ip-address-of-robot>
      ```

2.  **Undock the Robot:**
    - In a new terminal on your PC (after sourcing your ROS 2 setup), run:
      ```bash
      ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
      ```
    - To send the robot back to its dock, run:
      ```bash
      ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
      ```

3.  **Start Teleoperation (Manual Control):**
    - Open another terminal to control the robot with your keyboard.
      ```bash
      ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
      ```

4.  **Launch SLAM:**
    - In a new terminal, launch the SLAM node.
      ```bash
      # First, ensure the navigation packages are installed
      sudo apt install ros-jazzy-turtlebot4-navigation

      # Launch SLAM
      ros2 launch turtlebot4_navigation slam.launch.py
      ```

5.  **Launch RViz2 (Visualization):**
    - In another terminal, launch the visualization tool.
      ```bash
      ros2 launch turtlebot4_viz view_navigation.launch.py
      ```
    - Drive the robot around using the teleoperation terminal to build the map in RViz2.

6.  **Save the Map:**
    - Once you are satisfied with the map, open a new terminal and run:
      ```bash
      ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name:
        data: 'my_map_name'"
      ```
    - This will save `my_map_name.pgm` and `my_map_name.yaml` files in your current directory.

### Autonomous Navigation with a Saved Map

1.  **Launch Localization:**
    - In a terminal, run the localization launch file, pointing to your saved map.
      ```bash
      ros2 launch turtlebot4_navigation localization.launch.py map:=/path/to/your/my_map_name.yaml
      ```

2.  **Launch Nav2 Stack:**
    - In another terminal, start the navigation stack.
      ```bash
      ros2 launch turtlebot4_navigation nav2.launch.py
      ```

3.  **Launch RViz2 for Navigation:**
    - In a third terminal, open RViz2.
      ```bash
      ros2 launch turtlebot4_viz view_navigation.launch.py
      ```

4.  **Interact in RViz2:**
    - **2D Pose Estimate:** Use this tool first. Click and drag an arrow on the map in RViz to tell the robot its approximate starting location and orientation.
    - **Nav2 Goal:** Use this tool to set a destination. Click a point on the map, and the robot will plan a path and navigate to it.

## 8. YOLO (Object Detection) Setup

This section describes how to set up YOLO for real-time object detection using the robot's camera.

1.  **Install Ultralytics:**
    - Open a terminal and install the required Python package.
      ```bash
      python3 -m pip install ultralytics --break-system-packages
      ```

2.  **Get the Subscriber Script:**
    - Download the `camera_subscriber.py` script required to process the camera feed.

3.  **Run the YOLO Node:**
    - Navigate to the directory where you saved `camera_subscriber.py`.
    - Run the script:
      ```bash
      python3 camera_subscriber.py
      ```
    - When prompted by the script's menu, enter `2` to start the object detection.
