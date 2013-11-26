from Tkinter import *
import ctypes
import time


class FullScreenApp():
	def __init__(self, parent, images, solutions):
		# time constants
		self.waiting_screen_time = 3000 # in s
		self.question_display_time = 3000 # in ms
		
		# marker definitions
		self.waiting_screen_start = 1
		self.question_screen_start = 2
		self.keyboard_event = 3
		self.correct_answer = 4
		self.false_answer = 5
		
		# parallel port adress
		self.pport_address = 0xE010
		
		# store images/solutions
		self.images = images
		self.solutions = solutions
		self.curr_questionID = -1
		
		# set up initial window
		self.bg_color = "dark slate gray"
		self.parent = parent
		self.parent.geometry("{0}x{1}+0+0".format(parent.winfo_screenwidth(), parent.winfo_screenheight()))
		self.main_container = Frame(parent, background=self.bg_color)
		self.main_container.pack(side="top", fill="both", expand=True)
		
		self.startScreen()

	def startScreen(self):
		# prepare containers
		self.top_frame = Frame(self.main_container, background=self.bg_color)
		self.bottom_frame = Frame(self.main_container, background=self.bg_color)
		self.top_frame.pack(side="top", fill="both", expand=True)
		self.bottom_frame.pack(side="bottom", fill="y", expand=True)
		
		# add start button
		self.startButton = Button(self.bottom_frame, text="Start", command=lambda: self.waitingScreen(0))
		self.startButton.pack()
		
	def answerScreen(self, afterID):
		self.clearScreen()
		
		# set marker
		self.setMarker(self.keyboard_event)
		
		# stop the automatic question screen skip
		self.parent.after_cancel(afterID)
		
		# prepare containers
		self.top_frame = Frame(self.main_container, background=self.bg_color)
		self.bottom_frame = Frame(self.main_container, background=self.bg_color)
		self.top_frame.pack(side="top", fill="both", expand=True)
		self.bottom_frame.pack(side="bottom", fill="y", expand=True)
		
		# show question image
		self.photo = PhotoImage(file=self.images[self.curr_questionID])
		scr_width, scr_height = self.main_container.winfo_screenwidth(), self.main_container.winfo_screenheight()
		img_width, img_height = self.photo.width(), self.photo.height()
		img_posX = (scr_width-img_width)/2
		self.image_canvas = Canvas(self.top_frame, width=img_width, height=img_height,
								bg=self.bg_color, bd=0, highlightthickness=0)
		self.image_canvas.create_image(img_posX,100,anchor=NW, image=self.photo)
		self.image_canvas.pack(side="top", fill="both", expand=True)
		
		# show text label
		self.textLabel = Label(self.bottom_frame, text="Please select your answer",
							font=("Helvetica", 15), background=self.bg_color)
		self.textLabel.pack(side="left", expand=False)
		
		# show answer buttons: one selection for each answer possibility plus one "I don't know" option.
		self.answer_container = Frame(self.bottom_frame, background=self.bg_color)
		self.answer_container.pack(side="left",  padx=20)#, fill="both", expand=True)
		number_of_answers = self.solutions[self.curr_questionID][0]
		correct_answer = self.solutions[self.curr_questionID][1]
		self.answer = IntVar()
		self.answerOptions = []
		for i in range(number_of_answers+1):
			if i < number_of_answers:
				answerText = "Answer " + str(i+1)
				self.answerOptions.append(Radiobutton(self.answer_container, text=answerText, highlightthickness=0,
					variable=self.answer, bg=self.bg_color, bd=0, value=i+1, padx=3, 
					command=self.checkAnswer))
			else:
				answerText = "I don't know"
				self.answerOptions.append(Radiobutton(self.answer_container, text=answerText, highlightthickness=0,
					variable=self.answer, bg=self.bg_color, bd=0, value=-1, padx=3,
					command=self.checkAnswer))
				
			self.answerOptions[i].pack(expand=False)
		
	def waitingScreen(self, nextQuestionID=0):
		self.clearScreen()
		
		# increment to next question
		if (self.curr_questionID+1) < len(self.images):
			self.curr_questionID += 1
		else:
			quit()
		
		# prepare containers
		self.top_frame = Frame(self.main_container, background=self.bg_color)
		self.bottom_frame = Frame(self.main_container, background=self.bg_color)
		self.top_frame.pack(side="top", fill="both", expand=True)
		self.bottom_frame.pack(side="bottom", fill="both", expand=True)
		
		# show text label
		self.textLabel = Label(self.bottom_frame, text="The next Question will appear shortly.",
							font=("Helvetica", 30), background=self.bg_color)
		self.textLabel.pack(expand="False")
		
		# set marker
		self.setMarker(self.waiting_screen_start)
		
		self.parent.after(self.waiting_screen_time, self.questionScreen)
		
	def feedbackScreen(self):
		self.clearScreen()
			
		# prepare containers
		self.top_frame = Frame(self.main_container, background=self.bg_color)
		self.bottom_frame = Frame(self.main_container, background=self.bg_color)
		self.top_frame.pack(side="top", fill="both", expand=True)
		self.bottom_frame.pack(side="bottom", fill="both", expand=True)
		
		# show text label
		self.textLabel = Label(self.bottom_frame, text="The next Question will appear shortly.",
							font=("Helvetica", 30), background=self.bg_color)
		self.textLabel.pack(expand="False")
		
		self.startButton = Button(self.bottom_frame, text="Next Question", command=self.questionScreen)
#		self.startButton.pack()
	
	def questionScreen(self):
		self.clearScreen()
			
		# prepare containers
		self.top_frame = Frame(self.main_container, background=self.bg_color)
		self.bottom_frame = Frame(self.main_container, background=self.bg_color)
		self.top_frame.pack(side="top", fill="both", expand=True)
		self.bottom_frame.pack(side="bottom", fill="both", expand=True)
		
		# show question image
		self.photo = PhotoImage(file=self.images[self.curr_questionID])
		scr_width, scr_height = self.main_container.winfo_screenwidth(), self.main_container.winfo_screenheight()
		img_width, img_height = self.photo.width(), self.photo.height()
		img_posX = (scr_width-img_width)/2
		self.image_canvas = Canvas(self.top_frame, width=img_width, height=img_height, background=self.bg_color, bd=-2, highlightthickness=0)
		self.image_canvas.create_image(img_posX,100,anchor=NW, image=self.photo)
		self.image_canvas.pack(side="top", fill="both", expand=True)
		
		# show question text label
		self.textLabel = Label(self.bottom_frame, text="If you know the solution, press any button", font=("Helvetica", 30), background=self.bg_color)
		self.textLabel.pack(expand="False")
		
		# initiate auto skip
		afterID = self.parent.after(self.question_display_time, self.waitingScreen)
		
		# add keyboard event
		self.top_frame.focus_set()
		self.top_frame.bind("<Key>", lambda event: self.answerScreen(afterID))
		
		# set marker
		self.setMarker(self.question_screen_start)
		
	def clearScreen(self):
		for child in self.main_container.winfo_children():
			child.destroy()
		self.main_container.pack(side="top", fill="both", expand="True")
		
	def setMarker(self, marker):
#		ctypes.windll.inpout32.Out32(self.pport_address, marker)
#		time.sleep(0.005)
#		ctypes.windll.inpout32.Out32(self.pport_address, 0)
		print "Set marker: ", marker
		
	def checkAnswer(self):
		if (self.answer.get() == self.solutions[self.curr_questionID][1]):
			# corrent answer
			print "Correct, the solution was answer", self.answer.get()
			self.setMarker(self.correct_answer)
		else:
			# false answer
			self.setMarker(self.false_answer)
			print "False, you chose answer", self.answer.get(), ", but the correct solution was answer", self.solutions[self.curr_questionID][1]
			
		self.waitingScreen()

def main():
	images, solutions = loadQuestions('questions.txt')
	root = Tk()
	app = FullScreenApp(root, images, solutions)
	root.mainloop()

def loadQuestions(filename):
	images = []
	solutions = []
	with open(filename) as lines:
		for line in lines:
			img, num_answers, solution = line.split(' ')
			images.append(img)
			solutions.append((int(num_answers), int(solution)))
	return images, solutions

if __name__ == '__main__':
	main()  
