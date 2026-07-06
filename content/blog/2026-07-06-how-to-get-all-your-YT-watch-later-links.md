Title: How to get all your YT watch later links? 
Date: 2026.07.06
Tags: automation, js, script, yt, watch-later
Slug: get-yt-watch-later

1. Go to: [https://www.youtube.com/playlist?list=WL](https://www.youtube.com/playlist?list=WL) - when logged into YT account
2. Scroll to bottom
3. Open Developer tools ('F12' OR 'Ctrl + Shift + I'), then tab Console
4. Paste:

```js
copy([...document.querySelectorAll('a#video-title')]
.map(a => 'https://www.youtube.com' + a.getAttribute('href'))
.join('\n'));
```

<ol start="5">
<li>All links are now in your clipboard
  <ol>
  <li>Paste them in any text editor</li>
  </ol>
</li>
<li> 🎉 Profit</li>
</ol> 
