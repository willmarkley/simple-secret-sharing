import abc


class KeyDep(abc.ABC):
	@abc.abstractmethod
	def generateShares(self, N):
		pass

	@abc.abstractmethod
	def encrypt(self, filepath, recipient):
		pass

	@abc.abstractmethod
	def exportShares(self, keyIds, targetDirectory):
		pass