# simple-secret-sharing
Simple implementation of Secret Sharing using asymmetric cryptography

[Secret Sharing](https://en.wikipedia.org/wiki/Secret_sharing) can be simply, but inefficiently implemented using [asymmetric cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography).  This approach to Secret Sharing is advantageous because reconstructing the secret from the shares is very straightforward and requires only `gpg` (something sure to be around for quite some time).


### Alternatives

The following are more efficient implementations of Secret Sharing, but require the specific implementation to be available at the time of secret reconstruction.

* http://point-at-infinity.org/ssss/
* http://manpages.ubuntu.com/manpages/disco/en/man7/gfshare.7.html

[Stack Exchange Question 83897](https://security.stackexchange.com/questions/83897/shamirs-secret-sharing-scheme-how-standardised) points out the problems using these to reconstruct a secret and implicity points out the advantages of using a very simple reconstruction process.  The [Key distribution](https://en.wikipedia.org/wiki/Key_distribution) wikipedia entry explicitly points out an advantage of using Secret Sharing with asymmetric cryptography.
