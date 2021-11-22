'''Main Window options:
[1] : Setup Screencapture options
[2] : Clear Images (X amount)
[3] : Best Move Trainer
[4] : Bad Move Trainer
[5] : Exit


CTMaster Class:
	--Tuple pos1
	--Tuple pos2


Setup Screen Capture (Class) extends CTMaster
	-- FINAL KeyCode capture_key = SpaceBar
	
	constructor():
		print("Screenshot setup initiated,"
		+ capture_key + " to get pos1, then again for pos2")
		

		while(True):
			waitForKeyPress(e):
				print("Waiting or pos1 to be set, press space")
				if(e.Code == capture_key):
					this.pos1 = pyautogui.capture()

				print("Pos1 Set as: " + pos1)

			waitForKeyPress(e):
				print("Waiting or pos2 to be set, press space")
				if(e.Code == capture_key):
					this.pos1 = pyautogui.capture()

				print("Pos1 Set as: " + pos1)

			print("Region Set From: " +pos1+" To " + pos2)
			print("Would you like to set again(yes - no)?")

			if input == yes:
				continue
			else:
				break

Clear Images (Method):
	print("Are you sure?")

	if input == yes:
		for x in imagesDir:
		if x.name == chessCapture*.png:
			delete(x)
		print("Images successfully deleted")
		pause
	else:
		print("Image delete cancelled")
		pause

Best Move Trainer (Class) extends CTMaster:
	--FINAL KeyCode NextKey = SpaceBar
	--FINAL KeyCode ExitKey = Backspace
	--String player = "w"
	-- String imgName = None

	
	
	constructor():
		print("white or black"
		if input == black:
			this.player = b
		else:
			this.player = w


		print("Best Move Trainer Started, press space to get next move")
		while(True):
			print("waiting...")
			waitForKeyPress(e):
				if(e.Code == NextKey):
					image = pyautogui.bbox(this.pos1, this.pos2)	
					imgName = "chessCapture" + Date.Day + Date.hour + Date.second + ".png"
					image.save(imgName)
					print(findBestMove(imgName))
				elif(e.code == ExitKey):
					break

	String findBestMove(imageName):
		* import Chessfen.tensorflow_chessbot.py as tfcb
		fen = tfcb --filepath ChessImages/imageName
		bm = stockfish(BestMove for this.player, fen)
		return bm.toString()



	

'''
import sys
sys.path.append('./tfchess')
sys.path.append('./chess-board')

import os
from pynput import keyboard
import pyautogui
from tkinter import Tk
from stockfish import Stockfish
from sys import platform
import tensorflow_chessbot
import display



class CTMaster:
	player = True #True is white False is black
	pos1 = None	
	pos2 = None

	def menu(self):
		while(True):
			print("\n"*100)

			print('''
-------------------------
-------------------------
---Bit's Chess Trainer---
-------------------------
-------------------------

Options:
[1] : Setup Capture Region
[2] : Clear Images
[3] : Best Move Trainer
[4] : Bad Move Trainer
[5] : Exit

			''')
			inp = input("Selection >> ")
			try:
				inp = int(inp)
				if(inp < 1 or inp > 5):
					raise ValueError()
			except Exception as e:
				print("Error: Input was not a valid option")
				continue

			if inp == 1:
				setupCapture()
			elif inp == 2:
				clearImages()
			elif inp == 3:
				if(self.pos1 != None or self.pos2 != None):
					bestMove()
				else:
					print("\n\nPlease Set Up Capture Region Before Using Best Move or Bad Move Trainers")
					input("\n\nPress Enter to Continue")
			elif inp == 4:
				None
			elif inp == 5:
				exit()


	def __init__(self):
		self.menu()

class clearImages:
	def __init__(self):
		dir = "./Captures/"
		os.chdir(dir)

		while(True):

			try:
				print("\n\nAre you sure you want to clear all images in: " + str(os.getcwd()) + "?")
				inp = input("(yes) or (no) >> ")
				if inp == "no":
					print("\n\nClear Images Operation Cancelled")
				elif inp == "yes":
					for f in os.listdir("."):
						if f.endswith(".png"):
							os.remove("." + f)
					print("\n\nCaptures Deleted")
				else:
					raise ValueError()
				break
			except Exception as e:
				print("\n\nError: Invalid option")
			
		os.chdir("..")

class setupCapture(CTMaster):

	def __init__(self):

		while True:
			print("\n"*10)
			print("Press SPACEBAR when mouse is slightly outside the TOP-LEFT of the chess board")
			print("waiting...")
			listener = keyboard.Listener(on_press=self.setPos1)
			listener.start()
			listener.join()

			print("\n\nPosition 1 Set as: x=" + str(self.pos1[0]) +  " y=" + str(self.pos1[1]))

			print("Press SPACEBAR when mouse is slightly outside the BOTTOM-RIGHT of the chess board")
			print("waiting...")

			listener = keyboard.Listener(on_press=self.setPos2)
			listener.start()
			listener.join()
			print("\n\nPosition 2 Set as: x=" + str(self.pos2[0]) +  " y=" + str(self.pos2[1]))

			if(self.pos1.x >= self.pos2.x):
				print("---ERROR---")
				print("First Position should be LEFT of your second position \nInstead found Position 1 " + str(self.pos1.x-self.pos2.x) + " pixels to the right of position 2")
				input("\nPress Enter to Continue...")
				continue
			elif(self.pos1.y >= self.pos2.y):
				print("---ERROR---")
				print("First Position should be ABOVE of your second position \nInstead found Position 1 " + str(self.pos1.y-self.pos2.y) + " pixels below position 2")
				input("\nPress Enter to Continue")
				continue
			else:
				root = Tk()
				root.wait_visibility(root)
				root.resizable(False, False) 
				root.attributes('-type', 'dock')
				root.attributes('-alpha',0.3)
				root.configure(bg="red")
				root.geometry(str(self.pos2.x - self.pos1.x)+ "x" + str(self.pos2.y - self.pos1.y) + "+" + str(self.pos1.x)+ "+" + str(self.pos1.y))
				print("\n\nSelected Region Highlighted")
				input("\n\nPress Enter To Return to Menu")
				root.destroy()
				break

	def setPos1(self, key):
		if key == keyboard.Key.space:
			self.pos1 = pyautogui.position()
			CTMaster.pos1 = pyautogui.position()
			return False

	def setPos2(self, key):
		if key == keyboard.Key.space:
			self.pos2 = pyautogui.position()
			CTMaster.pos2 = pyautogui.position()
			return False
	


class bestMove(CTMaster):
	sf = None
	doFenFlip = False
	fen = None
	def __init__(self):
		if platform == "linux":
			self.sf = Stockfish("./Stockfish/stockfishlinux", parameters={"Threads": 4, "Minimum Thinking Time": 200, "Skill Level":9, "Ponder": True})
		elif platform == "win32":
			self.sf = Stockfish("./Stockfish/stockfishwindows.exe", parameters={"Threads": 4, "Minimum Thinking Time": 200, "Skill Level":9, "Ponder": True} )
		
		listener = keyboard.Listener(on_press=self.keyHandler)
		listener.start()

		im = pyautogui.screenshot(region=(self.pos1.x, self.pos1.y, self.pos2.x-self.pos1.x, self.pos2.y-self.pos1.y))
		im.save("./Captures/analysisCapture.png")
		info = tensorflow_chessbot.main("./Captures/analysisCapture.png")
		
		self.fen = info[0]
		print(self.fen)
		display.start()
		display.update(self.fen)

		listener.join()



	def unflipFEN(self, fen):
		if len(fen) < 71:
			fen = self.lengthenFEN(fen)
		return '/'.join([ r[::-1] for r in fen.split('/') ][::-1])
	
	def shortenFEN(self, fen, player):
		shortened = fen.replace('11111111','8').replace('1111111','7').replace('111111','6').replace('11111','5').replace('1111','4').replace('111','3').replace('11','2')
		return str(shortened) + " " +  str(player) + " - - 0 1"
	
	def lengthenFEN(self, fen):
		return fen.replace('8','11111111').replace('7','1111111') \
            .replace('6','111111').replace('5','11111') \
            .replace('4','1111').replace('3','111').replace('2','11')



	def captureBestMove(self, player, flip=False):
		im = pyautogui.screenshot(region=(self.pos1.x, self.pos1.y, self.pos2.x-self.pos1.x, self.pos2.y-self.pos1.y))
		im.save("./Captures/analysisCapture.png")
		info = tensorflow_chessbot.main("./Captures/analysisCapture.png")
		self.fen = info[0]
		
		if flip == True:
			self.fen = self.unflipFEN(self.fen)

		short = self.shortenFEN(self.fen, player)
		display.update(short)

		print(short)
		self.sf.set_fen_position(short)
		print("Board Recognition Confidence: " + str(info[1]))
		print("Best Move for " +player+ " is: " + str(self.sf.get_best_move()) + "\n\n")

	def keyHandler(self, key):
		if key == keyboard.KeyCode.from_char("w"):
			self.captureBestMove("w", self.doFenFlip)
		
		elif key == keyboard.KeyCode.from_char("b"):
			self.captureBestMove("b", self.doFenFlip)

		elif key == keyboard.KeyCode.from_char("f"):	
			self.doFenFlip = not self.doFenFlip
			print("FEN flip is now: " + str(self.doFenFlip))
			self.fen = self.unflipFEN(self.fen)
			display.update(self.fen)
			print(self.fen)
		
		elif key == keyboard.Key.esc:
			return False

	
			

	# short_fen = shortenFEN(fen)
 #  short_fen = str(short_fen) + " " +  str(pl) + " - - 0 1"


if __name__ == "__main__":
	ct = CTMaster()