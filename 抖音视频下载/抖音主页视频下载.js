function saveText(text) {
    const blob = new Blob([text], { type: 'text/plain' });
    const anchor = document.createElement('a');
    anchor.download = 'output.txt';
    anchor.href = window.URL.createObjectURL(blob);
    anchor.click();
}

const urls = [];
const videos = document.getElementsByClassName('B3AsdZT9 chmb2GX8');
for (let i=0; i<videos.length; i++){
    urls.push(videos[i].href)
    //console.log(videos[i].href)
}

saveText(urls)


