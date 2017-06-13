import sys
import time
import telepot
from collections import deque
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open

# MrHush's telegram authentication token
TIMEOUT = 35
TOKEN = ''
with open(sys.argv[1], 'r') as f:
    TOKEN = f.readline().strip()

class MessageCounter(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(MessageCounter, self).__init__(*args, **kwargs)
		self._messages = {}
		self._alert = {}

	def on_chat_message(self, msg):
		# Extract message data
		content_type, chat_type, chat_id = telepot.glance(msg)
		from_block = msg['from']
		user_id = from_block['id']		
		user_first = from_block['first_name']
		time = msg['date']

		# Track message
		if user_id in self._messages:
			self._messages[user_id].append(time)
		else:
			self._messages[user_id] = deque([time])
			self._alert[user_id] = True

		# Remove stale messages
		while (time - self._messages[user_id][0]) > TIMEOUT:
			self._messages[user_id].popleft()

		# Top quality Sean meme
		if user_first == 'Sean' and msg['text'] == 'sucky sucky, Ching pong ping':
			self.sender.sendMessage('*sucks Sean\'s little teeny tiny ding dong*', disable_notification = True)
			self.sender.sendMessage('Mistah gimme five dollah!', disable_notification = True)

		# Check if excessive shitposting is occurring

		# First give a warning
		if len(self._messages[user_id]) >= 7 and self._alert[user_id]:
			self.sender.sendMessage('Hey ' + user_first + ', slow your roll kid, you\'re shitposting over the legal limit.', disable_notification = True)
			self._alert[user_id] = False

		# Start deleting messages
		if len(self._messages[user_id]) >= 8 and chat_type == 'supergroup':
			msg_id = telepot.message_identifier(msg)
			self.bot.deleteMessage(msg_id)

		# Ban
		if len(self._messages[user_id]) >= 15 and chat_type == 'supergroup':
			self.bot.kickChatMember(chat_id, user_id)
			self.sender.sendMessage('Banned.', disable_notification = True)


# Initialize bot
bot = telepot.DelegatorBot(TOKEN, [
	pave_event_space()(
		per_chat_id(), create_open, MessageCounter, timeout=35),
	])
MessageLoop(bot).run_as_thread()
while 1:
	time.sleep(15)


