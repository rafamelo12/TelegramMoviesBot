import requests
import telegram
import random

class MoviesBot():
	readyStrings = ['Ready to help!']
	whatStrings = ['Yes?', 'Hmmm?', 'What do you want?']
	yesStrings = ['I can do that.', 'Be happy to.', 'Sure!']
	noStrings = ["I can't do that.", "You stupid?", "Not right...", "Don't think that I can do that..."]
	# pissedStrings = ['Stop harassing me!', 'I\'m on my break, won\'t do anything now!']

	options = ["search", "recommend"]

	helpMessage = """ Hello, fellow user! I'm the Good Guy Movies Bot!
    
	Here is what I can do now:
	/search Give me a series/movie title and I'll get information about it for you!

	"""
	default_url = 'http://www.omdbapi.com/?t=TITLE&plot=short&tomatoes=true&r=json'

	def __init__(self, token = "TOKEN"):
		self.token = token
		self.bot = telegram.Bot(token)
		try:
			self.lastUpdate = self.bot.getUpdates()[-1].update_id
		except IndexError:
			self.lastUpdate = None

	def startBot(self):
		while True:
			for update in self.bot.getUpdates(offset = self.lastUpdate, timeout=10):
				chat_id = update.message.chat_id
				message = update.message.text

				if message:
					if "@GoodMoviesBot" in message:
						botid = "@GoodMoviesBot"
						message = message[:message.find(botid)] + message[message.find(botid) + len(botid):]
					if(message.startswith('/')):
						command, _, arguments = message.partition(' ')
						if command == '/start':
							self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.readyStrings[0])
						elif command == '/help':
							self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.helpMessage)
						elif command[1:] in MoviesBot.options:
							noArgument = False
							if arguments == '':
								noArgument = True

							rand = random.randint(0, len(MoviesBot.yesStrings)-1)
							self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.yesStrings[rand])

							if command == '/search':
								if noArgument:
									self.bot.sendMessage(chat_id=chat_id, text="Give me something to search.")
								else:
									msg, poster = self.searchMovie(arguments)
									self.bot.sendPhoto(chat_id=chat_id, photo=poster)
									self.bot.sendMessage(chat_id=chat_id, text=msg)


					else:
						rand = random.randint(0, len(MoviesBot.whatStrings)-1)
						self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.whatStrings[rand])

					self.lastUpdate = update.update_id + 1
	
	def searchMovie(self, title):
		title = title.replace(" ", "+")
		usr_request = MoviesBot.default_url.replace("TITLE", title)
		movie = requests.get(usr_request).json()
		message = movie['Title'] + "\n" + 'Genre(s): ' + movie['Genre'] + "\n" + 'IMDB Rating: ' + movie['imdbRating'] + "\n" + 'Rotten Tomatoes Rating: ' + movie['tomatoMeter'] + "\n" + 'Rotten Tomatoes User Rating: ' + movie['tomatoUserMeter'] + "\n" + 'Movie Plot: ' + movie['Plot']
		poster = movie['Poster']
		return message, poster


def main():
    # print "Oxi"
    moviesbot = MoviesBot()
    moviesbot.startBot()

if __name__ == '__main__':
    main()