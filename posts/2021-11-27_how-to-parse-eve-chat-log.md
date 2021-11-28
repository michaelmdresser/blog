---
title: How to parse EVE Online chat logs (in Common Lisp)
date: 2021-11-27
---

> If you'd like to skip straight to the details, [click here](#how-to-parse-the-logs)

[EVE Online](https://www.eveonline.com/) has many interesting properties that emerge
from its "sandbox" environment, especially the areas referred to as "nullsec" that have
completely free-for-all PVP combat. Corporations (guilds, in common MMO parlance) form Alliances
in nullsec, control regions of this slice of the in-game world, and perform various
money-making activity there which often benefit (if only in safety) from the Alliance's control
of the area. To keep track of enemy activity in Alliance-controlled space, Alliances usually
have a common intel-sharing chat channel (think something like an IRC channel), where players
post messages like `R1O-GN 3`, indicating that 3 hostile players have been spotten in the
system `R1O-GN`. Players in the Alliance use this information to keep themselves safe by hiding
or to seek out a fight by chasing down the enemies.

EVE conveniently stores chat logs in a file on disk live. These logs can be found on Windows in
the folder `C:\Users\yourusernamehere\Documents\EVE\logs\Chatlogs`. This presents an opportunity
to build tooling around this data, which is available in a convenient text format for out-of-game tools
to consume. Many EVE players have built tools around this data to provide audio alerts and visualizations
of the intel information. For my own education, and for the fun of it, I decided to create something
similar in Common Lisp to suit my personal needs. What follows are some short notes on how to parse
on-disk EVE logs into a usable format in Common Lisp. I hope that it can also help others, as much
of the information is not Lisp-specific.

## How to parse the logs

> Many thanks to [py-eve-chat-mon](https://github.com/andrewpmartinez/py-eve-chat-mon) which I
> referenced heavily when trying to figure out the format of the log file and what regular
> expressions to use for parsing. I also dove through several other 

> Also, please note that I am very far from a Lisp expert. If you have any tips on improving this
> code, give me a shout!

### Read the log file
EVE uses UTF-16LE for chat. In Common Lisp, you can use `UIOP` to read the lines from the
file using the correct format:
```lisp
(uiop:read-file-lines LOGFILE :external-format :utf-16le)
```

### Remove the header
All chat logs come with a header, which I remove with a fairly hacky method that is based on
identifying the dash `-` characters that delimit the header region.
```lisp
(defun line-is-header-dashesp (chat-line)
  (not (not (substringp "-----" chat-line))))

(defun remove-header-from (chat-lines)
  (let* ((first-header-dashes
           (position-if #'line-is-header-dashesp chat-lines))
         (without-first-header-dashes
             (subseq chat-lines (+ first-header-dashes 1)))
         (second-header-dashes
           (position-if #'line-is-header-dashesp without-first-header-dashes))
         (without-second-header-dashes
             (subseq without-first-header-dashes (+ second-header-dashes 1))))
    without-second-header-dashes))
```

### Parse components of the message
To then extract the relevant parts of the message (timestamp, author, message contents),
I use the following (requires [CL-PPRCRE](http://edicl.github.io/cl-ppcre/)):
```lisp
(defparameter *message-parse-regex* "^.*\\[\\s+(.*?)\\s+\\]\\s(.*?)\\s>\\s(.*?)$")
(defun parse-eve-chat-message (message)
  (ppcre:register-groups-bind (timestamp author contents)
      (*message-parse-regex* message)
    ;; Your code here
    ))
```

While I don't think it should be necessary, the first `.*` (right after the `^`) is there because
experimentally it didn't work otherwise. I think it may have something to do with
[py-eve-chat-mon's "chat line delimeter"](https://github.com/andrewpmartinez/py-eve-chat-mon/blob/31f7855abcbbe5de0d985ed9f7a8df54b9c3a635/py_eve_chat_mon/chat_message.py#L29)
of `u"\ufeff"` which it removes from messages.

### Further parse the timestamp
The timestamp can be further parsed, if necessary, with the following:
```lisp
(defparameter *timestamp-parse-regex*
"([0-9][0-9][0-9][0-9])\\.([0-9][0-9])\\.([0-9][0-9]) ([0-9][0-9]):([0-9][0-9]):([0-9][0-9])")

(defun parse-eve-chat-timestamp (timestamp-string)
  (ppcre:register-groups-bind (year month day hour minute second)
      (*timestamp-parse-regex* raw-timestamp)
    ;; Your code here
    ))
```
