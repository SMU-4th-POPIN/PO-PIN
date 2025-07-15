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
  let selectedCategory = "";

  // 검색 및 필터링 관련 변수들을 먼저 선언
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const ratingFilter = document.getElementById("ratingFilter");
  const sortFilter = document.getElementById("sortFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const boardItems = Array.from(document.querySelectorAll(".board-item"));

  let filteredCards = boardItems; // 초기값 설정
  let currentPage = 1;
  const itemsPerPage = 2;

  // 카테고리 링크 이벤트 리스너
  const categoryLinks = document.querySelectorAll(".menu a");
  categoryLinks.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();

      categoryLinks.forEach(l => l.parentElement.classList.remove("active"));
      link.parentElement.classList.add("active");

      selectedCategory = link.dataset.category?.trim() || "";

      applyFilters();
    });
  });

  // 후기 카드 클릭 시 모달 열기
  document.querySelectorAll(".board-item").forEach(item => {
  item.addEventListener("click", (e) => {
    if (e.target.closest('.report-btn')) return;

    const artistText = item.querySelector(".artist")?.textContent.trim();
    const onoffText = item.querySelector(".onoff")?.textContent.trim();
    const TwayText = item.querySelector(".Tway")?.textContent.trim();
    const title = item.querySelector(".board-title")?.textContent.trim();
    const star = item.querySelector(".star")?.textContent.trim();
    
    // 수정: .board-content가 있으면 전체 내용, 없으면 .board-preview 사용
    const desc = item.querySelector(".board-content")?.innerHTML.trim() || 
                 item.querySelector(".board-preview")?.textContent.trim();
    
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
  
  // 수정: innerHTML 대신 textContent 사용하여 전체 내용 표시
  const descriptionEl = document.getElementById("modalPostDescription");
  descriptionEl.textContent = desc; // 전체 내용 표시
  // 또는 줄바꿈을 유지하려면:
  // descriptionEl.innerHTML = desc.replace(/\n/g, '<br>');
  
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

  // 토글 버튼 클릭 시 검색 입력창 전환
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault(); // 기본 동작 방지
      
      // 이미 활성화된 버튼을 클릭한 경우 아무것도 하지 않음
      if (this.classList.contains("active")) {
        return;
      }

      toggleBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const searchType = this.dataset.type;
      if (searchType === "general") {
        generalInput.style.display = "block";
        tagInput.style.display = "none";
        tagInput.value = ""; // 태그 검색 입력값 초기화
      } else if (searchType === "tag") {
        generalInput.style.display = "none";
        tagInput.style.display = "block";
        generalInput.value = ""; // 일반 검색 입력값 초기화
      }
      
      applyFilters();
    });
  });

  // 검색 입력 이벤트
  if (generalInput) {
    generalInput.addEventListener("input", function() {
      applyFilters();
    });
  }
  
  if (tagInput) {
    tagInput.addEventListener("input", function() {
      applyFilters();
    });
  }
  
  if (ratingFilter) {
    ratingFilter.addEventListener("change", function() {
      applyFilters();
    });
  }
  
  if (sortFilter) {
    sortFilter.addEventListener("change", function() {
      applyFilters();
    });
  }

  // 검색/필터/정렬 적용 함수
  function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = (searchMode === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
    const selectedRating = ratingFilter?.value;
    const sortBy = sortFilter?.value;

    const allCards = Array.from(document.querySelectorAll(".board-item"));
    const noResults = document.getElementById("noResultsMessage");
    const pagination = document.querySelector(".pagination");

    filteredCards = allCards.filter(item => {
      let showCard = true;

      // 카테고리 필터
      if (selectedCategory && selectedCategory !== "") {
        const cardCategory = item.dataset.category?.trim() || "";
        showCard = showCard && (selectedCategory === cardCategory);
      }

      // 검색 필터
      if (showCard && keyword) {
        if (searchMode === "general") {
          const title = item.querySelector(".board-title")?.textContent.toLowerCase() || "";
          const writer = item.querySelector(".writer_id")?.textContent.toLowerCase() || "";
          const partner = item.querySelector(".partner_id")?.textContent.toLowerCase() || "";
          showCard = title.includes(keyword) || writer.includes(keyword) || partner.includes(keyword);
        } else if (searchMode === "tag") {
          const tags = Array.from(item.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase().trim());
          showCard = tags.some(tag => tag.includes(keyword));
        }
      }

      // 평점 필터
      if (showCard && selectedRating && selectedRating !== "") {
        const star = item.querySelector(".star")?.textContent.replace("⭐", "").trim();
        showCard = star === selectedRating;
      }

      return showCard;
    });

    // 정렬
    if (sortBy) {
      filteredCards.sort((a, b) => {
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

    // 검색 결과 처리
    if (filteredCards.length === 0) {
      if (noResults) {
        noResults.textContent = "해당 게시물이 없습니다.";
        noResults.style.display = "block";
      }
      allCards.forEach(card => card.style.display = "none");
      if (pagination) pagination.style.display = "none";
      return;
    } else {
      if (noResults) noResults.style.display = "none";
      if (pagination) pagination.style.display = "flex";
    }

    // 페이지네이션 초기화 및 적용
    resetPagination(filteredCards);
  }

  // 페이지네이션 메인 함수
  function showPage(pageNumber) {
    currentPage = pageNumber;
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    // 모든 카드 숨기기
    document.querySelectorAll(".board-item").forEach(card => {
      card.style.display = "none";
    });

    // 현재 페이지에 해당하는 카드들만 보이기
    const cardsToShow = filteredCards.slice(startIndex, endIndex);
    cardsToShow.forEach(card => {
      card.style.display = "block";
    });

    const pagination = document.querySelector(".pagination");
    if (pagination) {
      const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
      
      // 게시물이 없거나 한 페이지에 모든 게시물이 들어가면 페이지네이션 숨김
      if (filteredCards.length <= itemsPerPage) {
        pagination.style.display = "none";
      } else {
        pagination.style.display = "flex";
        createPageNumberButtons(pagination, totalPages);
      }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function createPageNumberButtons(pagination, totalPages) {
  pagination.innerHTML = "";  // 버튼 초기화

  const maxVisiblePages = 5;

  // « 첫 페이지
  const firstBtn = document.createElement("a");
  firstBtn.href = "#";
  firstBtn.textContent = "«";
  if (currentPage === 1) firstBtn.classList.add("disabled");
  firstBtn.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage !== 1) showPage(1);
  });
  pagination.appendChild(firstBtn);

  // ‹ 이전 페이지
  const prevBtn = document.createElement("a");
  prevBtn.href = "#";
  prevBtn.textContent = "‹";
  if (currentPage === 1) prevBtn.classList.add("disabled");
  prevBtn.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage > 1) showPage(currentPage - 1);
  });
  pagination.appendChild(prevBtn);

  // 페이지 번호 범위 계산
  let startPage, endPage;
  if (totalPages <= maxVisiblePages) {
    startPage = 1;
    endPage = totalPages;
  } else {
    startPage = Math.max(1, currentPage - 2);
    endPage = startPage + maxVisiblePages - 1;
    if (endPage > totalPages) {
      endPage = totalPages;
      startPage = endPage - maxVisiblePages + 1;
    }
  }

  // 페이지 번호 버튼 생성
  for (let i = startPage; i <= endPage; i++) {
    if (i === currentPage) {
      const current = document.createElement("strong");
      current.textContent = i;
      pagination.appendChild(current);
    } else {
      const btn = document.createElement("a");
      btn.href = "#";
      btn.textContent = i;
      btn.addEventListener("click", e => {
        e.preventDefault();
        showPage(i);
      });
      pagination.appendChild(btn);
    }
  }

  // › 다음 페이지
  const nextBtn = document.createElement("a");
  nextBtn.href = "#";
  nextBtn.textContent = "›";
  if (currentPage === totalPages) nextBtn.classList.add("disabled");
  nextBtn.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage < totalPages) showPage(currentPage + 1);
  });
  pagination.appendChild(nextBtn);

  // » 마지막 페이지
  const lastBtn = document.createElement("a");
  lastBtn.href = "#";
  lastBtn.textContent = "»";
  if (currentPage === totalPages) lastBtn.classList.add("disabled");
  lastBtn.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage !== totalPages) showPage(totalPages);
  });
  pagination.appendChild(lastBtn);
}
  // 필터링 후 페이지네이션 초기화
  function resetPagination(newFilteredCards) {
    filteredCards = newFilteredCards;
    currentPage = 1;

    const container = document.querySelector(".board-list");
    const noResultsMessage = document.getElementById("noResultsMessage");

    if (container && filteredCards.length === 0) {
      // 게시물이 없을 때만 메시지 표시
      if (noResultsMessage) {
        noResultsMessage.textContent = "해당 게시물이 없습니다.";
        noResultsMessage.style.display = "block";
      }
    } else {
      if (noResultsMessage) noResultsMessage.style.display = "none";
    }

    showPage(1); // 첫 페이지 보여주기
  }

  // 초기 실행
  filteredCards = boardItems;
  showPage(1);
});