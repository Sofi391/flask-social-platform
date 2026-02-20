/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
document.addEventListener("DOMContentLoaded", () => {
    const postsContainer = document.getElementById("posts-container"); // <-- add this

    // ================= Navbar Scroll =================
    let scrollPos = 0;
    const mainNav = document.getElementById("mainNav");
    if (mainNav) {
        const headerHeight = mainNav.clientHeight;
        window.addEventListener("scroll", function() {
            const currentTop = document.body.getBoundingClientRect().top * -1;
            if (currentTop < scrollPos) {
                if (currentTop > 0 && mainNav.classList.contains("is-fixed")) {
                    mainNav.classList.add("is-visible");
                } else {
                    mainNav.classList.remove("is-visible", "is-fixed");
                }
            } else {
                mainNav.classList.remove("is-visible");
                if (currentTop > headerHeight && !mainNav.classList.contains("is-fixed")) {
                    mainNav.classList.add("is-fixed");
                }
            }
            scrollPos = currentTop;
        });
    }

    // ================= Like Button (AJAX) =================
    document.addEventListener("submit", function(e) {
        const form = e.target.closest(".like-form");
        if (!form) return;
        e.preventDefault();

        const postId = form.dataset.postId;
        const likeButton = form.querySelector(".like-btn");
        const likeCount = form.querySelector(".like-count");

        fetch(`/post_like/${postId}`, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            likeCount.textContent = data.likes_count;
            likeButton.style.color = data.liked ? "red" : "#adb5bd";
        })
        .catch(err => console.error("Error liking post:", err));
    });

    // ================= Liked-by Popup Toggle =================
    if (postsContainer) {
        postsContainer.addEventListener("click", e => {
            const toggle = e.target.closest(".liked-by-toggle");
            if (!toggle) return;
            e.preventDefault();

            const popup = toggle.closest("form").querySelector(".liked-by-list");

            document.querySelectorAll(".liked-by-list").forEach(p => {
                if (p !== popup) p.style.display = "none";
            });

            popup.style.display = popup.style.display === "block" ? "none" : "block";
        });
    }

    // Close popups when clicking outside
    document.addEventListener("click", e => {
        document.querySelectorAll(".liked-by-list").forEach(popup => {
            const toggle = popup.closest("form").querySelector(".liked-by-toggle");
            if (!popup.contains(e.target) && toggle && !toggle.contains(e.target)) {
                popup.style.display = "none";
            }
        });
    });
});


