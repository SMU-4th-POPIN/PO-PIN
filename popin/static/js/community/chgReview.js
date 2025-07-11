function reportBtn(){
  if(confirm("신고하시겠습니까?")){
    alert("신고되었습니다.");
  }else{
    alert("취소");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const modalImage = document.getElementById('modalImage');
  const imageModal = document.getElementById('imageModal');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const postModal = document.getElementById("postModal");
  const topBtn = document.getElementById("topBtn");
  let currentImageIndex = 0;
  let imageList = [];

  // 후기 카드 클릭 시 모달 열기
  document.querySelectorAll(".board-item").forEach(item => {
    item.addEventListener("click", (e) => {
      if (e.target.closest('.report-btn')) return;

      const artistText = item.querySelector(".artist")?.textContent.trim();
      const onoffText = item.querySelector(".onoff")?.textContent.trim();
      const TwayText = item.querySelector(".Tway")?.textContent.trim();
      const title = item.querySelector(".board-title")?.textContent.trim();
      const star = item.querySelector(".star")?.textContent.trim();
      const desc = item.querySelector(".board-preview, .board-content")?.textContent.trim();
      const writer = item.querySelector(".writer_id")?.textContent.trim();
      const partner = item.querySelector(".partner_id")?.textContent.trim();
      const date = item.querySelector(".post-date")?.textContent.trim();
      const images = item.getAttribute("data-images")?.split(",") || [];
      const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.trim());

      openPostModal(artistText, onoffText, TwayText, title, `${writer} ⇄ ${partner}`, star, desc, images, tags, date);
    });
  });

  function openPostModal(artistText, onoffText, TwayText, title, writerPartner, star, desc, imageUrls = [], tags = [], date = "") {
    const [writer, partner] = writerPartner.split(" ⇄ ");

    const artistEl = document.getElementById("modalPostArtist");
    const onoffEl = document.getElementById("modalPostOnoff");
    const TwayEl = document.getElementById("modalPostTway");

    artistEl.textContent = artistText;
    artistEl.className = "artist";

    onoffEl.textContent = onoffText;
    onoffEl.className = "onoff";

    TwayEl.textContent = TwayText;
    TwayEl.className = "Tway";

    document.getElementById("modalPostTitle").textContent = title;
    document.getElementById("modalPostWriter").textContent = `${writer}`;
    document.getElementById("modalPostPartner").textContent = `🔄 ${partner}`;
    document.getElementById("modalPostStar").textContent = `${star}`;
    document.getElementById("modalPostDescription").textContent = desc;
    document.getElementById("modalPostDate").textContent = date;

    const tagsContainer = document.getElementById("modalPostTags");
    tagsContainer.innerHTML = "";

    if (tags.length > 0) {
      tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "post-tag";
        span.textContent = `${tag}`;
        tagsContainer.appendChild(span);
      });
      tagsContainer.style.display = "flex";
      tagsContainer.style.gap = "10px";
    } else {
      tagsContainer.style.display = "none";
    }

    const imageContainer = document.getElementById("modalPostImages");
    imageContainer.innerHTML = "";

    if (imageUrls.length > 0 && imageUrls[0] !== "") {
      imageList = imageUrls.map(url => url.trim());
      imageList.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.alt = "후기 이미지";
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "10px";
        imageContainer.appendChild(img);
      });

      imageContainer.style.display = "flex";

      if (imageList.length > 1) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
      } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
      }
    } else {
      imageContainer.style.display = "none";
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
    }

    postModal.style.display = "flex";
    topBtn.style.pointerEvents = 'none';
    topBtn.style.opacity = '0.4';
  }

  // 모달 닫기
  window.closePostModal = function () {
    postModal.style.display = "none";
    topBtn.style.pointerEvents = 'auto';
    topBtn.style.opacity = '1';
  }

  // 바깥 클릭 시 닫기
  window.addEventListener("click", function (event) {
    if (event.target === postModal) {
      closePostModal();
    }
  });

  // 이미지 썸네일 클릭 시 전체보기
  const imageContainer = document.getElementById('modalPostImages');
  if (imageContainer) {
    imageContainer.addEventListener('click', (e) => {
      if (e.target.tagName === 'IMG') {
        const clickedSrc = e.target.src;
        const images = Array.from(imageContainer.querySelectorAll('img'));
        imageList = images.map(img => img.src);
        currentImageIndex = imageList.indexOf(clickedSrc);
        modalImage.src = clickedSrc;
        imageModal.style.display = 'flex';
      }
    });
  }

  if (imageModal) {
    imageModal.addEventListener('click', (e) => {
      if (e.target === modalImage) return;
      imageModal.style.display = 'none';
    });

    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });

    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex + 1) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });
  }

  // Top 버튼 기능
  window.addEventListener('scroll', function () {
    if (window.pageYOffset > 300) {
      topBtn.classList.add('show');
    } else {
      topBtn.classList.remove('show');
    }
  });

  topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 검색 및 필터링 기능
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const ratingFilter = document.getElementById("ratingFilter");
  const sortFilter = document.getElementById("sortFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const boardItems = Array.from(document.querySelectorAll(".board-item"));

  // 토글 버튼 클릭 시 검색 입력창 전환
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const type = btn.dataset.type;
      if (type === "general") {
        generalInput.style.display = "inline-block";
        tagInput.style.display = "none";
      } else {
        generalInput.style.display = "none";
        tagInput.style.display = "inline-block";
      }
      applyFilters();
    });
  });

  // 검색 입력 이벤트
  generalInput.addEventListener("input", applyFilters);
  tagInput.addEventListener("input", applyFilters);
  ratingFilter.addEventListener("change", applyFilters);
  sortFilter.addEventListener("change", applyFilters);

  // 검색/필터/정렬 적용 함수
  function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchMode === "general" ? generalInput.value : tagInput.value).toLowerCase();
    const selectedRating = ratingFilter.value;
    const sortBy = sortFilter.value;

    let filtered = boardItems.filter(item => {
      const title = item.querySelector(".board-title")?.textContent.toLowerCase() || "";
      const writer = item.querySelector(".writer_id")?.textContent.toLowerCase() || "";
      const partner = item.querySelector(".partner_id")?.textContent.toLowerCase() || "";
      const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase());
      const star = item.querySelector(".star")?.textContent.replace("⭐", "").trim();

      // 검색 필터
      let matchSearch = true;
      if (keyword) {
        if (searchMode === "general") {
          matchSearch = title.includes(keyword) || writer.includes(keyword) || partner.includes(keyword);
        } else {
          matchSearch = tags.some(tag => tag.includes(keyword));
        }
      }

      // 평점 필터
      let matchRating = true;
      if (selectedRating) {
        matchRating = star === selectedRating;
      }

      return matchSearch && matchRating;
    });

    // 정렬
    if (sortBy) {
      filtered.sort((a, b) => {
        if (sortBy === "latest") {
          const dateA = new Date(a.querySelector(".post-date")?.textContent.trim() || 0);
          const dateB = new Date(b.querySelector(".post-date")?.textContent.trim() || 0);
          return dateB - dateA;
        } else if (sortBy === "rating") {
          const ratingA = parseFloat(a.querySelector(".star")?.textContent.replace("⭐", "").trim() || 0);
          const ratingB = parseFloat(b.querySelector(".star")?.textContent.replace("⭐", "").trim() || 0);
          return ratingB - ratingA;
        } else if (sortBy === "views") {
          const viewsA = parseInt(a.querySelector(".board-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
          const viewsB = parseInt(b.querySelector(".board-meta span:last-child")?.textContent.replace("👁️", "").trim() || 0);
          return viewsB - viewsA;
        }
        return 0;
      });
    }

    // 페이지네이션 초기화 및 적용
    resetPagination(filtered);
  }

  // 초기 필터링 적용
  applyFilters();
});

// 페이지네이션 관련 변수
let currentPage = 1;
let itemsPerPage = 2;
let filteredCards = [];

// 페이지네이션 메인 함수
function showPage(pageNumber) {
  currentPage = pageNumber;
  hideAllCards();
  showCurrentPageCards();
  updatePageButtons();

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 모든 카드 숨기기
function hideAllCards() {
  const allCards = document.querySelectorAll(".board-item");
  allCards.forEach(card => {
    card.style.display = "none";
  });
}

// 현재 페이지 카드들만 보여주기
function showCurrentPageCards() {
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const cardsToShow = filteredCards.slice(startIndex, endIndex);

  cardsToShow.forEach(card => {
    card.style.display = "block"; // 필요한 카드만 보이게 함
  });
}


// 페이지네이션 버튼 업데이트
function updatePageButtons() {
  const pagination = document.querySelector(".pagination");
  if (!pagination) return;

  const totalPages = Math.ceil(filteredCards.length / itemsPerPage);

  // ✅ 페이지 수가 1 이하 또는 전체 게시물 수가 한 페이지 이하일 경우 페이지네이션 숨김
  if (totalPages <= 1 || filteredCards.length <= itemsPerPage) {
    pagination.innerHTML = "";
    pagination.style.display = "none";
    return;
  } else {
    pagination.style.display = "flex";
  }

  pagination.innerHTML = "";

  createNavigationButtons(pagination, totalPages);
  createPageNumberButtons(pagination, totalPages);
}

// 이전/다음 버튼 생성
function createNavigationButtons(pagination, totalPages) {
  const firstBtn = createButton("«", "첫 페이지", () => {
    if (currentPage > 1) showPage(1);
  });
  
  const prevBtn = createButton("‹", "이전 페이지", () => {
    if (currentPage > 1) showPage(currentPage - 1);
  });
  
  const nextBtn = createButton("›", "다음 페이지", () => {
    if (currentPage < totalPages) showPage(currentPage + 1);
  });
  
  const lastBtn = createButton("»", "마지막 페이지", () => {
    if (currentPage < totalPages) showPage(totalPages);
  });
  
  // 비활성화 상태 스타일링
  if (currentPage === 1) {
    firstBtn.classList.add('disabled');
    prevBtn.classList.add('disabled');
  }
  
  if (currentPage === totalPages) {
    nextBtn.classList.add('disabled');
    lastBtn.classList.add('disabled');
  }
  
  pagination.appendChild(firstBtn);
  pagination.appendChild(prevBtn);
  pagination.nextBtn = nextBtn;
  pagination.lastBtn = lastBtn;
}

// 페이지 번호 버튼들 생성
function createPageNumberButtons(pagination, totalPages) {
  const maxVisiblePages = 5;
  let startPage, endPage;
  
  if (totalPages <= maxVisiblePages) {
    startPage = 1;
    endPage = totalPages;
  } else {
    startPage = Math.max(1, currentPage - 2);
    endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage === totalPages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
  }
  
  for (let i = startPage; i <= endPage; i++) {
    const pageBtn = createPageButton(i, i === currentPage);
    pagination.appendChild(pageBtn);
  }
  
  pagination.appendChild(pagination.nextBtn);
  pagination.appendChild(pagination.lastBtn);
}

// 일반 버튼 생성 헬퍼 함수
function createButton(text, title, clickHandler) {
  const button = document.createElement("a");
  button.href = "#";
  button.title = title;
  button.textContent = text;
  button.addEventListener("click", (e) => {
    e.preventDefault();
    if (!button.classList.contains('disabled')) {
      clickHandler();
    }
  });
  return button;
}

// 페이지 번호 버튼 생성 헬퍼 함수
function createPageButton(pageNumber, isCurrentPage) {
  if (isCurrentPage) {
    const currentBtn = document.createElement("strong");
    currentBtn.textContent = pageNumber;
    currentBtn.classList.add('current-page');
    return currentBtn;
  } else {
    return createButton(pageNumber, `${pageNumber}페이지`, () => {
      showPage(pageNumber);
    });
  }
}

// 필터링 후 페이지네이션 초기화
function resetPagination(newFilteredCards) {
  filteredCards = newFilteredCards;
  currentPage = 1;

  const container = document.querySelector(".board-list");
  const noResultsMessage = document.getElementById("noResultsMessage");

  if (container) {
    container.innerHTML = "";

    // 게시물 0개일 경우 메시지 표시
    if (filteredCards.length === 0) {
      if (noResultsMessage) {
        noResultsMessage.textContent = "해당 조건에 맞는 게시물이 없습니다.";
        noResultsMessage.style.display = "block";
      }
    } else {
      if (noResultsMessage) noResultsMessage.style.display = "none";
      filteredCards.forEach(item => {
        item.style.display = "none";
        container.appendChild(item);
      });
    }
  }

  showPage(1); // 첫 페이지 보여주기
}

// 초기 실행
function initializePagination() {
  filteredCards = Array.from(document.querySelectorAll(".board-item"));
  showPage(1);
}