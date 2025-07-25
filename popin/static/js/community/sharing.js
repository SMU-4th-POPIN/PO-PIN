document.addEventListener('DOMContentLoaded', () => {
  // 변수 선언 (필요한 엘리먼트들)
  const postModal = document.getElementById("postModal");
  const modalImage = document.getElementById('modalImage');
  const imageModal = document.getElementById('imageModal');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const topBtn = document.getElementById('topBtn');
  const sortSelect = document.getElementById('sortSelect'); 
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const stateFilter = document.getElementById("stateFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const categoryLinks = document.querySelectorAll(".group a[data-category]");
  const noResultsMessage = document.getElementById('noResultsMessage');
  const allCards = Array.from(document.querySelectorAll(".post-card"));
  const paginationContainer = document.querySelector('.pagination');
  
  let currentImageIndex = 0;
  let imageList = [];
  let currentPage = 1;
  const postsPerPage = 2;
  let selectedCategory = null;

  // 신고 버튼 함수 (전역에 선언 가능)
  window.reportBtn = function() {
    if (confirm("신고하시겠습니까?")) {
      alert("신고되었습니다.");
    } else {
      alert("취소");
    }
  };

  // 이미지 썸네일 클릭 -> 모달 띄우기
  document.getElementById('modalPostImages').addEventListener('click', (e) => {
    if (e.target.tagName === 'IMG') {
      const clickedSrc = e.target.src;
      const images = Array.from(document.querySelectorAll('#modalPostImages img'));
      imageList = images.map(img => img.src);
      currentImageIndex = imageList.indexOf(clickedSrc);
      modalImage.src = clickedSrc;
      imageModal.style.display = 'flex';
    }
  });

  // 이미지 모달 닫기
  imageModal.addEventListener('click', (e) => {
    if (e.target === modalImage) return;
    imageModal.style.display = 'none';
  });

  // 이미지 이전 / 다음 버튼
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

  // 모달 열기 함수
  window.openPostModal = function(artistText, stypeText, title, date, place, check, desc, imgListStr = "", tags = [], wdate = "") {
    const artistElem = document.getElementById("modalPostArtist");
    const stypeElem = document.getElementById("modalPostStype");
    const titleElem = document.getElementById("modalPostTitle");
    const dateElem = document.getElementById("modalPostDate");
    const placeElem = document.getElementById("modalPostPlace");
    const checkElem = document.getElementById("modalPostCheck");
    const descElem = document.getElementById("modalPostDescription");
    const createdElem = document.getElementById("modalPostCreated");
    const tagsContainer = document.getElementById("modalPostTags");
    const imageContainer = document.getElementById("modalPostImages");

    artistElem.textContent = artistText || "";
    stypeElem.textContent = stypeText || "";
    titleElem.textContent = title || "";
    dateElem.textContent = `📅 ${date || ""}`;
    placeElem.textContent = `📍 ${place || ""}`;
    checkElem.textContent = `✅ ${check || ""}`;
    descElem.textContent = desc || "";
    createdElem.textContent = `${wdate || ""}`;

    tagsContainer.innerHTML = "";
    if (tags.length > 0) {
      tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "post-tag";
        span.textContent = `#${tag}`;
        tagsContainer.appendChild(span);
      });
      tagsContainer.style.display = "flex";
      tagsContainer.style.gap = "10px";
    } else {
      tagsContainer.style.display = "none";
    }

    imageContainer.innerHTML = "";
    if (imgListStr) {
      const imgUrls = imgListStr.split(",").map(u => u.trim());
      imageList = imgUrls;
      imgUrls.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.alt = "첨부 이미지";
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "10px";
        imageContainer.appendChild(img);
      });
      prevBtn.style.display = imgUrls.length > 1 ? "block" : "none";
      nextBtn.style.display = imgUrls.length > 1 ? "block" : "none";
      imageContainer.style.display = "flex";
    } else {
      imageContainer.style.display = "none";
      prevBtn.style.display = "none";
      nextBtn.style.display = "none";
    }

    postModal.style.display = "block";
    topBtn.style.pointerEvents = 'none';
    topBtn.style.opacity = '0.4';
  };

  window.closePostModal = function() {
    postModal.style.display = "none";
    topBtn.style.pointerEvents = 'auto';
    topBtn.style.opacity = '1';
  };

  window.onclick = function(event) {
    if (event.target === postModal) {
      closePostModal();
    }
  };



  // 카테고리 표시 업데이트 함수
   
  function updateCategoryDisplay() {
  if (!selectedCategory) {
    // selectedCategory가 null, undefined, 빈 문자열 등 falsy하면 바로 리턴
    return;
  }
  const selectedCategoryLower = selectedCategory.toLowerCase();
  console.log('업데이트 시작', selectedCategory);
  
  categoryLinks.forEach(link => {
    link.parentElement.classList.remove('active');
  });

  const activeLink = Array.from(document.querySelectorAll('a[data-category]'))
    .find(a => a.dataset.category.toLowerCase() === selectedCategoryLower);

  console.log('활성화할 링크:', activeLink);
  if (activeLink) {
    activeLink.parentElement.classList.add('active');
    console.log('active 클래스 추가됨');
  } else {
    console.log('해당 카테고리 링크 없음');
  }
}
  // 카테고리 링크 이벤트
  categoryLinks.forEach(link => {
  link.addEventListener("click", function (e) {
    e.preventDefault();

    selectedCategory = this.dataset.category.toLowerCase();  // 현재 선택된 카테고리 기억
    updateCategoryDisplay();  // UI 업데이트

    filteredCards = allCards.filter(card => {
      const postCategory = card.dataset.category?.toLowerCase() || "";

      // "포함된 단어" 일치 (예: "nct" → "nct 127", "nct wish" 등 가능)
      return postCategory.includes(selectedCategory);
    });

    currentPage = 1;
    applyFilters();
  });
});

  // 게시글 카드 클릭 이벤트 설정
  function setupPostCardEvents() {
    // 기존 이벤트 제거 후 재등록
    document.querySelectorAll(".post-card").forEach(card => {
      card.replaceWith(card.cloneNode(true));
    });
    
    document.querySelectorAll(".post-card").forEach(card => {
      card.addEventListener("click", (event) => {
        if (
          event.target.tagName === 'BUTTON' ||
          event.target.closest('.post-actions') ||
          event.target.closest('.report-btn') ||
          event.target.closest('.join-btn')
        ) return;

        const artistText = card.querySelector(".artist")?.textContent.trim() || "";
        const stypeText = card.querySelector(".stype")?.textContent.trim() || "";
        const title = card.querySelector(".post-title")?.textContent.trim() || "";
        const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim() || "";
        const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim() || "";
        const check = card.querySelector(".info-check span:nth-child(2)")?.textContent.trim() || "";
        const desc = card.getAttribute("data-full-content") || card.querySelector(".post-description")?.textContent.trim() || "";
        const imgListStr = card.getAttribute("data-imgs") || "";
        const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.replace('#','').trim());
        const wdate = card.querySelector(".post-meta")?.textContent.trim() || "";

        openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr, tags, wdate);
      });
    });
  }

  // Top 버튼 스크롤 이벤트
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) topBtn.classList.add('show');
    else topBtn.classList.remove('show');
  });

  topBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 페이징 UI 생성 함수
  function renderPagination(totalPosts, perPage) {
    if (totalPosts === 0) {
      paginationContainer.style.display = 'none';
      return;
    } else if (totalPosts <= perPage) {
      paginationContainer.style.display = "none";
      return;
    } else {
      paginationContainer.style.display = "flex";
    }

    const totalPages = Math.ceil(totalPosts / perPage);
    paginationContainer.innerHTML = "";

    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    const maxButtons = 5;
    let startPage = Math.max(currentPage - Math.floor(maxButtons / 2), 1);
    let endPage = startPage + maxButtons - 1;

    if (endPage > totalPages) {
      endPage = totalPages;
      startPage = Math.max(endPage - maxButtons + 1, 1);
    }

    // 페이지 링크 생성 함수
    const createPageLink = (text, page, isActive = false, ariaLabel = '', isDisabled = false) => {
      const a = document.createElement('a');
      a.href = "#";
      a.textContent = text;
      if (ariaLabel) a.setAttribute('aria-label', ariaLabel);

      if (isActive) {
        a.innerHTML = `<strong>${text}</strong>`;
      }
      
      if (isDisabled) {
        a.style.pointerEvents = 'none';
        a.style.opacity = '0.5';
      }

      a.addEventListener('click', (e) => {
        e.preventDefault();
        if (isActive || isDisabled) return;
        currentPage = page;
        applyFilters();
        // 페이지 변경 후 스크롤을 위로
        setTimeout(() => {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 50);
      });

      return a;
    };

    // 페이지네이션 버튼 생성
    paginationContainer.appendChild(createPageLink('«', 1, false, '첫 페이지', currentPage === 1));
    paginationContainer.appendChild(createPageLink('‹', Math.max(currentPage - 1, 1), false, '이전 페이지', currentPage === 1));

    for (let i = startPage; i <= endPage; i++) {
      paginationContainer.appendChild(createPageLink(i.toString(), i, i === currentPage));
    }

    paginationContainer.appendChild(createPageLink('›', Math.min(currentPage + 1, totalPages), false, '다음 페이지', currentPage === totalPages));
    paginationContainer.appendChild(createPageLink('»', totalPages, false, '마지막 페이지', currentPage === totalPages));
  }

  // 필터링 + 정렬 + 페이지네이션 적용 함수
  function applyFilters() {
    const searchType = document.querySelector(".toggle-btn.active")?.dataset.type || "general";
    const keyword = ((searchType === "general" ? generalInput?.value : tagInput?.value) || "").toLowerCase().trim();
    const selectedState = stateFilter?.value || "";
    const sortOption = sortSelect?.value || "";

    let cards = Array.from(document.querySelectorAll(".post-card"));
    let filteredCards = [];

    // 필터링
    cards.forEach(card => {
      let show = true;
      
      // 카테고리 필터
      if (selectedCategory && card.dataset.category !== selectedCategory) {
        show = false;
      }
      
      // 키워드 검색
      if (show && keyword) {
        if (searchType === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          show = title.includes(keyword);
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.replace('#','').toLowerCase());
          show = tags.some(t => t.includes(keyword));
        }
      }

      // 나눔 종류 필터
      if (show && selectedState && selectedState !== "" && selectedState !== "전체") {
        const stype = card.querySelector(".stype")?.textContent.trim() || "";
        show = stype === selectedState;
      }

      if (show) {
        filteredCards.push(card);
      }
    });

    // 정렬
    if (sortOption === "최신순") {
      filteredCards.sort((a, b) => {
        const dateA = a.querySelector(".post-meta")?.textContent.trim() || "";
        const dateB = b.querySelector(".post-meta")?.textContent.trim() || "";
        return new Date(dateB) - new Date(dateA);
      });
    } else if (sortOption === "조회순") {
      filteredCards.sort((a, b) => {
        const viewsA = parseInt(a.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "") || 0);
        const viewsB = parseInt(b.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "") || 0);
        return viewsB - viewsA;
      });
    }

    // 페이징 처리
    const total = filteredCards.length;
    const start = (currentPage - 1) * postsPerPage;
    const paginatedCards = filteredCards.slice(start, start + postsPerPage);

    // 모든 카드 숨기기
    cards.forEach(card => {
      card.style.display = "none";
    });

    // 페이징된 카드만 보이기
    paginatedCards.forEach(card => {
      card.style.display = "block";
    });

    // 페이지네이션 렌더링
    renderPagination(total, postsPerPage);

    // 결과 메시지 처리
    if (total === 0) {
      noResultsMessage.style.display = 'block';
    } else {
      noResultsMessage.style.display = 'none';
    }

    // 이벤트 재등록
    setupPostCardEvents();
  }

  // 토글 버튼 이벤트 (검색 타입)
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      if (btn.classList.contains("active")) return;

      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const type = btn.dataset.type;
      if (type === "general") {
        generalInput.style.display = "block";
        tagInput.style.display = "none";
        tagInput.value = "";
      } else if (type === "tag") {
        generalInput.style.display = "none";
        tagInput.style.display = "block";
        generalInput.value = "";
      }

      currentPage = 1;
      applyFilters();
    });
  });

  // 검색 입력 및 필터, 정렬 변경 이벤트
  [generalInput, tagInput, stateFilter, sortSelect].forEach(input => {
    if (!input) return;
    const eventName = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, () => {
      currentPage = 1;
      applyFilters();
    });
  });

  // 초기 설정
  setupPostCardEvents();
  applyFilters();
  updateCategoryDisplay();
});