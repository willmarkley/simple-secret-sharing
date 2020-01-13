#!/usr/bin/env python3.7
'''
usage: simpleSecretSharing.py <pathToSecret> <N> <k> <pathToNewOutputDir>

simpleSecretSharing implements simple Secret Sharing using asymmetric cryptography

Parameters:
	pathToSecret (str): absolute path to the secret file (<10000 bytes)
	N (int): number of shares (<7)
	k (int): number of shares to reconstruct secret (<4)
	pathToNewOutputDir (str): absolute path to the output directory.  Must not already exist
'''

import docopt
import gpg
import itertools
import logging
import os
import pathlib
import stat
import shutil
import sys


def simpleSecretSharing(pathToSecret, N, k, pathToNewOutputDir):
	'''
	simpleSecretSharing implements simple Secret Sharing using asymmetric cryptography
	
	Args:
		pathToSecret (str): absolute path to the secret file (<10000 bytes)
		N (int): number of shares (<7)
		k (int): number of shares to reconstruct secret (<4)
		pathToNewOutputDir (str): absolute path to the output directory.  Must not already exist
	
	Returns:
		A list of the files created, both encryptedSecrets and secretShares
	'''
	
	## validate input
	if not os.path.isabs(pathToSecret) or not os.path.exists(pathToSecret) or not os.path.isfile(pathToSecret) or not os.path.getsize(pathToSecret) < 10000:
		logging.error("pathToSecret %s is invalid", str(pathToSecret))
		raise RuntimeError()

	if not isinstance(N, int) or not N < 7 or not N > 0:
		logging.error("N %s is invalid", str(N))
		raise RuntimeError()

	if not isinstance(k, int) or not k < 4 or not k > 0:
		logging.error("k %s is invalid", str(k))
		raise RuntimeError()

	if not os.path.isabs(pathToNewOutputDir) or os.path.exists(pathToNewOutputDir):
		logging.error("pathToNewOutputDir %s is invalid", str(pathToNewOutputDir))
		raise RuntimeError()

	## setup
	pathWorkDir = pathlib.Path(pathToNewOutputDir) / 'tmp'
	pathWorkDir.mkdir(parents=True)
	os.chmod(pathWorkDir, stat.S_IRWXU)
	workDir = str(pathWorkDir)

	pathSecretSharesDir = pathlib.Path(pathToNewOutputDir) / 'secretShares'
	pathSecretSharesDir.mkdir()
	secretSharesDir = str(pathSecretSharesDir)

	pathEncryptedSecretsDir = pathlib.Path(pathToNewOutputDir) / 'encryptedSecrets'
	pathEncryptedSecretsDir.mkdir()
	encryptedSecretsDir = str(pathEncryptedSecretsDir)

	secretBasename = os.path.basename(pathToSecret)
	shutil.copy(pathToSecret, encryptedSecretsDir)
	cleanup = []
	cleanup.append(encryptedSecretsDir + "/" + secretBasename)

	keydep = gpg.GpgKeyDep(workDir)
	
	## generate all of the shares (keys) in WORK_DIR
	shares = keydep.generateShares(N)
	
	## determine all of the encrypted secrets to generate
	combinations = list(itertools.combinations(shares, k))
	logging.info("Combinations: %s", combinations)

	files = []
	for combo in combinations:
		files.append(encryptedSecretsDir + "/" + secretBasename + "." + '.gpg.'.join(combo) + '.gpg')
		logging.info("To generate:    %s", files[-1])

	## encrypt the secret with caching
	for combo in combinations:
		filename = encryptedSecretsDir + "/" + secretBasename
		for share in combo:
			logging.info("Encrypting secret with Share (%s) in combo (%s)", share, combo)
			targetFilename = filename + "." + str(share)[-8:] + ".gpg"

			if os.path.exists(targetFilename):
				logging.info("Encrypted file has already been created: %s", targetFilename)
				filename = targetFilename
				continue

			filename = keydep.encrypt(filename, share)
			if filename not in files:
				cleanup.append(filename)

	## export
	files.extend(keydep.exportShares(shares, secretSharesDir))

	## cleanup
	for file in cleanup:
		os.remove(file)
	shutil.rmtree(workDir)

	return sorted(files)



if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout,level=logging.INFO,format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s - %(message)s')
	arguments = docopt.docopt(__doc__)
	logging.info("simpleSecretSharing %s", ' '.join(sys.argv))


	simpleSecretSharing(arguments['<pathToSecret>'], int(arguments['<N>']), int(arguments['<k>']), arguments['<pathToNewOutputDir>'])


