#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use setAngles Method"""

import qi
import argparse
import sys
import time
import rospy
from sensor_msgs.msg import JointState

#session = None

def main(msg, session):
    """
    This example uses the setAngles method.
    """
    # Get the service ALMotion.
    joint_states = msg.position

    motion_service  = session.service("ALMotion")

    motion_service.setStiffnesses("Head", 1.0)

    # Example showing how to set angles, using a fraction of max speed
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [0.0, 0.0]
    fractionMaxSpeed  = 0.2
    motion_service.setAngles(names, angles, fractionMaxSpeed)

    time.sleep(3.0)
    motion_service.setStiffnesses("Head", 0.0)


if __name__ == "__main__":
    #global session
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    rospy.init_node("pepper_head_correction")
    rospy.Subscriber("/pepper_robot/naoqi_driver/joint", JointState, lambda msg: main(msg, session))
    #main(session)
