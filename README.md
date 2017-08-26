# Edsby XSS Proof-Of-Concept

~~Confirmed to work on Edsby instances with version numbers of at least 17431 and below (also seen as 1492092324).~~
**Update:** This vulnerability has been fixed in a patch rolled out to all Edsby instances as of June 2017, very shortly after disclosure. Many thanks to COreFour for their prompt response to
the issue:)

## Overview

 Edsby's backend does not validate URL metadata passed when posting links, and instead posts the included content straight into the DOM, without validation. Using this, we can effectively post arbitrary HTML into any class feed, which gives us a [persistent XSS vulnerability](https://en.wikipedia.org/wiki/Cross-site_scripting#Persistent).

#### How does it work?

When a user drafts a message that includes one or more links, Edsby calls its own web spider API and attempts to scrape metadata about the webpage so it can generate a kind of URL preview later on, which it appends to the bottom of the post.

However, an issue arises when including this metadata in a message submission. After scraping and formatting,
the link preview JSON (which is attached to the message submission) looks like this. Notice the identical url and href properties:

        {
            "code": 200,
            "description": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.",
            "right": {
                "description": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.",
                "title": "Google"
            },
            "embedstatus": "complete",
            "uuid": 6,
            "title": "Google",
            "url": "https://www.google.com/",
            "href": "https://www.google.com/",
            "type": "link",
            "thumbnail": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png",
            "left": {
                "thumbnail": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png"
            }
        }


  As it turns out, while the href property is used to set the corresponding value in the generated link for the preview, the url
 property is simply placed inside of the `<a>` tag without any kind of validation or escaping whatsoever. So, you can place any html
 you'd like to add to the DOM (including script elements) in here, and it will be rendered by the user's browser. Assuming that all
 of the other properties in this object remain unchanged, it'll still render as a normal link preview. Posts with XSS included are
 indistinguishable from other posts in your class feed (Scary!)

  _**Side note:** I have tested to see if you can post fake links by setting the URL as one value and href as another, but it doesn't seem to work._

#### Why is this bad?
  If you aren't already familiar with the security risks posed by XSS vulnerabilities, you should [familiarize yourself](https://en.wikipedia.org/wiki/Cross-site_scripting#Persistent_attack).

##### Some nasty things a malicious actor could do with this:
  - Steal the current user's session cookies and personal information,
  - Perform _any_ action on Edsby as the current user: student,  teacher, or administrator,
  - Make a self-replicating worm (like [Samy](https://en.wikipedia.org/wiki/Samy_(computer_worm))) that spreads throughout your entire instance,
  - Or really anything else.


#### Mitigation:

  ~~As of right now, there is no way to prevent the submission of malicious payloads, or
  for Edsby users to protect themselves from their reciept. You'll have to sit tight and
  wait for CoreFour to update the backend so it validates inputs properly.~~

  **Update:** Has been patched as of early June!

#### Configuration:
   This document includes a Proof-Of-Concept which demonstrates the exploitation process. This section
  details how it should be configured.

      dry_run:
          Set to False to actually send the payload

      host:
          Edsby instance hostname

      username:
          Your Edsby username

      password:
          Your edsby password

      classNID:
          NID of the class you want to post the payload in.
          Must be a class you have permissions to post in.

      fake_url:
          Link that the message should appear as. Will be scraped to generate the link preview.

      payload:
            Default is a manually triggered payload, so the user must click the link for it to run.

            If an automatically running payload were desired, use similar to the following:

            '</a><a href="https://www.google.com">nothing illegitimate here<img onerror="alert(\'Whoops.\')"/></a><a>'
