document.addEventListener("DOMContentLoaded", function() {
    var avatar = document.querySelector(".nav_avatar");
    var dropdown = document.querySelector(".avatar_dropdown");

    // Xử lý sự kiện click vào avatar
    avatar.addEventListener("click", function(event) {
        event.stopPropagation(); // Ngăn chặn sự kiện click lan ra ngoài
        // Kiểm tra trạng thái hiển thị của dropdown
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        } else {
            dropdown.style.display = "block";
        }
    });

    // Ẩn dropdown khi click bên ngoài nó
    document.addEventListener("click", function(event) {
        if (!avatar.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = "none";
        }
    });
});
