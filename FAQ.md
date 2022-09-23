# FAQ

**Why can't we get rid of all the files under `/usr/share/doc` to save even more space?**

Due to legal constraints. Coinboot images already exclude all documentation like man-pages to save space. What we have to keep are copyright notices under `/usr/share/doc`. Because Coinboot distributes software under several Open source licences in a binary form. Coinboot aligns in this topic with the polices of Debian: [Copyright considerations](https://www.debian.org/doc/debian-policy/ch-archive.html#copyright-considerations).  
The good news: these copyright notices are highly compressible data stored in the images and plugin archives as well in the Zstd compressed RAM drive on the workers nodes in a highly compressed state. For instance the 4.8 MB uncompressed data under `/usr/share/doc/` are compressed to 272 KB so a reduction in size by around 95% takes place.
