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
    clone.querySelector("input[name='tweet_id']").value = tweet.tweet_id;
    clone.querySelector("input[name='user_id'").value = tweet.user_id;
    clone.querySelector("#tweetText").textContent = tweet.tweet_text;
    if (tweet.tweet_image_src != "") {
        clone.querySelector("img").src = `./images/${tweet.tweet_image_src}`;
    } else {
        clone.querySelector("img").remove();
    }
    const createdAt = new Date(parseInt(tweet.tweet_created_at) * 1000);
    clone.querySelector("#tweetCreatedAtDate").textContent = createdAt.toLocaleString();

    const dest = document.querySelector("#tweets");
    const firstChild = dest.firstChild;
    dest.insertBefore(clone, firstChild);
}