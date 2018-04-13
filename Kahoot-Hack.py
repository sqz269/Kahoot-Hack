import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from colorama import init, Fore
from PyQt4 import QtGui, QtCore


def InitMessage():
	init()
	print(Fore.LIGHTGREEN_EX + "MADE BY SQZ")
	print("Written in python")
	print("KAHOOT ANSWER HACK v0.01")
	print("SOFTWARE LICENSE: Attribution 2.0 Generic (CC BY 2.0)")
	print("FORK ME ON GITHUB: https://github.com/sqz269/Kahoot-Hack\n\n" + Fore.RESET)

class Get_Answer(object):


	def __init__(self, quizID, Username, Password, pageLoadTime):
		self.quizID = quizID
		self.Username = Username
		self.Password = Password
		self.SleepTime = int(pageLoadTime)
		super(Get_Answer, self).__init__()


	def Get_QuizPage(self):
		Driver = webdriver.Chrome("chromedriver.exe")
		Driver.get(self.quizURL)
		time.sleep(self.SleepTime)
		username = Driver.find_element_by_id("username-input-field__input")
		password = Driver.find_element_by_id('password-input-field__input')
		username.send_keys(self.Username)
		password.send_keys(self.Password)
		Driver.find_element_by_css_selector('.button').click()
		time.sleep(self.SleepTime)

		if 'login' in Driver.current_url: # check if the user still in the same page
			print("\nLogin failed")
			input("Press Enter To Retry")
			Driver.close()
			os.system('cls')
			main()

		Driver.find_element_by_css_selector('.question-list__group-toggle').click()
		self.soup = BeautifulSoup(Driver.page_source, 'html5lib')
		Driver.close()


	def Get_Question_And_Answer(self):
		global Question_And_Answers
		Question_And_Answers = {}
		All_Questions_RAW = self.soup.findAll('div', {'class': 'question'})
		for items in All_Questions_RAW:
			Get_Question = items.find('div', {'class': 'question-media__text-inner-wrapper'})
			Get_Options = items.findAll('li', {'class': 'choices__choice'})
			Question = items.find('span', {'class': None}).text
			for options in Get_Options:
				Correct_Answer = options.find('div', {'class': 'choices__choice--correct'})
				if Correct_Answer:
					Answer_Shape = options.find('span')
					Shape = str(Answer_Shape)
					print(Question)
					if 'diamond' in Shape:
						Question_And_Answers.update({Question:'diamond'})
						print('diamond')
					elif 'square' in Shape:
						Question_And_Answers.update({Question:'square'})
						print('square')
					elif 'triangle' in Shape:
						Question_And_Answers.update({Question:'triangle'})
						print('triangle')
					elif 'circle' in Shape:
						Question_And_Answers.update({Question:'circle'})
						print('circle')
					break
		

	def Get_Quiz_Info(self):
		Title = self.soup.find('h1', {'class': 'kahoot-title__heading'}).text
		Subtitle = self.soup.find('span', {'class': 'kahoot-type-description'}).text
		Number_Of_Questions = self.soup.find('span', {'class': 'question-list__num-questions'}).text
		Number_Of_Questions = Number_Of_Questions.replace('(', '').replace(')', '')
		print("\nQuiz Title: {}\nQuiz Subtitle: {}\nNumber Of Questions: {}".format(Title, Subtitle, Number_Of_Questions))


	def Get_Quizurl(self):
		self.quizURL = 'https://create.kahoot.it/details/' + self.quizID


class Auto_Player(object):


	def __init__(self, Pin_Number, Username, pageloadtime):
		super(Auto_Player, self).__init__()
		self.Pin_Number = Pin_Number
		self.Username = Username
		self.SleepTime = int(pageloadtime)


	def Enter_Game(self):
		# Get_Answer.Get_QuizPage()
		self.Driver = webdriver.Chrome('chromedriver.exe')
		self.Driver.get('https://www.kahoot.it')
		time.sleep(self.SleepTime)
		Session_Pin = self.Driver.find_element_by_id('inputSession')
		Session_Pin.send_keys(self.Pin_Number)
		self.Driver.find_element_by_css_selector('.btn.join, button').click()
		time.sleep(self.SleepTime)
		Session_Username = self.Driver.find_element_by_css_selector('input.username')
		Session_Username.send_keys(self.Username)
		self.Driver.find_elements_by_class_name('btn')[0].click()

		
	def Sync(self):
		pass


	def Start_Play(self):
		global Question_And_Answers
		Question_Number = 0
		while True:
			if 'gameblock' in self.Driver.current_url:
				# GET answer from the answer dict
				Question = list(Question_And_Answers.keys())[Question_Number]
				Answer = list(Question_And_Answers.values())[Question_Number]
				print('Question: {}\nAnswer: {}\n'.format(Question, Answer))
				self.Driver.switch_to_frame("gameBlockIframe")
				Question_Number += 1
				time.sleep(3)
				triangle = self.Driver.find_element_by_css_selector('.card-button--triangle')
				square = self.Driver.find_element_by_css_selector('.card-button--square')
				diamond = self.Driver.find_element_by_css_selector('.card-button--diamond')
				circle = self.Driver.find_element_by_css_selector('.card-button--circle')
				if 'triangle' in Answer:
					triangle.click()
					print("Clicked Triangle")
					self.Driver.switch_to_default_content()
				elif 'diamond' in Answer:
					diamond.click
					print("Clicked Diamond")
					self.Driver.switch_to_default_content()
				elif 'square' in Answer:
					square.click()
					print("Clicked Square")
					self.Driver.switch_to_default_content()
				elif 'circle' in Answer:
					circle.click()
					print("Clicked circle")
					self.Driver.switch_to_default_content()
				continue


def main():
	InitMessage()
	print("--------------Answer Gathering----------------")
	quizID = input('quizId=')
	kahootUsername = input('kahoot username: ')
	kahootPassword = input('kahoot password: ')
	webpageLoadingTime = input('webpage Loading time: ')
	print("\n--------------Auto Game Play-----------------")
	kahootPlayPin = input('kahoot game pin: ')
	kahootPlayerName = input('kahoot ingame username: ')

	Answer = Get_Answer(quizID, kahootUsername, kahootPassword, webpageLoadingTime)
	Answer.Get_Quizurl()
	Answer.Get_QuizPage()
	Answer.Get_Quiz_Info()
	Answer.Get_Question_And_Answer()

	AutoPlay = Auto_Player(kahootPlayPin, kahootPlayerName, webpageLoadingTime)
	AutoPlay.Enter_Game()
	AutoPlay.Start_Play()
	

main()
