# testCLSrest
### Python test script for the Cloudy Logic Studios REST API

Welcome to the Python test script for the CLS REST API. The CLS REST API server code ([available on GitHub here](https://github.com/kenlowrie/clsrestapi)) is hosted on [api.cloudylogic.com](http://api.cloudylogic.com), and although it has a manual testing facility built into the main page using AJAX, the Python script goes much further in shaking out the API. If you have questions, or would like to provide feedback and/or to report a bug, feel free to contact the author, Ken Lowrie, at [www.kenlowrie.com](http://www.kenlowrie.com/).

### Attributions

Attributions here...

#### Installing this app to your server

To run this script, you'll need a current version of Python 2.7 installed on your machine. You'll also need the Requests Python module installed on your machine; find all the details for installing Requests [here](http://docs.python-requests.org/en/master/user/install/). Other than that, you should be set. That's it! If you run into any problems, feel free to contact me for assistance.

#### Why a command line test app?

In order to make sure that the CLS REST API is returning the correct objects to potential clients, I needed an automated way to validate it, as well as test any future changes to make sure it doesn't break expected functionality. Whether or not I can achieve the latter is yet to be seen, but I figured it was a worthy cause.

So, I created this Python script to automatically do that, and as a bonus, if you're wanting to see one way of consuming JSON inside Python, this app might be a good starting place for you. Although I don't have every conceivable data type in my API, there's enough that you should be able to figure it out by looking at what I've already done.

#### testCLSrest usage

The usage for the script is as follows:

    python testCLSrest.py [host | .] [api_name | \*]

If you don't pass any parameters, it will assume that you have the server code running on your local development server on port 8000. So, http://localhost:8000 is where it will be sending the JSON requests. I'm assuming this because I use [Gulp](http://gulpjs.com/) as my automated build environment, and the [gulp-connect-php](https://www.npmjs.com/package/gulp-connect-php) module, and that is the default it uses. If you use something else or a different default, change the port and/or URL in your copy.

If you don't have it (the CLS REST API Server code) running locally, you can use the live server at [http://api.cloudylogic.com](http://api.cloudylogic.com). Do that by specifying: 

    python testCLSrest.py http://api.cloudylogic.com

Be default, it will run all the tests. If you want to run a single test, specify the name of that test. Supported tests are:

    versions - Returns the versions of a specific (or all) API. 
    about-us - Returns a text description of what Cloudy Logic Studios does.
    contact-info - Returns contact information for Cloudy Logic.
    reels - Returns information about demo reels including a streaming URL.
    our-work - Returns information about select video projects that showcase the company.

So, for example, to test the reels API, you would run:

    python testCLSrest.py http://api.cloudylogic.com reels
    python testCLSrest.py . reels

The first line would run the request against the live server, and the second one would run it against your local server.

That's about it, there's not a lot to this script, at least right now. I may be developing some additional test scripts in other languages, and if so, they will become part of this same repository.

#### Additional Information

For additional information, take a look at the comments in the source code! I tried to add plenty of useful comments in there to help you understand the app.

Of course you may also want to take a look at the repository for the CLS REST API server code, which is located [here](https://github.com/kenlowrie/clsrestapi) on [GitHub](https://github.com/). It is written in PHP, so you'll need at least a basic understanding of that in order to decipher it. I've also added lots of comments to it as well, so you might find answers to some of your questions by reviewing that. The README.md file that's part of that repository also provides plenty of documentation on the API.

#### Summary

This concludes the documentation on the testCLSrest.py Python test script.

