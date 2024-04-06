import customtkinter
import json
import uuid
import socket
import pymongo
from dotenv import load_dotenv
import os
from script.gesture_control import GestureControl
import threading
from script.modules.GestureAnimation import GestureAnimation


load_dotenv()


def get_unique_id():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    hostname = socket.gethostname()
    return f"{mac}-{hostname}"

ges_con = GestureControl(True)
ges_con_thread = threading.Thread(target=ges_con.run)

unique_id = get_unique_id()
print(unique_id)

client = pymongo.MongoClient(os.getenv("MONGODB.URI"))

db = client["hci"]

collection = db["user-config"]

customGestureJson = collection.find_one({"_id": unique_id})

f = open("script\\appList.json", "r")
data = json.load(f)

f = open("script\\anim_data.json", "r")
anim_data = json.load(f)

if customGestureJson == None:
    collection.insert_one(
        {
            "_id": unique_id,
            "name": socket.gethostname(),
            "userDefinedControls": {
                "index": "null",
                "index and middle": "null",
                "index, middle and ring": "null",
                "index, middle, ring and little": "null",
                "thumb": "null",
            },
        }
    )

    customGestureJson = collection.find_one({"_id": unique_id})

    with open("./script/modules/user_defined_data.json", "w") as f:
        json.dump(customGestureJson, f)

app = customtkinter.CTk()
app.title("Gesture Navigator")
app.geometry("600x500")
app.iconbitmap("dark.ico")

# system mode
customtkinter.set_appearance_mode("system")

# Create two frames for the screens
menuFrame = customtkinter.CTkFrame(app, corner_radius=25, border_width=5)
customiseFrame = customtkinter.CTkFrame(app)
tutorialFrame = customtkinter.CTkFrame(app)


def getAppNames():
    # read a file appList.json and fetch names
    # return the list of app names
    ls = ["Select"]
    for i in data:
        ls.append(i["displayName"])
    return ls


# Function to switch to the second screen
def goToCustomise():
    menuFrame.pack_forget()
    customiseFrame.pack(fill="both", expand=True)


# Function to switch to the third screen
def goToTutorial():
    menuFrame.pack_forget()
    tutorialFrame.pack(fill="both", expand=True)


# Function to run python script
def launchGestureControl():
    if not ges_con_thread.is_alive():
        ges_con.runFlag = True
        ges_con_thread.start()
    else :
        print("The program is already running. Please wait")

# Function to switch back to the first screen
def backToMenuFrame():
    customiseFrame.pack_forget()
    tutorialFrame.pack_forget()
    menuFrame.pack(fill="both", expand=True, pady=60, padx=90)


# Function to print "Hello, World!"
def print_hello_world(varName):
    print("Hello, World!", varName)


def saveGestures(data):
    userDefinedControls = {}
    userDefinedControls["index"] = (
        gesture1_dropdown.get() if gesture1_dropdown.get() != "Select" else "null"
    )
    userDefinedControls["index and middle"] = (
        gesture2_dropdown.get() if gesture2_dropdown.get() != "Select" else "null"
    )
    userDefinedControls["index, middle and ring"] = (
        gesture3_dropdown.get() if gesture3_dropdown.get() != "Select" else "null"
    )
    userDefinedControls["index, middle, ring and little"] = (
        gesture4_dropdown.get() if gesture4_dropdown.get() != "Select" else "null"
    )
    userDefinedControls["thumb"] = (
        gesture5_dropdown.get() if gesture5_dropdown.get() != "Select" else "null"
    )

    for i in data:
        if i["displayName"] == userDefinedControls["index"]:
            userDefinedControls["index"] = i["shellName"]
        if i["displayName"] == userDefinedControls["index and middle"]:
            userDefinedControls["index and middle"] = i["shellName"]
        if i["displayName"] == userDefinedControls["index, middle and ring"]:
            userDefinedControls["index, middle and ring"] = i["shellName"]
        if i["displayName"] == userDefinedControls["index, middle, ring and little"]:
            userDefinedControls["index, middle, ring and little"] = i["shellName"]
        if i["displayName"] == userDefinedControls["thumb"]:
            userDefinedControls["thumb"] = i["shellName"]

    if customGestureJson is not None:
        customGestureJson["userDefinedControls"] = userDefinedControls
        collection.update_one({"_id": unique_id}, {"$set": customGestureJson})

    with open("./script/modules/user_defined_data.json", "w") as f:
        json.dump(customGestureJson, f)


############################################################################################################
# First screen
menuFrame.pack(fill="both", expand=True, pady=60, padx=90)
launchButton = customtkinter.CTkButton(
    menuFrame,
    text="Launch program",
    command=lambda: launchGestureControl(),
)
launchButton.pack(pady=50)

customiseButton = customtkinter.CTkButton(
    menuFrame, text="Customise gestures", command=lambda: threading.Thread(target=goToCustomise).start()
)
customiseButton.pack(pady=30)

tutorialButton = customtkinter.CTkButton(
    menuFrame, text="Tutorial", command=lambda: goToTutorial()
)
tutorialButton.pack(pady=50)

############################################################################################################
# Second screen
customiseDesc = customtkinter.CTkLabel(
    customiseFrame, text="Customise your gestures here"
)
customiseDesc.pack(pady=5)
customiseDesc2 = customtkinter.CTkLabel(
    customiseFrame,
    text="You have five available gestures to customise which\ncan launch an app from the given list of apps.",
)
customiseDesc2.pack(pady=5)

# Five drop down lists should be there

# Gesture 1
gesture1_frame = customtkinter.CTkFrame(customiseFrame)
gesture1_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture1_label = customtkinter.CTkLabel(gesture1_frame, text="Gesture 1")
gesture1_label.pack(side="left", pady=5, padx=80)

gesture1_dropdown = customtkinter.CTkComboBox(gesture1_frame, values=getAppNames())
gesture1_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if i["shellName"] == customGestureJson["userDefinedControls"]["index"]:
            gesture1_dropdown.set(i["displayName"])
gesture1_frame.pack_configure(anchor="center")

# Gesture 2
gesture2_frame = customtkinter.CTkFrame(customiseFrame)
gesture2_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture2_label = customtkinter.CTkLabel(gesture2_frame, text="Gesture 2")
gesture2_label.pack(side="left", pady=5, padx=80)

gesture2_dropdown = customtkinter.CTkComboBox(gesture2_frame, values=getAppNames())
gesture2_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"]["index and middle"]
        ):
            gesture2_dropdown.set(i["displayName"])
gesture2_frame.pack_configure(anchor="center")

# Gesture 3
gesture3_frame = customtkinter.CTkFrame(customiseFrame)
gesture3_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture3_label = customtkinter.CTkLabel(gesture3_frame, text="Gesture 3")
gesture3_label.pack(side="left", pady=5, padx=80)

gesture3_dropdown = customtkinter.CTkComboBox(gesture3_frame, values=getAppNames())
gesture3_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"]["index, middle and ring"]
        ):
            gesture3_dropdown.set(i["displayName"])
gesture3_frame.pack_configure(anchor="center")

# Gesture 4
gesture4_frame = customtkinter.CTkFrame(customiseFrame)
gesture4_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture4_label = customtkinter.CTkLabel(gesture4_frame, text="Gesture 4")
gesture4_label.pack(side="left", pady=5, padx=80)

gesture4_dropdown = customtkinter.CTkComboBox(gesture4_frame, values=getAppNames())
gesture4_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"][
                "index, middle, ring and little"
            ]
        ):
            gesture4_dropdown.set(i["displayName"])
gesture4_frame.pack_configure(anchor="center")

# Gesture 5
gesture5_frame = customtkinter.CTkFrame(customiseFrame)
gesture5_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture5_label = customtkinter.CTkLabel(gesture5_frame, text="Gesture 5")
gesture5_label.pack(side="left", pady=5, padx=80)

gesture5_dropdown = customtkinter.CTkComboBox(gesture5_frame, values=getAppNames())
gesture5_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if i["shellName"] == customGestureJson["userDefinedControls"]["thumb"]:
            gesture5_dropdown.set(i["displayName"])
gesture5_frame.pack_configure(anchor="center")


# button to save gestures
saveButton = customtkinter.CTkButton(
    customiseFrame, text="Save", command=lambda: saveGestures(data)
)
saveButton.pack_configure(anchor="center", pady=20)
backToMainMenu = customtkinter.CTkButton(
    customiseFrame, text="Back", command=lambda: backToMenuFrame()
)
backToMainMenu.pack_configure(anchor="center", pady=0)

############################################################################################################
# Third Screen
# Third screen is for the user to view tutorial

# Create a dropdown list
options = list(anim_data.keys())
selected_option = customtkinter.StringVar()
dropdown = customtkinter.CTkComboBox(
    tutorialFrame, values=options, variable=selected_option
)
dropdown.set(options[0])
dropdown.pack(pady=20)

# Create a frame for the GIFs
gif_frame = customtkinter.CTkFrame(tutorialFrame)
gif_frame.pack(ipady=20, ipadx=20)

# Specify the hands for the GIFs, these should be displayed side by side above the GIFs
left_hand = customtkinter.CTkLabel(gif_frame, text="Left Hand")
left_hand.grid(row=0, column=0, padx=30, pady=10)

right_hand = customtkinter.CTkLabel(gif_frame, text="Right Hand")
right_hand.grid(row=0, column=1, pady=10)

# Create labels for the GIFs
left_gif_label = GestureAnimation(gif_frame, "left", "animations\\1.gif")
right_gif_label = GestureAnimation(gif_frame, "right", "animations\\2.gif")

# Create a frame for the heading and description
description_frame = customtkinter.CTkFrame(
    tutorialFrame, width=400, height=200, corner_radius=25, border_width=5
)
description_frame.pack(ipady=5, pady=10)

# Create the heading
heading = customtkinter.CTkLabel(
    description_frame, text="Description", font=("Arial", 16, "bold")
)
heading.pack(pady=10)

# Create the description text
description_label = customtkinter.CTkLabel(
    description_frame, text=anim_data[options[0]]["description"], wraplength=500
)
description_label.pack(pady=5, padx=20)


# Function to update the GIFs based on the selected option
def update_gifs(*_):
    try:
        option = selected_option.get()
        description_label.configure(text=anim_data[option]["description"])
        left_gif_label.update_gif(anim_data[option]["left"])
        right_gif_label.update_gif(anim_data[option]["right"])
    except Exception as e:
        pass

# Bind the update_gifs function to the dropdown selection
selected_option.trace_add("write", update_gifs)

# Create a button to go back to the main menu
back_button = customtkinter.CTkButton(
    tutorialFrame, text="Back", command=backToMenuFrame
)
back_button.pack()

app.mainloop()

# To be executed when the app is closed
ges_con.runFlag = False
ges_con_thread.join()

client.close()
