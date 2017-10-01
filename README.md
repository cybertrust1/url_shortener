No frills URL shortener (no database & running on AWS)
======================================================

What? Yet another URL shortener? This is so 2009 (which in tech years is a few decades)... I can almost hear you say. But wait, this is a little different. This one has no datastore requirements (no DBs, no text files etc.) and it is hosted on AWS.

I wanted something that would be easily testable on the internet, something that wouldn't need constant maintenance and that would live free on its own for the coming years. Because isn't it a little sad when a URL shortener dies, you can't access shortened links and stuff...

So serverless application using AWS' Lambda (which comfortably fits in free tier usage) and API Gateway (which is not in free tier list but costs next to nothing) fit the bill very well. They also recently announced about [SAM (Serverless Application Model)](https://aws.amazon.com/blogs/compute/introducing-simplified-serverless-application-deplyoment-and-management/) which I had not tested yet. This was the perfect opportunity (also, bit operations, yay!).

How does it work?
=================

I use East Asian characters to encode URLs. This means for example the character 𪛖 encodes two ASCII letters at the same time. There's also a simple heuristics to encode the protocol in a single bit. The compression (if it can be called compression :)) is not too big but it is a fun thing to work on. The resulting characters are less than half the original URLs.

I'm using [code points from 0x20000 to 0x2a6d6](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs#CJK_Unified_Ideographs_Extension_F) which gives me a little over 42k characters. I can probably try to use emoji characters and characters from other languages to compress a bit more, but I settled on my original range because it seemed that my laptop had fonts to print these while other characters was not a sure thing.

Shortcomings
============

* Only [ASCII characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters) are mapped to East Asian ones, which means URLs containing non-ASCII characters are not supported (see [Guardian article on unicode domain names to see how this could actually pose security risk](https://www.theguardian.com/technology/2017/apr/19/phishing-url-trick-hackers)).

* The shortened URL is not as short as services which use a DB to map shortened hash values to URLs. A data store also enables those services to offer custom shortened URLs.

* Only http and https is supported. This is a design decision as I am using a single bit to encode 'http[s]?://' part.

Requirements
============

For prod run, only Python 3. That's all :)

For running tests locally, you need py.test installed:

    pip install -r requirements_test.txt

And you can run all tests with:
    
    py.test

Test it
======

Test locally using curl and jq:

    curl -X POST https://s3f6v3cd4c.execute-api.eu-west-1.amazonaws.com/Prod/shorten_url -d '{"url": "http://www.helloworld.com"}' | jq '.'
    {
        "url": "𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭"
    }

Then visit [https://s3f6v3cd4c.execute-api.eu-west-1.amazonaws.com/Prod/𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭](https://s3f6v3cd4c.execute-api.eu-west-1.amazonaws.com/Prod/𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭) on your browser.

Deployment
==========

Add your credentials into .aws/config or .aws/credentials under a profile. Create a bucket to hold your uploaded lambda functions, such as `my-bucket` using aws-cli or AWS Console.

Run the following to create a complete cloudformation file which includes the code URI:

    aws --profile my_profile cloudformation package --template-file cloudformation.yml --output-template-file cloudformation_with_codeuri.yml --s3-bucket my-bucket

You will notice the new `cloudformation_with_codeuri.yml` file which is created. You can then deploy:

    aws --profile my_profile --region eu-west-1 cloudformation deploy --template-file cloudformation_with_codeuri.yml --stack-name url-shortener --capabilities CAPABILITY_IAM

Et, voila!

Notes
=====

Printable characters and those displayable on your screen are two very different things. Characters other than the control characters are generally printable. There are some exceptions such as space character which is printable, but for our purposes not very useful in a short URL. Even if a character is printable, you might see a question mark if you do not have the fonts installed. 

    import unicodedata
    unicodedata.category(' ')  # prints 'Zs'
    unicodedata.category('\t') # prints 'Cc'

[Character categories](https://en.wikipedia.org/wiki/Unicode_character_property#General_Category) that start with 'C' are control characters.

TO DO?
======

One could in theory achieve a shorter URLs by compressing it before encoding it. [Redis author antirez has a nice project compressing short text using some heuristics](https://github.com/antirez/smaz).

Another improvement could come from utilizing vast number of other characters in different languages. [Wikipedia page on UTF8](https://en.wikipedia.org/wiki/UTF-8#Description) gives hints as to how the 4 byte representation could be used to encode ASCII.

I am using raw cloudformation to deploy (well, with SAM transformation) and pure python for the lambdas at the moment but a further abstraction would simplify things a lot more. In particular [chalice](http://chalice.readthedocs.io/en/latest/) looks very promising. [Apex](http://apex.run/) and [Serverless](https://serverless.com/) are other two frameworks that are a bit more extensive and up for heavy-lifting. Note that with SAM, [API Gateway is the simple proxy for lambda](http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-simple-proxy-for-lambda-input-format).
