

#Nao imports

import nao_nocv_2_1 as nao

#Import all the dialogs

import start_dialog_hello as diaHello
import start_dialog_name as diaName
import start_dialog_dance as diaDance
import start_dialog_ready as diaReady
import start_dialog_end as diaEnd


#import the gestures.
import start_dance_behavior as Dance

#Import landmark detection
import landmark_detection as targetDetect

robot_ip="192.168.0.115" # replace this with the actual ip address of the robot
port=9559 # Robot port number


def doRobotOff():                   # state 0, initialize the robot
    nao.InitProxy("192.168.0.115")
    nao.InitPose() 
    nao.InitSonar(True)
    nao.InitLandMark()
    state = "SearchParticipant"
    return state
    

def doSearchDanceParticipant(participants):
            # state 1, search dancefloor: once initially and once when humans are invited
    nao.InitTrack
    nao.ALTrack
    nao.MoveHead()                  #check dit
        
    detected, timestamp, markerInfo= nao.DetectLandMark()
    if detected:
    # robot searches for dancefloor/target
    # first search dancefloor
        state = "MoveTarget" 
    return state


def moveTarget(markerInfo):
    detected, timestamp, markerInfo= nao.DetectLandMark()
    if detected:
        nao.Move(dx=targetDetect.compute_velocity(SL, SR, target_distance), dy=0, dtheta=targetDetect.compute_turnrate(target_distance, target_angle, SL, SR), freq=1)
    state = "intro"
    return state

def intro(robot_ip, port):              #hello dialog, robots starts this off with the nao.Say() function
    #dialog_topic = "/home/nao/group_11/Hello_enu.top"  # Absolute path of the dialog topic file (on the robot).
    nao.Say("Hello there")
    nao.sleep(5)
    #nao.GoToPosture()  # --> Waving hand 
    state = "Name_ask"
    return state

def name_ask(robot_ip, port):  #Name dialog, robots ask for name, after which it responds to your name and ask for your mood
    dialog_topic = "/home/nao/group_11/Name_enu.top"
    nao.Say("My name Nao, what is yours")
    nao.sleep(2)
    diaName.main(robot_ip, port, dialog_topic)
    #nao.sleep(2)
    state = "Dance"
    return state


def dance():    #Dance dialog
    dialog_topic = "/home/nao/group_11/Dance_enu.top"
    diaDance.main(robot_ip, port, dialog_topic)
    nao.GoToPosture()  #Do a dance move 
    state = "Ready"
    return state

def ready_to_dance(): #asking whether the person is ready to dance dialog
    dialog_topic = "/home/nao/group_11/Ready_enu.top" 
    nao.Say("Are you ready?")
    diaReady.main(robot_ip, port, dialog_topic)
    state = "Finish"
    return state

def dance():
    core_dance = "/home/nao/group_11/Behaviour_Dance_enu.top"
    Dance.main(robot_ip, port, core_dance)


def finish():        #th
    dialog_topic = "/home/nao/group_11/End_enu.top" 
    nao.Say("Great job. It was a pleasure to dance with you.")
    nao.sleep(2)
    diaEnd.main(robot_ip, port, dialog_topic)
    state = "Stop"
    return state

def doError():                      # state X
    # robot says something and does something
    nao.Move(dx = 0, dy = 0, dtheta = 0)
    nao.InitSonar(False)                    # turn off sonars
    nao.say('')                             # Stop Talking
    nao.Crouch()                            # always end in this position
    state = 'Stop'
    return state


def main():     # State Machine
    # initialize parameters that are used in the states
          # List of stored names
    state = 'RobotOff'
    while state is not 'Stop':      # 'Stop' is now the final state where it stops
        if state == 'RobotOff':
            state = doRobotOff()
        elif state == 'SearchParticipant':
            state = doSearchDanceParticipant()
        elif state == 'MoveTarget':
            state = moveTarget()
        elif state == 'Intro':
            state = intro(robot_ip, port)  
        elif state == 'Name_ask':
            state = name_ask(robot_ip, port)        
        elif state == 'Dance':
            state = dance(robot_ip, port)  
        elif state == 'Ready':
            state = ready_to_dance(robot_ip, port)  
        elif state == 'Finish':
            state = finish(robot_ip, port)  
        else:       # if none of the above states --> unknown state so error
            state = doError()


    nao.Move(dx = 0, dy = 0, dtheta = 0)
    nao.InitSonar(False)                    # turn off sonars
    nao.Say('')                             # Stop Talking
    nao.Crouch()                            # always end in this position



if __name__ == "__main__":
    main()