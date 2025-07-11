// 이미지 모달 기능
let currentImageIndex = 0;
const images = document.querySelectorAll('.image-item');
const modal = document.getElementById('imageModal');
const modalImage = document.getElementById('modalImage');
const modalCaption = document.getElementById('modalCaption');

function openModal(imageItem) {
    const img = imageItem.querySelector('img');
    
    currentImageIndex = Array.from(images).indexOf(imageItem);
    
    modalImage.src = img.src;
    modalCaption.textContent = '';  // 캡션 제거
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    }

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function changeImage(direction) {
    currentImageIndex += direction;

    if (currentImageIndex >= images.length) {
        currentImageIndex = 0;
    } else if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1;
    }

    const currentItem = images[currentImageIndex];
    const img = currentItem.querySelector('img');

    modalImage.src = img.src;
    modalCaption.textContent = '';  // 캡션 제거
    }

// 키보드 이벤트
document.addEventListener('keydown', function(e) {
    if (modal.style.display === 'block') {
    if (e.key === 'Escape') {
        closeModal();
    } else if (e.key === 'ArrowLeft') {
        changeImage(-1);
    } else if (e.key === 'ArrowRight') {
        changeImage(1);
    }
    }
});

// 모달 배경 클릭 시 닫기
modal.addEventListener('click', function(e) {
    if (e.target === modal) {
    closeModal();
    }
});