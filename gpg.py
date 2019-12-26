import gnupg
import keydep
import logging


class GpgKeyDep(keydep.KeyDep):

	def __init__(self, workDir):
		self.gpg = gnupg.GPG(gnupghome=workDir)
		self.gpg.encoding = 'utf-8'

	def generateShares(self, N):
		input_data = self.gpg.gen_key_input(key_type="RSA", key_length=1024, passphrase="")
		
		keys = []
		for _ in range(N):
			key = self.gpg.gen_key(input_data)
			if not key.fingerprint or key.fingerprint == None:
				logging.error("Generation of key failed: %s", key.stderr)
				raise RuntimeError()
			keys.append(key.fingerprint[-8:])
			logging.info("Generated key %s", key.fingerprint)

		return keys

	def encrypt(self, filepath, recipient):
		targetFile = str(filepath) + "." + str(recipient)[-8:] + ".gpg"

		with open(filepath, "rb") as file:
			result = self.gpg.encrypt_file(file, recipient, armor=False, output=targetFile)
			if not result.ok:
				logging.error("Encryption of %s with key %s failed: %s", filepath, recipient, result.status)
				raise RuntimeError()
		logging.info("Encrypted %s with recipient %s into %s", filepath, recipient, targetFile)

		return targetFile

	def exportShares(self, keyIds, targetDirectory):
		files = []
		for key in keyIds:
			ascii_armored_private_key = self.gpg.export_keys(key, True, passphrase="")
			outputFile = targetDirectory + '/' + key + '.asc'
			with open(outputFile, 'w') as f:
				f.write(ascii_armored_private_key)
			logging.info("Exported key %s to %s", key, outputFile)
			files.append(outputFile)

		return files



