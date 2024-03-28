# Human-Computer-Interaction using gestures

Human-Computer-Interaction using gestures is a Python application designed to provide users with customizable gesture controls for launching various applications. This application utilizes Python's tkinter library for creating a graphical user interface (GUI) and interacts with MongoDB for storing user-defined configurations.

## Features

- **Customizable Gestures**: Users can assign specific applications to different gestures (e.g., tapping, swiping) for quick access.
- **User-Friendly Interface**: The GUI allows users to easily customize their gestures and manage their configurations.
- **Persistent Storage**: User configurations are stored in a MongoDB database, ensuring that preferences are retained across sessions.
- **Cross-Platform Compatibility**: The application is compatible with multiple operating systems including Windows and macOS.

## How It Works

1. **Unique ID Generation**: The application generates a unique identifier based on the user's machine's MAC address and hostname.
2. **MongoDB Integration**: Utilizing pymongo, the application connects to a MongoDB database to store and retrieve user configurations.
3. **GUI Creation**: The tkinter library is used to create a two-screen GUI. The first screen displays options to launch the program or customize gestures, while the second screen allows users to customize their gesture preferences.
4. **Custom Gesture Configuration**: Users can select applications from a predefined list and assign them to five available gestures (index, index and middle, index, middle and ring, index, middle, ring and little, thumb).
5. **Persistence**: User-defined configurations are saved to the MongoDB database and a local JSON file for persistence across sessions.
6. **Launching Applications**: Upon customization and saving of gestures, users can launch the assigned applications by performing the corresponding gestures.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- MongoDB

## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: 
   - Depending on your system, choose the appropriate requirements file to install the necessary Python packages:
     - For macOS (Darwin):
       - Run `pip install -r requirements_apple_silicon.txt` if you're using an Apple Silicon-based Mac.
     - For Windows:
       - Run `pip install -r requirements_windows.txt` to install the required Python packages.

3. **Set Up MongoDB**: Make sure MongoDB is running locally or accessible via a URI. Set the MongoDB URI in a `.env` file in the project directory.
4. **Run the Application**: Execute the Python script `main.py` to launch the application.
5. **Customize Gestures**: Follow the on-screen instructions to customize gestures and assign applications.
6. **Enjoy Gesture Navigation**: Once customization is complete, use the assigned gestures to perform various actions with ease.

## Contributors

This project was made possible thanks to the collaborative efforts of the following team members:

| Contributor                  | Role                           |
|-----------------------|--------------------------------|
| Medhaj Bhandari       | GUI Development, Blender Animations  |
| Akshat V Ghanathay    | Gesture Recognition Algorithm, Testing |
| Aditya Chintala       | Database Integration, GUI Development, Windows specific algorithm |
| Adithya Kramadhati    | Gesture Recognition Algorithm, Documentation, GUI Development |


## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
