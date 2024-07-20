# Two Player Bookworm

## About the Project
### Overview
This was my final output for my Introduction to Python class. We had to create a two-player game with File Management, Socket Communication, and GUI.

The game was inspired by PopCap's Bookworm. However, it's unique in that it has a turn-based two player format and a shared healthbar. You have to compete with your opponent in making the most complex words you can.

![][1]

### Built With
Tkinter was used for the GUI and NLTK for word-checking.

## How to Play
This can be played either on the same computer or on two different computers connected over the same network.

1. Open two terminal windows.
2. Run `python RunServer.py` on one terminal and `python RunClient.py` on the other. 
    * If running on separate devices, change `self.host` in SocketManager.py to the local ip address
3. You can check **Best Words** for the record of the top 10 most complex words made in the game.
4. To start a new game, click on **New Game**. The game will start after you and your opponent have entered your names.
5. First player to win three rounds wins the game.

You can use the three items in the Shop Panel to gain an advantage.
+ Replace - provides a new set of letters. You can purchase this even without sufficient coins but it forfeits your turn.
+ Wildcard - gives you '**?**' that can act as any letter for a valid word. You can have up to seven wildcards before the game crashes from the brute-force word-checking algorithm haha.
+ Powerup - increases damage per letter by 1 point.

### Demo
![][2]

## Planned Changes
* Implement event-based communication between scripts
* Improve UI



[1]: img/GameScreenshot.png
[2]: img/GameDemo.mp4