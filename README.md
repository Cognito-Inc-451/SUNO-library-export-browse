# SUNO-library-export-browse
Export your Suno library and locally browse your prompts &amp; songs

## First
Open your [Suno Library](https://suno.com) and right click on the first/top-most song -> Inspect

In dev tools go to the console and paste the script below.

Let it scroll the library's pages until the last item. The console will say DONE in the end.
```JavaScript
(async () => {

  const scroller =
    document.querySelector('.clip-browser-list-scroller');

  const songs = new Map();

  function collect() {

    document.querySelectorAll('.clip-row').forEach(row => {

      const a = row.querySelector('a.hover\\:underline');

      if (!a) return;

      const title = a.textContent?.trim() || '';
      const link = a.href || '';

      const prompt =
        row.querySelector('.css-1j82g8w.edgsit113')
          ?.textContent?.trim() || '';

      songs.set(link, {
        title,
        link,
        prompt
      });
    });

    console.log(
      'songs:',
      songs.size,
      'scroll:',
      scroller.scrollTop
    );
  }

  let last = 0;
  let stuck = 0;

  while (stuck < 30) {

    collect();

    scroller.scrollTop += 1500;

    await new Promise(r => setTimeout(r, 1000));

    if (songs.size === last) {
      stuck++;
    } else {
      stuck = 0;
      last = songs.size;
    }
  }

  window.sunoExport = [...songs.values()];

  // Copy pretty-printed JSON to clipboard
  copy(JSON.stringify(window.sunoExport, null, 2));

  console.log(
    'DONE',
    window.sunoExport.length,
    '- copied to clipboard'
  );

})();
```

## Next
- Open Notepad
- Paste result from clipboard
- Save as suno.json
- Make sure generate.py is in the same location
- Execute generate.py and then open the new index.html : done. Enjoy !
<img width="819" height="89" alt="image" src="https://github.com/user-attachments/assets/8386c6c9-8866-426d-b01b-3c31b7e60639" />
