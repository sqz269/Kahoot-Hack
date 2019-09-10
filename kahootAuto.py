from configparser import ConfigParser
from logger import init_logging
from logging import getLogger
import time

from selenium import webdriver, common

init_logging()

class GetAnswers():


	def __init__(self, quizID):
		self.logger = getLogger("bot")

		self.quizID = quizID
		self.logger.info("Got Quiz id: {}".format(quizID))

		self.initWebDriver()

		self.CVT_INT_SHAPE = {
			3: "TRIANGLE",
			5: "DIAMOND",
			7: "CIRCLE",
			9: "SQUARE"
		}


	def initWebDriver(self):
		self.logger.info("Initalizing Automated Browser Session")
		try:
			self.driver = webdriver.Chrome("chromedriver_76.exe") # TODO: Allow user to select chromedriver version
		except common.exceptions.WebDriverException as err:
			self.logger.error("ERROR: {}".format(err))
			if ("binary" in str(err)):
				self.logger.error("Failed to locate Chrome binary.")

		self.logger.info("Automated Browser Session Initalized")


	def getQuizAnswers(self) -> dict:
		self.logger.info("Entering Get Quiz Answers")
		answerDict = {}
		questions = self.driver.find_elements_by_class_name("question-list__item")
		self.logger.info("Found {} Questions".format(len(questions)))
		self.logger.info("Parsing Questions")
		for question in questions:
			questionTextSplit = question.text.split("\n")
			questionAnswerIndex = questionTextSplit.index("This is a correct answer") - 1
			questionAnswer = questionTextSplit[questionAnswerIndex]
			questionNumber = int(questionTextSplit[0].split("-")[0])
			answerDict.update({questionNumber: self.CVT_INT_SHAPE.get(questionAnswerIndex)})
			self.logger.debug({questionNumber: self.CVT_INT_SHAPE.get(questionAnswerIndex)})
		self.logger.info("Got All Answers")
		self.logger.info("Destroying Automated Browser Session")
		self.driver.quit()
		return answerDict


	def getQuizPage(self):
		quizAnswersURL = "https://create.kahoot.it/details/{}".format(self.quizID)
		self.logger.info("Constructed Quiz Answer URL: {}".format(quizAnswersURL))
		self.driver.get(quizAnswersURL)
		self.logger.info("Clicking on Show Answers Button")
		time.sleep(1)  # Pause and make javascript do the work
		showAnswersBtn = self.driver.find_element_by_class_name("question-list__group-toggle")
		showAnswersBtn.click()


class AutoPlay():


	def __init__(self, gamePin, username, answerDelay, answerKey):
		self.gamePin = gamePin
		self.username = username
		self.answerDelay = answerDelay
		self.answerDict = answerKey
		self.logger = getLogger("bot")
		self.initWebDriver()

		self.CVT_SHAPE_CLASSNAME = {
			"SQUARE": "bDfINc",
			"CIRCLE": "eYFENK",
			"TRIANGLE": "eRSCLD",
			"DIAMOND": "fabXZJ"
		}


	def initWebDriver(self):
		self.logger.info("Initalizing Automated Browser Session")
		try:
			self.driver = webdriver.Chrome("chromedriver_76.exe") # TODO: Allow user to select chromedriver version
		except common.exceptions.WebDriverException as err:
			self.logger.error("ERROR: {}".format(err))
			if ("binary" in str(err)):
				self.logger.error("Failed to locate Chrome binary.")

		self.logger.info("Automated Browser Session Initalized")


	def enterGame(self):
		gameURL = "https://kahoot.it/"
		self.driver.get(gameURL)
		self.logger.info("Entering Game PIN")
		self.driver.find_element_by_id("game-input").send_keys(self.gamePin)
		self.driver.find_element_by_class_name("enter-button__EnterButton-sc-1o9b9va-0").click()
		self.logger.info("Pressing Enter Button")
		time.sleep(1)
		self.driver.find_element_by_id("nickname").send_keys(self.username)
		self.logger.info("Entering Username")
		self.driver.find_element_by_class_name("enter-button__EnterButton-sc-1o9b9va-0").click()
		self.logger.info("Entering Game")


	def doGameLoop(self):
		while True:
			if (self.driver.current_url == "https://kahoot.it/v2/gameblock"):
				questionNumberText = self.driver.find_element_by_class_name("question-top-bar__QuestionNumber-sc-1pwisow-3").text
				self.logger.debug("Question number raw text form: {}".format(questionNumberText))
				questionNumber = int(questionNumberText.split("of")[0])
				self.logger.info("Current Question is: {} | Answer Shape: {}".format(questionNumber, self.answerDict.get(questionNumber)))
				time.sleep(self.answerDelay)
				self.driver.find_element_by_class_name(self.CVT_SHAPE_CLASSNAME.get(self.answerDict.get(questionNumber))).click()
			else:
				self.logger.debug("Not In Question stage. waiting")
				time.sleep(0.5)
		self.logger.info("Destorying Session")
		self.driver.quit()


def startGameFromIni():
	cfg = ConfigParser()
	cfg.read("kahoot.ini")
	mainCfg = cfg["config"]
	uuid = mainCfg["QuizUUID"]
	pin = mainCfg["GamePIN"]
	username = mainCfg["Username"]
	delay = float(mainCfg["AnswerDelay"])
	AP = AutoPlay(pin, username, delay, getQuizAnswers(uuid))
	AP.enterGame()
	AP.doGameLoop()


def getQuizAnswers(quizUUID):
	GA = GetAnswers(quizUUID)
	GA.getQuizPage()
	return GA.getQuizAnswers()


def getUserInput():
	quizUUID = input("Game UUID: ")

	gamePin = input("Game Pin: ")
	username = input("Username: ")
	delay = float(input("Answer Delay: "))
	AP = AutoPlay("195226", "Test", 0.01, getQuizAnswers(quizUUID))
	AP.enterGame()
	AP.doGameLoop()


def main():
	try:
		with open("kahoot.ini") as file: pass
		use = input("Kahoot.ini configuration found. use it? (y/n)")
		if (use.lower() == "y"):
			startGameFromIni()
		else:
			getUserInput()
	except:
		print("Unable to find kahoot.ini; defaulting to user input;")
		getUserInput()


main()
