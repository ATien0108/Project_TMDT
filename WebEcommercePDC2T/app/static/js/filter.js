// Xác định thanh kéo giá tiền
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');

// Thêm sự kiện cho thanh kéo giá tiền
priceRange.addEventListener('input', function() {
    // Hiển thị giá trị hiện tại của thanh kéo
    priceValue.textContent = formatCurrency(priceRange.value) + ' VND';
});

// Hàm định dạng tiền tệ
function formatCurrency(amount) {
    return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Xác định nút lọc
const filterButton = document.querySelector('.filter_button');

// Thêm sự kiện cho nút lọc
filterButton.addEventListener('click', function() {
    // Lấy giá trị hiện tại của thanh kéo
    const minPrice = parseInt(document.getElementById('priceRange').value);

    // Lọc danh sách các sản phẩm dựa trên giá tiền
    const filteredProducts = products.filter(product => {
        return product.price >= minPrice;
    });

    // Hiển thị các sản phẩm đã lọc
    displayProducts(filteredProducts);
});

// Hàm hiển thị danh sách sản phẩm
function displayProducts(products) {
    // Lấy danh sách swiper
    const swipers = document.querySelectorAll('.swiper');

    // Duyệt qua từng swiper
    swipers.forEach(swiper => {
        // Lấy wrapper của swiper hiện tại
        const swiperWrapper = swiper.querySelector('.swiper-wrapper');

        // Xóa hết các slide hiện có trong swiper
        swiperWrapper.innerHTML = '';

        // Duyệt qua danh sách sản phẩm và thêm các slide mới vào swiper
        products.forEach(product => {
            const slideHTML = `
                <div class="swiper-slide">
                    <div class="card">
                        <div class="card_top">
                            <a href="#"><img src="${product.image}" alt="" class="card_img"></a>
                            <div class="card_top_icons">
                                <a href="#"><i class="uil uil-heart card_top_icon"></i></a>
                                <a href="#"><i class="uil uil-eye card_top_icon"></i></a>
                            </div>
                        </div>
                        <div class="card_body">
                            <h3 class="card_title">${product.name}</h3>
                            <p class="card_price">${formatCurrency(product.price)} VND</p>
                        </div>
                    </div>
                </div>
            `;
            swiperWrapper.insertAdjacentHTML('beforeend', slideHTML);
        });
    });
}