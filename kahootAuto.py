from configparser import ConfigParser
from logger import init_logging
from logging import getLogger
import time

from selenium import webdriver, common

init_logging()

class GetAnswers():


	def __init__(self, quizID, pageLoadTime):
		self.logger = getLogger("bot")

		self.quizID = quizID
		self.logger.info("Got Quiz id: {}".format(quizID))

		self.initWebDriver()

		self.pageLoadTime = pageLoadTime

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
			self.logger.critical("FAILED TO START AUTOMATED BROWSER SESSION; UNABLE TO CONTINUE\nPress Enter to exit")
			input(); raise SystemExit(1);

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
		self.logger.info("Webpage Load complete; Wait constant amt({}s) for Js to load".format(self.pageLoadTime))
		time.sleep(self.pageLoadTime)  # Pause and make javascript do the work
		showAnswersBtn = self.driver.find_element_by_class_name("question-list__group-toggle")
		showAnswersBtn.click()


class AutoPlay():


	def __init__(self, gamePin, username, answerDelay, answerKey, pageLoadTime):
		self.gamePin = gamePin
		self.username = username
		self.answerDelay = answerDelay
		self.answerDict = answerKey
		self.pageLoadTime = pageLoadTime
		self.logger = getLogger("bot")
		self.logger.warning("Answer Delay is set to {}s".format(answerDelay))
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
			self.logger.critical("FAILED TO START AUTOMATED BROWSER SESSION; UNABLE TO CONTINUE\nPress Enter to exit")
			input(); raise SystemExit(1);

		self.logger.info("Automated Browser Session Initalized")


	def enterGame(self):
		gameURL = "https://kahoot.it/"
		self.driver.get(gameURL)
		self.logger.info("Entering Game PIN")
		self.driver.find_element_by_id("game-input").send_keys(self.gamePin)
		self.driver.find_element_by_class_name("enter-button__EnterButton-sc-1o9b9va-0").click()
		self.logger.info("Pressing Enter Button")
		self.logger.info("Webpage Load complete; Wait constant amt({}s) for Js to load".format(self.pageLoadTime))
		time.sleep(self.pageLoadTime)
		self.driver.find_element_by_id("nickname").send_keys(self.username)
		self.logger.info("Entering Username")
		self.driver.find_element_by_class_name("enter-button__EnterButton-sc-1o9b9va-0").click()
		self.logger.info("Entering Game")


	def doGameLoop(self):
		while True:
			if (self.driver.current_url == "https://kahoot.it/v2/gameblock"):
				try:
					questionNumberText = self.driver.find_element_by_class_name("question-top-bar__QuestionNumber-sc-1pwisow-3").text
					self.logger.debug("Question number raw text form: {}".format(questionNumberText))
					questionNumber = int(questionNumberText.split("of")[0])
					self.logger.info("Current Question is: {} | Answer Shape: {}".format(questionNumber, self.answerDict.get(questionNumber)))
					time.sleep(self.answerDelay)
					self.driver.find_element_by_class_name(self.CVT_SHAPE_CLASSNAME.get(self.answerDict.get(questionNumber))).click()
				except Exception as e:
					self.logger.exception("Failed to answer question number: {}; Supposed Answer: {}. Execution will continue".format(questionNumber, self.answerDict.get(questionNumber)))
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
	pageLoadDelay = float(mainCfg["pgLoadDelay"])
	AP = AutoPlay(pin, username, delay, getQuizAnswers(uuid, pageLoadDelay), pageLoadDelay)
	AP.enterGame()
	AP.doGameLoop()


def getQuizAnswers(quizUUID, loadDelay):
	GA = GetAnswers(quizUUID, loadDelay)
	GA.getQuizPage()
	return GA.getQuizAnswers()


def getUserInput():
	quizUUID = input("Game UUID: ")
	gamePin = input("Game Pin: ")
	username = input("Username: ")
	delay = float(input("Answer Delay: "))
	pgLoadDelay = float(input("Click Element delay after page load: "))
	AP = AutoPlay(gamePin, username, delay, getQuizAnswers(quizUUID, pgLoadDelay), pgLoadDelay)
	AP.enterGame()
	AP.doGameLoop()


def main():
	try:
		with open("kahoot.ini"): pass
		use = input("Kahoot.ini configuration found. use it? (y/n)")
		if (use.lower() == "y"):
			startGameFromIni()
		else:
			getUserInput()
	except (FileNotFoundError, PermissionError):
		print("Unable to find kahoot.ini; defaulting to user input;")
		getUserInput()


main()
