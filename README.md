# Generate semver tags for docker images

Semver is nice. The somewhat tricky part is allowing a service to be pinned to a specific MAJOR version 
and then tagging your released docker images accordingly.
 
Given we have the following tags in our repo:
 * `0.1.0`
 * `0.2.0`
 * `0.3.0`
 
And we then build `0.2.1` - what tags should be applied?
 
This tools tries to generate those tags. It'll spit out:
  `0.2` and `0.2.1`. It will not touch the `0` tag as this should still point to `0.3.0`.


## Usage
Find a way to get a hold of your current tags. 

 ```shell script
 $ cat EXISTING_TAGS | python3 semver-tag.py 0.2.1 
 ```
Complete:
```
echo "0.1.0
0.2.0
0.3.0" | python3 semver-tag.py 0.2.1
0.2.1 0.2
```
I'm using this to in the scripts that apply tags.

You'll need to integrate this with your registry somehow.

Note that this tool hasn't been given much testing. However, as I found nothing like it I thought it might make
sense to publish it. File and issue if you have any comments.

