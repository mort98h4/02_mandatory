async function tweet() {
    const form = event.target.form;
    console.log(form.tweet_text.value);

    const connection = await fetch("/tweet", {
        method: "POST",
        body: new FormData(form)
    });

    if (!connection.ok) {
        alert("Could not tweet");
        return
    }

    const tweet = await connection.json();
    console.log(tweet);

    const temp = document.querySelector("#tweetTemp");
    const clone = temp.cloneNode(true).content;
    clone.querySelector("#tweetId").textContent = tweet.tweet_id;
    clone.querySelector("#tweetText").textContent = tweet.tweet_text;

    const dest = document.querySelector("#tweets");
    const firstChild = dest.firstChild;
    dest.insertBefore(clone, firstChild);
}