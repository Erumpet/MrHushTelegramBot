import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open

# MrHush's telegram authentication token
TOKEN = '341016958:AAFm44_Qjo5Z1cZGT375_mhnCdvizGAMad4'

'''
def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)
	print(msg['from'])

	if content_type == 'text':
		bot.sendMessage(chat_id, msg['text'])
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
while 1:
	time.sleep(10);

'''
class MessageCounter(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(MessageCounter, self).__init__(*args, **kwargs)
		self._count = {}
		self._alert = {}

	def on_chat_message(self, msg):
		# Extract meta data
		content_type, chat_type, chat_id = telepot.glance(msg)
		from_block = msg['from']
		user_id = from_block['id']		
		user_first = from_block['first_name']

		# Count messages
		if user_id in self._count:
			self._count[user_id] += 1
		else:
			self._count[user_id] = 1
			self._alert[user_id] = True

		# Check if excessive shitposting is occurring
		# First give a warning
		if user_first == 'Sean' and msg['text'] == 'sucky sucky, Ching pong ping':
			self.sender.sendMessage('*sucks Sean\'s little teeny tiny ding dong*', disable_notification = True)
			self.sender.sendMessage('Mistah gimme five dollah!', disable_notification = True)

		if self._count[user_id] >= 7 and self._alert[user_id]:
			self.sender.sendMessage('Hey ' + user_first + ', slow your roll kid, you\'re shitposting over the legal limit.', disable_notification = True)
			self._alert[user_id] = False

		# Start deleting messages
		if self._count[user_id] >= 8 and chat_type == 'supergroup':
			msg_id = telepot.message_identifier(msg)
			self.bot.deleteMessage(msg_id)

		# Ban
		if self._count[user_id] >= 15 and chat_type == 'supergroup':
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


'''
8450 okinawa st sacremrrnto 95828
bt collins army reserve training facility
'''




















