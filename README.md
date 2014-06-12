managchan-downloader
====================

A simple script to download manga chapters from Mangachan.ru or Yaoichan.ru.

Just add a link to chapter page on the command line.

Example:

  mangachan-dl http://mangachan.ru/online/27510-occupation-angel-shokugyou-tenshi_v1_ch1.html

You can specify folder with -f and number of files to skip with -s (but
this doesn't work well with several chapters).

You can also set up a maximal timeout after each image via -t argument
(in seconds). The real timeout will be a random number from 0 to maximal
timeout. The default is 1.5 seconds.

You can specify several URLs; then, several chapters will be downloaded
(please keep in mind this works bad with -s and -f arguments: they will
be applied to all the chapters at the same time!).

Will probably work for Hentaichan.ru too, but it haven’t been tested.
