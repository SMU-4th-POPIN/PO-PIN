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
    categoryLinks.forEach(link => {
      link.parentElement.classList.remove('active');
    });
    if (selectedCategory) {
      const activeLink = document.querySelector(`a[data-category="${selectedCategory}"]`);
      if (activeLink) activeLink.parentElement.classList.add('active');
    }
  }

  // 카테고리 링크 이벤트
  categoryLinks.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      selectedCategory = link.dataset.category || null;
      currentPage = 1;
      updateCategoryDisplay();
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
        const desc = card.querySelector(".post-description")?.textContent.trim() || "";
        const imgListStr = card.getAttribute("data-imgs") || "";
        const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.replace('#','').trim());
        const wdate = card.querySelector(".post-meta")?.textContent.trim() || "";

        openPostModal(artistText, stypeText, title, date, place, check, desc, imgListStr, tags, wdate);
      });
    });
  }

  setupPostCardEvents();

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
    const paginationContainer = document.querySelector('.pagination');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const postList = document.querySelector('.postlist');

    if (totalPosts === 0) {
      paginationContainer.style.display = 'none';
      postList.style.display = 'none';
      noResultsMessage.style.display = 'block';
      return;
    } else if (totalPosts <= perPage) {
      paginationContainer.innerHTML = "";
      paginationContainer.style.display = "none";
      postList.style.display = 'block';
      noResultsMessage.style.display = 'none';
      return;
    } else {
      paginationContainer.style.display = "flex";
      noResultsMessage.style.display = 'none';
      postList.style.display = 'block';
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

      if (isActive) a.classList.add('active');
      if (isDisabled) {
        a.classList.add('disabled');
        a.setAttribute("aria-disabled", "true");
      }

      a.addEventListener('click', (e) => {
        e.preventDefault();
        if (isActive || isDisabled) return;
        currentPage = page;
        applyFilters();
        requestAnimationFrame(() => {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      });

      return a;
    };

    paginationContainer.appendChild(createPageLink('«', 1, false, '첫 페이지', currentPage === 1));
    paginationContainer.appendChild(createPageLink('‹', Math.max(currentPage - 1, 1), false, '이전 페이지', currentPage === 1));

    for (let i = startPage; i <= endPage; i++) {
      paginationContainer.appendChild(createPageLink(i, i, i === currentPage));
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

    // 필터링
    cards.forEach(card => {
      let show = true;
      
      if (selectedCategory && card.dataset.category !== selectedCategory) {
        show = false;
      }
      
      if (show && keyword) {
        if (searchType === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          show = title.includes(keyword);
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.replace('#','').toLowerCase());
          show = tags.some(t => t.includes(keyword));
        }
      }

      if (show && selectedState && selectedState !== "" && selectedState !== "전체") {
        const stype = card.querySelector(".stype")?.textContent.trim() || "";
        show = stype === selectedState;
      }

      card.style.display = show ? "block" : "none";
    });

    // 보이는 카드만 가져오기
    const visibleCards = cards.filter(card => card.style.display !== "none");
    
    // 정렬
    if (sortOption === "최신순") {
      visibleCards.sort((a, b) => {
        const dateA = a.querySelector(".post-meta")?.textContent.trim() || "";
        const dateB = b.querySelector(".post-meta")?.textContent.trim() || "";
        return new Date(dateB) - new Date(dateA);
      });
    } else if (sortOption === "조회순") {
      visibleCards.sort((a, b) => {
        const viewsA = parseInt(a.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "") || 0);
        const viewsB = parseInt(b.querySelector(".participants span")?.textContent.replace(/[^\d]/g, "") || 0);
        return viewsB - viewsA;
      });
    }

    // DOM에 정렬된 순서대로 카드 배치
    const postlistContainer = document.querySelector('.postlist');
    const paginationElement = document.querySelector('.pagination');
    if (postlistContainer && visibleCards.length > 0) {
      visibleCards.forEach(card => {
        if (paginationElement) {
          postlistContainer.insertBefore(card, paginationElement);
        } else {
          postlistContainer.appendChild(card);
        }
      });
    }

    // 페이징
    const total = visibleCards.length;
    const start = (currentPage - 1) * postsPerPage;
    const paginated = visibleCards.slice(start, start + postsPerPage);

    // 모든 카드 숨기고 페이징 대상 카드만 보여주기
    cards.forEach(card => card.style.display = "none");
    paginated.forEach(card => card.style.display = "block");

    renderPagination(total, postsPerPage);

    setupPostCardEvents();  // 이벤트 재등록

    // 게시글 없을 때 / 있을 때 메시지 처리
    const noResultsMessage = document.getElementById('noResultsMessage');
    if (total === 0) {
      noResultsMessage.style.display = 'block';
      postlistContainer.style.display = 'none';
    } else {
      noResultsMessage.style.display = 'none';
      postlistContainer.style.display = 'block';
    }
  }

  // 토글 버튼 이벤트 (검색 타입)
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      generalInput.style.display = btn.dataset.type === "general" ? "block" : "none";
      tagInput.style.display = btn.dataset.type === "tag" ? "block" : "none";
      generalInput.value = "";
      tagInput.value = "";
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

  // 초기 필터 적용 및 카테고리 표시 업데이트
  applyFilters();
  updateCategoryDisplay();
});
