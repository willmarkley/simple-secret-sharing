import gnupg
import itertools
import logging
import math
import os
import pytest
import random
import simpleSecretSharing


SECRET_DATA = "test secret\n"

## Obtained from https://bitbucket.org/vinay.sajip/python-gnupg/src/default/test_secring.gpg
SECRET_GPG_KEY = '''-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=GaZF
-----END PGP PRIVATE KEY BLOCK-----
'''

ENCRYPTED_SECRET_DATA = '''-----BEGIN PGP MESSAGE-----

hQIOAzoz3Ee4krqfEAgAk38HIET8v0XNXFY3LJ/X6qIEdAV6PQSLGBicmeZBQ8ZH
twPYlBLsvZnWRUJVb4VhIBrFH20YHVkrfhixmCwec2NVIY4MScON3ckPqz80SHdu
kMj7T2x4x86Olioi8qruvtY0tEpFFyOABvkoD1xH2HcdL+xXr57CYO+bAXcskXkQ
4+YYPzSPccnT6sfR1k5ufgcuAkB7hK4YW50JwniVMOPzYyhitd6hx7Gi5nNQYRMn
g31Zgva8/6XzvE2PIi+Io1dyu46U46zInDzwlI3xHIysQ02AwqqeA1/8OvHFVhAo
NhjH9MfIeXCRyzpUoX8aOgwe7KovNc9wO49iKe69BQf/aBl/ixCPJk/IZpidxCZr
RtduU+uBCINQxMqFJltUFB4PXYsH6reYey9VRQpk1JaW12PCATnkk+5QTulCXLbB
LB6wdrg7YVCP7Q0fmdP9zXUvOwESP1n8EoUHEqJL95rDjACMm2cNC49wQMAgxYa4
XcXgK3GTIcdenenGd0M1GtNwWTip3IBlUFKl5T//vJbULiudO9yKjHxTMRjC47dE
bUrUBLc3301oaD15F1gcWhWo/5WeFTSbEYGOt90EZJraizWxhfUH72HHNqOPjQ+I
AKJHZqTU+K9hNBmQLFhLb5upuGMD5+v6Cd3bwEzZ3MOpakLT06TJH8e4OdN4UoYK
N9JNAXsvFZjl/kYY7m+42ioAKLsp/8W8PBrH04XtSjz8CvaRNDObL3Rp/8Mfd3q8
6QllkD2Nq1+sQwcMpfD/vd/YmabCAcwGiWephH8Cshc=
=wpiO
-----END PGP MESSAGE-----
'''


def act_assert_simpleSecretSharing(secret, pathToSecret, N, k, pathToNewOutputDir, tmp_path):
	secretBasename = os.path.basename(pathToSecret)
	encryptedSecretsDir = pathToNewOutputDir + '/encryptedSecrets'
	secretSharesDir = pathToNewOutputDir + '/secretShares'

	## Act
	outputFiles = simpleSecretSharing.simpleSecretSharing(pathToSecret, N, k, pathToNewOutputDir)

	## Assert
	logging.info("[TEST] outputFiles: %s", outputFiles)

	### Confirm the correct number of `outputFiles` in each category
	outputEncryptedSecrets = set(filter(lambda k: 'encryptedSecrets' in k, outputFiles))
	assert len(outputEncryptedSecrets) == math.comb(N, k) # bionomial coefficient
	outputShareFiles       = set(filter(lambda k: 'secretShares' in k, outputFiles))
	assert len(outputShareFiles) == N

	### Confirm the files in `outputFiles` actually exist on the system
	assert set(os.listdir(pathToNewOutputDir)) == {'encryptedSecrets', 'secretShares'}
	assert set(map((encryptedSecretsDir + '/{0}').format, os.listdir(encryptedSecretsDir))) == outputEncryptedSecrets
	assert set(map((secretSharesDir + '/{0}').format, os.listdir(secretSharesDir)))         == outputShareFiles

	### Randomly select k keys and try to decrypt an encryptedSecrets.  Ensure result is equal to original secret
	path = tmp_path / 'tmpgpg'
	path.mkdir()
	gpg = gnupg.GPG(gnupghome=str(path))
	gpg.encoding = 'utf-8'

	keyFiles = random.sample(outputShareFiles, k)
	logging.info("[TEST] keyFiles: %s", keyFiles)
	keyIds = []
	for key in keyFiles:
		with open(key, 'r') as f:
			gpg.import_keys(f.read())
		keyIds.append(os.path.splitext(os.path.basename(key))[0])

	possibleFiles = []
	for combo in list(itertools.permutations(keyIds)):
		possibleFiles.append(encryptedSecretsDir + '/' + secretBasename + '.' + '.gpg.'.join(combo) + '.gpg')

	encryptedSecret = (set(possibleFiles) & set(outputEncryptedSecrets)).pop()
	logging.info("[TEST] encryptedSecret: %s", encryptedSecret)
	for i in range(k):
		targetFile = encryptedSecret[:-13]
		with open(encryptedSecret, "rb") as file:	
			gpg.decrypt_file(file, output=targetFile)
		encryptedSecret = targetFile

	assert encryptedSecret == (pathToNewOutputDir + '/encryptedSecrets/' + secretBasename)
	content = ""
	with open(encryptedSecret, 'r') as f:
		content = f.read()
		logging.info("[TEST] read secret: %s", content)
		assert secret == content

	if os.path.splitext(secretBasename)[-1] == '.asc':
		gpg.import_keys(content)
		decryptedSecret = gpg.decrypt(ENCRYPTED_SECRET_DATA)
		logging.info("[TEST] decrypted secret data: %s", decryptedSecret)
		assert SECRET_DATA == str(decryptedSecret)


def test_simpleSecretSharing_3_2(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / 'secret.txt')
	with open(pathToSecret, 'w') as f:
		f.write(SECRET_DATA)
	N = 3
	k = 2
	pathToNewOutputDir = str(tmp_path / 'output')

	act_assert_simpleSecretSharing(SECRET_DATA, pathToSecret, N, k, pathToNewOutputDir, tmp_path)

def test_simpleSecretSharing_5_2(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / 'secret.txt')
	with open(pathToSecret, 'w') as f:
		f.write(SECRET_DATA)
	N = 5
	k = 2
	pathToNewOutputDir = str(tmp_path / 'output')

	act_assert_simpleSecretSharing(SECRET_DATA, pathToSecret, N, k, pathToNewOutputDir, tmp_path)

def test_simpleSecretSharing_6_3(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / 'secret.txt')
	with open(pathToSecret, 'w') as f:
		f.write(SECRET_DATA)
	N = 6
	k = 3
	pathToNewOutputDir = str(tmp_path / 'output')

	act_assert_simpleSecretSharing(SECRET_DATA, pathToSecret, N, k, pathToNewOutputDir, tmp_path)

def test_simpleSecretSharing_5_2_keyAsSecret(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / '4C7798F2.asc')
	with open(pathToSecret, 'w') as f:
		f.write(SECRET_GPG_KEY)
	N = 5
	k = 2
	pathToNewOutputDir = str(tmp_path / 'output')

	act_assert_simpleSecretSharing(SECRET_GPG_KEY, pathToSecret, N, k, pathToNewOutputDir, tmp_path)
	

def test_simpleSecretSharing_6_3_keyAsSecret(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / '4C7798F2.asc')
	with open(pathToSecret, 'w') as f:
		f.write(SECRET_GPG_KEY)
	N = 6
	k = 3
	pathToNewOutputDir = str(tmp_path / 'output')

	act_assert_simpleSecretSharing(SECRET_GPG_KEY, pathToSecret, N, k, pathToNewOutputDir, tmp_path)


def test_simpleSecretSharing_3_2_bad_args(caplog, tmp_path):
	caplog.set_level(logging.INFO)

	## Arrange
	pathToSecret = str(tmp_path / 'secret.txt')
	N = 3
	k = 2
	pathToNewOutputDir = str(tmp_path / 'output')

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing("output/myfile", N, k, pathToNewOutputDir)
	assert caplog.text.endswith("pathToSecret output/myfile is invalid\n")
	caplog.clear()

	largeSecret = str(tmp_path / 'largeSecret.txt')
	with open(largeSecret, 'wb') as f:
		f.write(os.urandom(11000))
	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(largeSecret, N, k, pathToNewOutputDir)
	assert caplog.text.endswith("pathToSecret " + largeSecret + " is invalid\n")
	caplog.clear()

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, N, k, pathToNewOutputDir)
	assert caplog.text.endswith("pathToSecret " + pathToSecret + " is invalid\n")
	caplog.clear()

	with open(pathToSecret, 'w') as f:
		f.write(SECRET_DATA)

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, 7, k, pathToNewOutputDir)
	assert caplog.text.endswith("N 7 is invalid\n")
	caplog.clear()

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, 0, k, pathToNewOutputDir)
	assert caplog.text.endswith("N 0 is invalid\n")
	caplog.clear()

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, N, 4, pathToNewOutputDir)
	assert caplog.text.endswith("k 4 is invalid\n")
	caplog.clear()

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, N, 0, pathToNewOutputDir)
	assert caplog.text.endswith("k 0 is invalid\n")
	caplog.clear()

	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, N, k, "output/mydir")
	assert caplog.text.endswith("pathToNewOutputDir output/mydir is invalid\n")

	pathObjToNewOutputDir = tmp_path / 'output'
	pathObjToNewOutputDir.mkdir()
	with pytest.raises(RuntimeError):
		simpleSecretSharing.simpleSecretSharing(pathToSecret, N, k, pathToNewOutputDir)
	assert caplog.text.endswith("pathToNewOutputDir " + pathToNewOutputDir + " is invalid\n")
	caplog.clear()
