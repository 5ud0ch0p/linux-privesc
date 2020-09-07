from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import challengehandler
import time
import sys

CHALLCOUNT = 9


# Initialise and print our banner, and start the menu itself
def menu():
    printbanner()
    handlemenu()


def handleselection(chall, level):
    # Check if we have already configured this practical
    if challengehandler.checkchallmutex(chall, level):
        print("> It looks like we have configured this challenge already. ")
        print("> Either create a new docker container, or roll back the previous practical!")
        time.sleep(3)
        return
    # Save the last practical and level we configured
    confirmation = input("> Configuring practical 0x0" + str(chall) + " at level " + str(level)
                         + ". Are you sure? [y/N]: ").strip()
    if confirmation == "y" or confirmation == "Y":
        challengehandler.configurechallenge(chall, level)
        print("> Practical configured. Good luck!")
        time.sleep(1)
    else:
        print("Aborted")


# Actually render and handle menu activity
def handlemenu():
    # Formatting the main menu to select the various practical challenges
    mainmenufmt = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER) \
                                     .set_prompt("SELECT>") \
                                     .set_title_align('center') \
                                     .show_header_bottom_border(True)
    usermenu = ConsoleMenu("Practical selection",
                           prologue_text="Select the practical section to configure...",
                           formatter=mainmenufmt)
    # For each of our challenges, create a menu item
    for practicalcount in range(1, CHALLCOUNT):
        # And create a submenu item so attendees can choose their desired difficulty
        difficulty_submenu = ConsoleMenu("Difficulty selection",
                                         formatter=mainmenufmt)
        for diffcount in range(1, 4):
            difffunct = FunctionItem("Level " + str(diffcount),
                                     function=handleselection,
                                     args=(practicalcount, diffcount,),
                                     should_exit=True)
            difficulty_submenu.append_item(difffunct)
        diff_submenu_item = SubmenuItem("Practical 0x0" + str(practicalcount),
                                        submenu=difficulty_submenu,
                                        menu=usermenu)
        usermenu.append_item(diff_submenu_item)
        # TODO: Add final challenge set as different menu item
    # TODO: Add option to unconfigure all practicals
    # Render the menu
    usermenu.show()


def printbanner():
    bannertext = '''
    ==============================================================================
    
                            dMP     dMP dMMMMb  dMP dMP dMP dMP                                        
                           dMP     amr dMP dMP dMP dMP dMK.dMP                                         
                          dMP     dMP dMP dMP dMP dMP .dMMMK"                                          
                         dMP     dMP dMP dMP dMP.aMP dMP"AMF                                           
                        dMMMMMP dMP dMP dMP  VMMMP" dMP dMP                                            

                dMMMMb  dMMMMb  dMP dMP dMP dMP dMP     dMMMMMP .aMMMMP dMMMMMP            
               dMP.dMP dMP.dMP amr dMP dMP amr dMP     dMP     dMP"    dMP                 
              dMMMMP" dMMMMK" dMP dMP dMP dMP dMP     dMMMP   dMP MMP"dMMMP                
             dMP     dMP"AMF dMP  YMvAP" dMP dMP     dMP     dMP.dMP dMP                   
            dMP     dMP dMP dMP    VP"  dMP dMMMMMP dMMMMMP  VMMMP" dMMMMMP                

        dMMMMMP .dMMMb  .aMMMb  .aMMMb  dMP     .aMMMb dMMMMMMP dMP .aMMMb  dMMMMb 
       dMP     dMP" VP dMP"VMP dMP"dMP dMP     dMP"dMP   dMP   amr dMP"dMP dMP dMP 
      dMMMP    VMMMb  dMP     dMMMMMP dMP     dMMMMMP   dMP   dMP dMP dMP dMP dMP  
     dMP     dP .dMP dMP.aMP dMP dMP dMP     dMP dMP   dMP   dMP dMP.aMP dMP dMP   
    dMMMMMP  VMMMP"  VMMMP" dMP dMP dMMMMMP dMP dMP   dMP   dMP  VMMMP" dMP dMP    
    
    ==============================================================================
                                Troy Defty (@5ud0ch0p)
                     Lukasz Gogolkiewicz (@synick)
    =============================================================================='''
    print(bannertext)
    time.sleep(1)
