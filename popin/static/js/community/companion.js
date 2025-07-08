// 신고버튼
function reportBtn() {
  if (confirm("신고하시겠습니까?")) {
    alert("신고되었습니다.");
  } else {
    alert("취소");
  }
}

// 채팅버튼
// document.getElementById("chatButton").addEventListener("click", function () {
//     location.href = "/chatting/chatting.html";
// });

// 메뉴 선택
const categoryLinks = document.querySelectorAll(".menu a");

categoryLinks.forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();

    const selectedCategory = link.dataset.category?.trim();
    const allCards = document.querySelectorAll(".post-card");

    filteredCards = Array.from(allCards).filter(card => {
      const cardCategory = card.dataset.category?.trim();
      return selectedCategory === "" || selectedCategory === cardCategory;
    });

    // 모든 카드 숨기고 필터링된 카드만 보여주기
    allCards.forEach(card => card.style.display = "none");

    showPage(1);
  });
});



document.addEventListener("DOMContentLoaded", function () {
  const modalImage = document.getElementById('modalImage');
  let currentImageIndex = 0;
  let imageList = [];

  const imageModal = document.getElementById('imageModal');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const postModal = document.getElementById("postModal");
  const postList = document.querySelector(".postlist");
  const topBtn = document.getElementById('topBtn');
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const regionFilter = document.getElementById("regionFilter");
  const stateFilter = document.getElementById("stateFilter");

  let filteredCards = [];
  let currentPage = 1;
  const itemsPerPage = 3;

  // 이미지 썸네일 클릭 시 모달 띄우기
  if (modalImage && document.getElementById('modalPostImages')) {
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
  }

  if (imageModal) {
    imageModal.addEventListener('click', (e) => {
      if (e.target === modalImage) return;
      imageModal.style.display = 'none';
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex + 1) % imageList.length;
      modalImage.src = imageList[currentImageIndex];
    });
  }

  // 후기 카드 클릭 시 모달 열기
  if (postList) {
    postList.addEventListener("click", (e) => {
      const card = e.target.closest(".post-card");
      if (!card) return;

      if (e.target.closest('.report-btn') || e.target.closest('.join-btn')) return;

      const artistText = card.querySelector(".artist")?.textContent.trim();
      const regionText = card.querySelector(".region")?.textContent.trim();
      const ptypeText = card.querySelector(".ptype")?.textContent.trim();
      const title = card.querySelector(".post-title")?.textContent.trim();
      const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim();
      const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim();
      const people = card.querySelector(".info-people span:nth-child(2)")?.textContent.trim();
      const desc = card.querySelector(".post-description")?.textContent.trim();
      const wdate = card.querySelector(".post-meta")?.textContent.trim();
      const imgListStr = card.getAttribute("data-imgs") || "";
      const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

      openPostModal(artistText, regionText, ptypeText, title, date, place, people, desc, imgListStr, tags, wdate);
    });
  }

  function openPostModal(artistText, regionText, ptypeText, title, date, place, people, desc, imgListStr = "", tags = [], wdate = "") {
    const artistEl = document.getElementById("modalPostArtist");
    const regionEl = document.getElementById("modalPostRegion");
    const ptypeEl = document.getElementById("modalPostPtype");

    artistEl.textContent = artistText;
    artistEl.className = "artist";

    regionEl.textContent = regionText;
    regionEl.className = "region";

    ptypeEl.textContent = ptypeText;
    ptypeEl.className = "ptype";

    document.getElementById("modalPostTitle").textContent = title;
    document.getElementById("modalPostDate").textContent = `📅 ${date}`;
    document.getElementById("modalPostPlace").textContent = `📍 ${place}`;
    document.getElementById("modalPostPeople").textContent = `👥 ${people}`;
    document.getElementById("modalPostDescription").textContent = desc;
    document.getElementById("modalPostCreated").textContent = wdate;

    const tagsContainer = document.getElementById("modalPostTags");
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

    const imageContainer = document.getElementById("modalPostImages");
    imageContainer.innerHTML = "";
    if (imgListStr) {
      const imgUrls = imgListStr.split(",").map(url => url.trim());
      imageList = imgUrls;

      imgUrls.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.alt = "첨부 이미지";
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "10px";
        img.style.cursor = "pointer";
        imageContainer.appendChild(img);
      });

      prevBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
      nextBtn.style.display = imgUrls.length > 1 ? 'block' : 'none';
      imageContainer.style.display = 'flex';
    } else {
      imageContainer.style.display = 'none';
    }

    postModal.style.display = "block";
    if (topBtn) {
      topBtn.style.pointerEvents = 'none';
      topBtn.style.opacity = '0.4';
    }
  }

  function closePostModal() {
    postModal.style.display = "none";
    if (topBtn) {
      topBtn.style.pointerEvents = 'auto';
      topBtn.style.opacity = '1';
    }
  }

  window.addEventListener("click", function (event) {
    if (event.target === postModal) {
      closePostModal();
    }
  });

  if (topBtn) {
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
  }

  // 페이지네이션 함수
  function showPage(pageNumber) {
    currentPage = pageNumber;
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    document.querySelectorAll(".post-card").forEach(card => {
      card.style.display = "none";
    });

    const cardsToShow = filteredCards.slice(startIndex, endIndex);
    cardsToShow.forEach(card => {
      card.style.display = "block";
    });

    const pagination = document.querySelector(".pagination");
    if (pagination) {
      const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
      createPageNumberButtons(pagination, totalPages);
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function createPageNumberButtons(pagination, totalPages) {
    const maxVisiblePages = 5;
    pagination.innerHTML = "";

    // 첫 페이지 버튼
    const firstBtn = document.createElement("a");
    firstBtn.href = "#";
    firstBtn.textContent = "«";
    // firstBtn.className = currentPage === 1 ? "disabled" : "";
    firstBtn.addEventListener("click", e => {
      e.preventDefault();
      if (currentPage !== 1) showPage(1);
    });
    pagination.appendChild(firstBtn);

    // 이전 페이지 버튼
    const prevBtn = document.createElement("a");
    prevBtn.href = "#";
    prevBtn.textContent = "‹";
    // prevBtn.className = currentPage === 1 ? "disabled" : "";
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

    // 페이지 번호 버튼들 생성
    for (let i = startPage; i <= endPage; i++) {
      const btn = document.createElement("a");
      btn.href = "#";
      btn.textContent = i;
      btn.className = i === currentPage ? "active" : "";
      btn.addEventListener("click", e => {
        e.preventDefault();
        if (i !== currentPage) showPage(i);
      });
      pagination.appendChild(btn);
    }

    // 다음 페이지 버튼
    const nextBtn = document.createElement("a");
    nextBtn.href = "#";
    nextBtn.textContent = "›";
    // nextBtn.className = currentPage === totalPages ? "disabled" : "";
    nextBtn.addEventListener("click", e => {
      e.preventDefault();
      if (currentPage < totalPages) showPage(currentPage + 1);
    });
    pagination.appendChild(nextBtn);

    // 마지막 페이지 버튼
    const lastBtn = document.createElement("a");
    lastBtn.href = "#";
    lastBtn.textContent = "»";
    // lastBtn.className = currentPage === totalPages ? "disabled" : "";
    lastBtn.addEventListener("click", e => {
      e.preventDefault();
      if (currentPage !== totalPages) showPage(totalPages);
    });
    pagination.appendChild(lastBtn);
  }

  function applyFilters() {
    const searchMode = document.querySelector(".toggle-btn.active")?.dataset.type || "general";

    const keyword = (searchMode === "general" ? generalInput?.value : tagInput?.value || "").toLowerCase().trim();
    const selectedRegion = regionFilter?.value;
    const selectedState = stateFilter?.value;

    const postCards = Array.from(document.querySelectorAll(".post-card"));

    filteredCards = postCards.filter(card => {
      let showCard = true;

      if (keyword) {
        if (searchMode === "general") {
          const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
          const artist = card.querySelector(".artist")?.textContent.toLowerCase() || "";
          showCard = title.includes(keyword) || artist.includes(keyword);
        } else {
          const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.toLowerCase().replace('#', '').trim());
          showCard = tags.some(tag => tag.includes(keyword));
        }
      }

      if (showCard && selectedRegion && selectedRegion !== "") {
        const region = card.querySelector(".region")?.textContent.trim().toLowerCase() || "";
        showCard = region.includes(selectedRegion.toLowerCase());
      }

      if (showCard && selectedState && selectedState !== "") {
        const state = card.querySelector(".post-status")?.textContent.trim() || "";
        showCard = state === selectedState;
      }

      return showCard;
    });

    // 해당게시글없다 문구
      const noResults = document.getElementById("noResultsMessage");
        if (filteredCards.length === 0) {
          noResults.style.display = "block";
        } else {
          noResults.style.display = "none";
        }

    if (filteredCards.length === 0 && !keyword && !selectedRegion && !selectedState) {
      filteredCards = postCards;
    }

    showPage(1);
  }

  // 초기 설정
  filteredCards = Array.from(document.querySelectorAll(".post-card"));

  toggleBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      toggleBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const searchType = this.dataset.type;
      if (searchType === "general") {
        generalInput.style.display = "block";
        tagInput.style.display = "none";
        tagInput.value = "";
      } else {
        generalInput.style.display = "none";
        tagInput.style.display = "block";
        generalInput.value = "";
      }
      applyFilters();
    });
  });

  if (generalInput) generalInput.addEventListener("input", applyFilters);
  if (tagInput) tagInput.addEventListener("input", applyFilters);
  if (regionFilter) regionFilter.addEventListener("change", applyFilters);
  if (stateFilter) stateFilter.addEventListener("change", applyFilters);

  applyFilters();
});
