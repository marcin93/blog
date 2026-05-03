# README

Page based on [Pelican](https://getpelican.com/) (static site generator) and Theme: [Flex](https://github.com/alexandrevicenzi/Flex) 

---

### Install and Test

1. Download or clone repo
2. Enter the folder
3. ```python -m pip install pelican``` or ```python -m pip install --upgrade pelican```
4. ```pelican-quickstart```
5. ```pelican -r -l``` <- will start pelican and reload on changes
6. Place articles under ```contetnt/``` 
7. Run content generation: ```pelican content```
8. Pages generated and ready to be published are located under: ```output/```

Plugins for **css** optimization have also been used and instead of 70KB! css we have 23KB
- postcss-cli
- autoprefixer
- cssnano
- @fullhuman/postcss-purgecss

Access via: [http://localhost:8000](http://localhost:8000)

---

### UX Experience

For better user experience, the [zooom.js] library has been added [zooom.js](https://github.com/tomik23/zooom.js)
To the photo which we want to be enlarged should be added class `zooom`
Example of use:
`![Bitbucket screen](/blog/images/bugfix123-bug_remove_extra_padding.png "Bitbucket screen"){: class="zooom"}`

---

### Copyright and license

It is under [the MIT license](/LICENSE).