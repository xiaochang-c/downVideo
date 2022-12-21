let urls=[]
let ids=document.getElementsByClassName("_576Tl9nl")
for (let i=0;i<ids.length;i++ ){
    console.log(ids[i])
    ids[i].click()
    url="https://www.douyin.com/video/"+location.href.slice(-19)
    //url="https://www.douyin.com/video/"+location.href.slice(-19)+"\n"

    urls.push(url)
}
console.log(urls.length)

for (let j=0;j<urls.length;j++){
    console.log(urls[j])
}

function saveText(text) {
    const blob = new Blob([text], { type: 'text/plain' });
    const anchor = document.createElement('a');
    anchor.download = 'output.txt';
    anchor.href = window.URL.createObjectURL(blob);
    anchor.click();
}

saveText(urls)
