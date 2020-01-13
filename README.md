# simple-secret-sharing
Simple implementation of Secret Sharing using asymmetric cryptography

[Secret Sharing](https://en.wikipedia.org/wiki/Secret_sharing) can be simply, but inefficiently implemented using [asymmetric cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography).  This approach to Secret Sharing is advantageous because reconstructing the secret from the shares is very straightforward and requires only `gpg` (something sure to be around for quite some time).



## Usage Examples

### Shell

```
usage: simpleSecretSharing.py <pathToSecret> <N> <k> <pathToNewOutputDir>

simpleSecretSharing implements simple Secret Sharing using asymmetric cryptography

Parameters:
	pathToSecret (str): absolute path to the secret file (<10000 bytes)
	N (int): number of shares (<7)
	k (int): number of shares to reconstruct secret (<4)
	pathToNewOutputDir (str): absolute path to the output directory.  Must not already exist
```

Example:
```
python simpleSecretSharing.py /home/secret.txt 3 2 /home/output
```
produces
```
/home/output/encryptedSecrets:
secret.txt.698823C9.gpg.B63A00BB.gpg
secret.txt.9A46E5FF.gpg.698823C9.gpg
secret.txt.9A46E5FF.gpg.B63A00BB.gpg

/home/output/secretShares:
698823C9.asc
9A46E5FF.asc
B63A00BB.asc
```
The number of secretShares is N.  The number of encryptedSecrets is the [bionomial coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient).

To reconstruct the secret:
```
# Given possession of 698823C9.asc and 9A46E5FF.asc and the encryptedSecrets directory
gpg --homedir /home/tmpgpg --import 698823C9.asc
gpg --homedir /home/tmpgpg --import 9A46E5FF.asc

gpg --homedir /home/tmpgpg --decrypt --output secret.txt.9A46E5FF.gpg secret.txt.9A46E5FF.gpg.698823C9.gpg
gpg --homedir /home/tmpgpg --decrypt --output secret.txt secret.txt.9A46E5FF.gpg
cat secret.txt
```


### Python

```
import simpleSecretSharing

pathToSecret = str('/home/secret.txt')
N = 3
k = 2
pathToNewOutputDir = str('/home/output')


outputFiles = simpleSecretSharing.simpleSecretSharing(pathToSecret, N, k, pathToNewOutputDir)

print(outputFiles)
```

produces

```
['/home/output/encryptedSecrets/secret.txt.698823C9.gpg.B63A00BB.gpg',
 '/home/output/encryptedSecrets/secret.txt.9A46E5FF.gpg.698823C9.gpg',
 '/home/output/encryptedSecrets/secret.txt.9A46E5FF.gpg.B63A00BB.gpg',
 '/home/output/secretShares/698823C9.asc',
 '/home/output/secretShares/9A46E5FF.asc',
 '/home/output/secretShares/B63A00BB.asc']
```

## Testing

```
pip install pytest
pytest test_simpleSecretSharing.py
```


## Alternatives

The following are more efficient implementations of Secret Sharing, but require the specific implementation to be available at the time of secret reconstruction.

* http://point-at-infinity.org/ssss/
* http://manpages.ubuntu.com/manpages/disco/en/man7/gfshare.7.html

[Stack Exchange Question 83897](https://security.stackexchange.com/questions/83897/shamirs-secret-sharing-scheme-how-standardised) points out the problems using these to reconstruct a secret and implicity points out the advantages of using a very simple reconstruction process.  The [Key distribution](https://en.wikipedia.org/wiki/Key_distribution) wikipedia entry explicitly points out an advantage of using Secret Sharing with asymmetric cryptography.


## Alternative Implementations

This implementation uses asymmetric cryptography.  It is possible to accomplish the same functionality using symmetric cryptography.  If symmetric cryptography were used, openssl would generate the keys instead of gnupg.

```
openssl rand 128 > symkey.key
openssl enc -e -aes-256-cbc -pbkdf2 -a -in secret.txt -out secret.txt.symkey.enc -pass file:symkey.key

openssl enc -d -aes-256-cbc -pbkdf2 -a -in secret.txt.symkey.enc -out secret.txt -pass file:symkey.key
```
