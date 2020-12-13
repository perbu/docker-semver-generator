# Generate semver tags for docker images


Given we have:
 * `0.1.0`
 * `0.2.0`
 * `0.3.0`
 
 And we build `0.2.1` - what tags should be applied?
 
 This tools tries to generate those tags. It'll spit out:
  `0.2` and `0.2.1`. It will not touch the `0` tag as this should still point to `0.3.0`.
 