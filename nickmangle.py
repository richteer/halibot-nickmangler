from halibot import HalFilter

class NickMangleFilter(HalFilter):

	# TODO: Expand mangling support with custom logic
	def mangle(self, s):
		return s[0] + '.' + s[1:] if len(s) > 1 else s


	def filter(self, msg):
		# Look for target agents to mangle
		for a in msg.target.split("/"):
			agent = self._hal.objects.agents.get(a)
			if not a:
				continue
			# TODO: Better way to filter the supported agents pls
			if agent.__class__.__name__ != "IrcAgent":
				continue # break instead? should we support/expect agent chaining?

			# Restrict nick scope to target channel
			ch = agent.client.channels.get(msg.target.split("/")[-1], None)
			if not ch:
				continue

			# TODO: This can probably be optimized
			for u in ch.get("users", []):
				msg.body = msg.body.replace(u, self.mangle(u))

		return msg
