"use strict";

async function logIn() {
    event.preventDefault();
    const path = window.location.pathname;
    const secondSlash = path.indexOf("/", 1);
    const language = secondSlash === 3 ? path.substring(1, secondSlash) : "en";

    const form = document.querySelector("#loginForm");
    const userEmail = form.user_email;
    const emailHint = document.querySelector("#emailHint");
    const userPassword = form.user_password;
    const passwordHint = document.querySelector("#passwordHint");
    const emailStatus = userEmail.validity;
    const passwordStatus = userPassword.validity; 

    if (emailStatus.valueMissing) {
        emailHint.style.display = "block";
        emailHint.textContent = "Please enter your e-mail.";
        userPassword.value = "";
        return false;
    } else if (emailStatus.typeMismatch || emailStatus.patternMismatch) {
        emailHint.textContent = "Please enter a valid e-mail.";
        emailHint.style.display = "block";
        userPassword.value = "";
        return false;
    } else {
        emailHint.textContent = "";
        emailHint.style.display = "none";
    }

    if (passwordStatus.valueMissing) {
        passwordHint.textContent = "Please enter your password.";
        passwordHint.style.display = "block";
        return false;
    } else if (passwordStatus.patternMismatch) {
        passwordHint.textContent = "Password must be at least 8 characters containing at least 1 uppercase letter, 1 lowercase letter and 1 number.";
        passwordHint.style.display = "block";
        userPassword.value = "";
        return false;
    } else {
        passwordHint.textContent = "";
        passwordHint.style.display = "none";
    }
    
    const connection = await fetch(`/${language}/login`, {
        method: "POST",
        body: new FormData(form)
    });
    const response = await connection.json();
    console.log(response);
    if (!connection.ok) {
        const info = response.info.toLowerCase();
        if (info.includes("email")) {
            emailHint.style.display = "block";
            emailHint.textContent = response.info;
            passwordHint.style.display = "none";
            passwordHint.textContent = "";
        } else {
            passwordHint.style.display = "block";
            passwordHint.textContent = response.info;
            emailHint.style.display = "none";
            emailHint.textContent = "";
        }
        userPassword.value = "";
    } else {
        location.href = './explore'
    }
}

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
    clone.querySelector("form").setAttribute("id", `tweet_${tweet.tweet_id}`);
    clone.querySelector("#userName").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
    clone.querySelector("#userHandle").textContent = `@${tweet.user_handle}`;
    clone.querySelector("#userImage").src = `./images/${tweet.user_image_src}`;
    clone.querySelector("input[name='tweet_id']").value = tweet.tweet_id;
    clone.querySelector("input[name='user_id'").value = tweet.user_id;
    clone.querySelector("#tweetText").textContent = tweet.tweet_text;
    if (tweet.tweet_image_src != "") {
        clone.getElementById("#tweetImage").src = `./images/${tweet.tweet_image_src}`;
    } else {
        clone.getElementById("#tweetImage").remove();
    }
    const createdAt = new Date(parseInt(tweet.tweet_created_at) * 1000);
    clone.querySelector("#tweetCreatedAtDate").textContent = createdAt.toLocaleString();

    const dest = document.querySelector("#tweets");
    const firstChild = dest.firstChild;
    dest.insertBefore(clone, firstChild);
}

function toggleUpdateTweet() {
    const form = event.target.form;

    const temp = document.querySelector("#updateTweetTemp");
    const dest = document.querySelector("#updateTweet");
    dest.innerHTML = "";
    const clone = temp.cloneNode(true).content;

    clone.querySelector("[name='tweet_id']").value = form.querySelector("[name='tweet_id']").value;
    clone.querySelector("textarea").value = form.querySelector("#tweetText").textContent;
    
    if (!form.querySelector(".tweetImage")) {
        clone.querySelector("button.delete").remove();
        clone.querySelector("img").remove();
        clone.querySelector("input[type='hidden'][name='tweet_image_src']").remove();
        clone.querySelector("input[type='file']").setAttribute("name", "tweet_image_src");
    } else {
        const src = form.querySelector(".tweetImage").src;
        const imageSrc = src.substring(src.lastIndexOf("/") + 1);
        clone.querySelector("img").src = src;
        clone.querySelector("input[type='file']").style.display = "none";
        clone.querySelector("input[type='hidden'][name='tweet_image_src']").value = imageSrc;
        clone.querySelector("button.delete").addEventListener("click", removeImage);
    }

    dest.appendChild(clone);
    dest.style.display = "block";
    
    function removeImage() {
        dest.querySelector("button.delete").removeEventListener("click", removeImage);
        dest.querySelector("img").remove();
        dest.querySelector("input[type='file']").style.display = "block";
        dest.querySelector("input[type='file']").setAttribute("name", "tweet_image_src");
        dest.querySelector("input[type='hidden'][name='tweet_image_src']").value = "";
        dest.querySelector("button.delete").remove();
    }
}

async function updateTweet() {
    const form = event.target.form;
    console.log(form);
    const tweetId = form.tweet_id.value;

    const connection = await fetch(`/tweet/${tweetId}`, {
        method: "PUT",
        body: new FormData(form)
    });

    const response = await connection.json();

    const updateTweet = document.querySelector("#updateTweet");

    if (!connection.ok) {
        const errorMessage = response.info.replace("_", " ");
        updateTweet.querySelector(".hint").textContent = errorMessage;
        updateTweet.querySelector(".hint").style.display = "block";
        return
    }

    updateTweet.innerHTML = "";
    updateTweet.style.display = "none";

    const tweet = document.querySelector(`#tweet_${response.tweet_id}`);
    const tweetText = tweet.querySelector("#tweetText");
    const tweetImage = tweet.querySelector(".tweetImage");
    tweet.querySelector("#tweetText").textContent = response.tweet_text;
    if (response.tweet_image_src === "" && tweetImage) {
        tweetImage.remove();
    }
    if (response.tweet_image_src !== "" && !tweetImage) {
        const img = document.createElement("img");
        img.classList.add("tweetImage");
        img.src = `./images/${response.tweet_image_src}`;
        tweetText.after(img);
    }
    if (response.tweet_image_src !== "" && tweetImage) {
        tweetImage.src = `./images/${response.tweet_image_src}`;
    }
}

async function deleteTweet() {
    const form = event.target.form;
    const tweetId = form.tweet_id.value;

    const connection = await fetch(`/tweet/${tweetId}`, {
        method: "DELETE",
        body: new FormData(form)
    });

    console.log(connection);
    const response = await connection.json();
    if (!connection.ok) {
        return
    }
    document.querySelector(`#tweet_${tweetId}`).remove();
}