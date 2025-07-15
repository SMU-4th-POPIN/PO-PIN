document.addEventListener("DOMContentLoaded", () => {
  // 요소 선언
  const postModal = document.getElementById("postModal");
  const modalImage = document.getElementById("modalImage");
  const imageModal = document.getElementById("imageModal");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const topBtn = document.getElementById("topBtn");
  const sortSelect = document.getElementById("sortSelect") || document.getElementById("sortFilter");
  const generalInput = document.getElementById("generalSearch");
  const tagInput = document.getElementById("tagSearch");
  const stateFilter = document.getElementById("stateFilter") || document.getElementById("regionFilter");
  const toggleBtns = document.querySelectorAll(".toggle-btn");
  const categoryLinks = document.querySelectorAll(".menu ul li a");
  const postlistContainer = document.querySelector(".postlist");
  const paginationContainer = document.querySelector(".pagination");

  let currentImageIndex = 0;
  let imageList = [];
  let currentPage = 1;
  const postsPerPage = 2;
  let selectedCategory = "전체보기";
  let searchMode = "general";

  // 신고 버튼
  window.reportBtn = function () {
    alert("신고");
  };

  // 이미지 모달 동작 (안전한 접근)
  const modalPostImages = document.getElementById("modalPostImages");
  if (modalPostImages) {
    modalPostImages.addEventListener("click", (e) => {
      if (e.target.tagName === "IMG") {
        const clickedSrc = e.target.src;
        imageList = Array.from(modalPostImages.querySelectorAll("img")).map(img => img.src);
        currentImageIndex = imageList.indexOf(clickedSrc);
        if (modalImage) {
          modalImage.src = clickedSrc;
          imageModal.style.display = "flex";
        }
      }
    });
  }

  if (imageModal) {
    imageModal.addEventListener("click", (e) => {
      if (e.target !== modalImage) imageModal.style.display = "none";
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
      if (modalImage) modalImage.src = imageList[currentImageIndex];
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      currentImageIndex = (currentImageIndex + 1) % imageList.length;
      if (modalImage) modalImage.src = imageList[currentImageIndex];
    });
  }

  // 모달 열기
  window.openPostModal = function (artistText, regionText, ptypeText, title, date, place, desc, imgListStr = "", tags = [], wdate = "") {
    const modalPostArtist = document.getElementById("modalPostArtist");
    const modalPostPtype = document.getElementById("modalPostPtype");
    const modalPostRegion = document.getElementById("modalPostRegion");
    const modalPostTitle = document.getElementById("modalPostTitle");
    const modalPostDate = document.getElementById("modalPostDate");
    const modalPostPlace = document.getElementById("modalPostPlace");
    const modalPostDescription = document.getElementById("modalPostDescription");
    const modalPostCreated = document.getElementById("modalPostCreated");

    if (modalPostArtist) {
      modalPostArtist.textContent = artistText || "";
      modalPostArtist.className = "artist";
    }
    if (modalPostPtype) {
      modalPostPtype.textContent = ptypeText || "";
      modalPostPtype.className = "ptype";
    }
    if (modalPostRegion) {
      modalPostRegion.textContent = regionText || "";
      modalPostRegion.className = "region";
    }
    if (modalPostTitle) modalPostTitle.textContent = title || "";
    if (modalPostDate) modalPostDate.textContent = `📅 ${date || ""}`;
    if (modalPostPlace) modalPostPlace.textContent = `📍 ${place || ""}`;
    if (modalPostDescription) modalPostDescription.textContent = desc || "";
    if (modalPostCreated) modalPostCreated.textContent = wdate || "";

    const tagsContainer = document.getElementById("modalPostTags");
    if (tagsContainer) {
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
    }

    const imageContainer = document.getElementById("modalPostImages");
    if (imageContainer) {
      imageContainer.innerHTML = "";
      if (imgListStr) {
        imageList = imgListStr.split(",").map(url => url.trim());
        imageList.forEach(url => {
          const img = document.createElement("img");
          img.src = url;
          img.alt = "첨부 이미지";
          Object.assign(img.style, {
            width: "100px", height: "100px", objectFit: "cover", borderRadius: "10px"
          });
          imageContainer.appendChild(img);
        });
        if (prevBtn && nextBtn) {
          prevBtn.style.display = nextBtn.style.display = imageList.length > 1 ? "block" : "none";
        }
        imageContainer.style.display = "flex";
      } else {
        imageContainer.style.display = "none";
        if (prevBtn && nextBtn) {
          prevBtn.style.display = nextBtn.style.display = "none";
        }
      }
    }

    if (postModal) {
      postModal.style.display = "block";
    }
    if (topBtn) {
      topBtn.style.pointerEvents = "none";
      topBtn.style.opacity = "0.4";
    }
  };

  window.closePostModal = () => {
    if (postModal) postModal.style.display = "none";
    if (topBtn) {
      topBtn.style.pointerEvents = "auto";
      topBtn.style.opacity = "1";
    }
  };

  window.onclick = (e) => {
    if (e.target === postModal) closePostModal();
  };

  function setupPostCardEvents() {
    document.querySelectorAll(".post-card").forEach(card => {
      // 기존 이벤트 리스너 제거를 위해 복제
      const newCard = card.cloneNode(true);
      card.parentNode.replaceChild(newCard, card);
    });
    
    document.querySelectorAll(".post-card").forEach(card => {
      card.addEventListener("click", (e) => {
        if (e.target.closest(".report-btn, .join-btn, .post-actions")) return;

        const artistText = card.querySelector(".artist")?.textContent.trim() || "";
        const regionText = card.querySelector(".region")?.textContent.trim() || "";
        const ptypeText = card.querySelector(".ptype")?.textContent.trim() || "";
        const title = card.querySelector(".post-title")?.textContent.trim() || "";
        const dateElement = card.querySelector(".info-date span:nth-child(2)");
        const date = dateElement ? dateElement.textContent.trim() : "";
        const placeElement = card.querySelector(".info-place span:nth-child(2)");
        const place = placeElement ? placeElement.textContent.trim() : "";
        const desc = card.querySelector(".post-content")?.textContent.trim() || 
                 card.querySelector(".post-description")?.textContent.trim();
        const wdate = card.querySelector(".post-meta")?.textContent.trim() || "";
        const imgListStr = card.getAttribute("data-imgs") || "";
        const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

        openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr, tags, wdate);
      });
    });
  }

  // 검색 모드 토글 버튼 이벤트
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      
      if (btn.classList.contains("active")) {
        return;
      }
      
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      searchMode = btn.dataset.type;
      
      if (searchMode === "general") {
        if (generalInput) {
          generalInput.style.display = "block";
        }
        if (tagInput) {
          tagInput.style.display = "none";
          tagInput.value = "";
        }
      } else {
        if (generalInput) {
          generalInput.style.display = "none";
          generalInput.value = "";
        }
        if (tagInput) {
          tagInput.style.display = "block";
        }
      }
      
      currentPage = 1;
      applyFilters();
    });
  });

  // 카테고리 링크 이벤트
  categoryLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      categoryLinks.forEach(l => l.parentElement.classList.remove("active"));
      link.parentElement.classList.add("active");
      selectedCategory = link.dataset.category || "전체보기";
      currentPage = 1;
      applyFilters();
    });
  });

  // 입력 필드 이벤트 리스너
  if (generalInput) {
    generalInput.addEventListener("input", () => {
      if (searchMode === "general") {
        currentPage = 1;
        applyFilters();
      }
    });
  }

  if (tagInput) {
    tagInput.addEventListener("input", () => {
      if (searchMode === "tag") {
        currentPage = 1;
        applyFilters();
      }
    });
  }

  if (stateFilter) {
    stateFilter.addEventListener("change", () => {
      currentPage = 1;
      applyFilters();
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      currentPage = 1;
      applyFilters();
    });
  }

  function applyFilters() {
    const keyword = (searchMode === "general" ? 
      (generalInput ? generalInput.value : "") : 
      (tagInput ? tagInput.value : "")
    ).toLowerCase();
    
    const selectedState = stateFilter?.value;
    const sortBy = sortSelect?.value;
    const allCards = Array.from(document.querySelectorAll(".post-card"));

    let filteredCards = allCards.filter(card => {
      const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
      const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.toLowerCase());
      const stype = card.querySelector(".stype")?.textContent.trim() || card.querySelector(".region")?.textContent.trim();
      const category = card.getAttribute("data-category") || "";

      const matchesSearch = !keyword || (searchMode === "general" ? 
        title.includes(keyword) : 
        tags.some(tag => tag.includes(keyword)));
      const matchesState = !selectedState || selectedState === "전체" || selectedState === "" || stype === selectedState;
      const matchesCategory = selectedCategory === "전체보기" || category === selectedCategory;

      return matchesSearch && matchesState && matchesCategory;
    });

    // 정렬
    if (sortBy === "최신순") {
      filteredCards.sort((a, b) => {
        const dateA = a.querySelector(".post-meta")?.getAttribute("data-date") || a.querySelector(".post-meta")?.textContent;
        const dateB = b.querySelector(".post-meta")?.getAttribute("data-date") || b.querySelector(".post-meta")?.textContent;
        return new Date(dateB) - new Date(dateA);
      });
    } else if (sortBy === "조회순") {
      filteredCards.sort((a, b) => {
        const viewsA = parseInt(a.querySelector(".participants span")?.textContent.replace(/\D/g, "") || "0");
        const viewsB = parseInt(b.querySelector(".participants span")?.textContent.replace(/\D/g, "") || "0");
        return viewsB - viewsA;
      });
    }

    const total = filteredCards.length;
    const totalPages = Math.ceil(total / postsPerPage);
    
    // 현재 페이지가 총 페이지를 초과하면 조정
    if (currentPage > totalPages && totalPages > 0) {
      currentPage = totalPages;
    }
    
    const start = (currentPage - 1) * postsPerPage;
    const paginated = filteredCards.slice(start, start + postsPerPage);

    // 모든 카드 숨기기
    allCards.forEach(card => card.style.display = "none");
    
    // 현재 페이지 카드만 보이기
    paginated.forEach(card => card.style.display = "block");

    renderPagination(total);
    setupPostCardEvents();

    // 결과 없음 메시지
    const noResultsMessage = document.getElementById("noResultsMessage");
    if (noResultsMessage) {
      if (filteredCards.length === 0) {
        noResultsMessage.textContent = "해당 게시물이 없습니다.";
        noResultsMessage.style.display = "block";
      } else {
        noResultsMessage.style.display = "none";
      }
    }
  }

  function renderPagination(totalPosts) {
    if (!paginationContainer) return;

    const totalPages = Math.ceil(totalPosts / postsPerPage);
    
    if (totalPosts <= postsPerPage || totalPages <= 1) {
      paginationContainer.innerHTML = "";
      paginationContainer.style.display = "none";
      return;
    }
    
    paginationContainer.style.display = "flex";
    paginationContainer.innerHTML = "";

    const createLink = (text, page, isActive = false, isDisabled = false) => {
      const a = document.createElement("a");
      a.href = "#";
      a.textContent = text;
      
      if (isActive) {
        a.classList.add("active");
        // active 클래스 대신 strong 태그 사용
        const strong = document.createElement("strong");
        strong.textContent = text;
        paginationContainer.appendChild(strong);
        return strong;
      }
      
      if (isDisabled) a.classList.add("disabled");

      a.addEventListener("click", (e) => {
        e.preventDefault();
        if (isDisabled) return;
        currentPage = page;
        applyFilters();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });

      return a;
    };

    // 첫 페이지
    paginationContainer.appendChild(createLink("«", 1, false, currentPage === 1));
    
    // 이전 페이지
    paginationContainer.appendChild(createLink("‹", Math.max(currentPage - 1, 1), false, currentPage === 1));

    // 페이지 번호들
    const maxButtons = 5;
    let start = Math.max(currentPage - Math.floor(maxButtons / 2), 1);
    let end = Math.min(start + maxButtons - 1, totalPages);
    if (end - start < maxButtons - 1) {
      start = Math.max(end - maxButtons + 1, 1);
    }

    for (let i = start; i <= end; i++) {
      paginationContainer.appendChild(createLink(i.toString(), i, i === currentPage));
    }

    // 다음 페이지
    paginationContainer.appendChild(createLink("›", Math.min(currentPage + 1, totalPages), false, currentPage === totalPages));
    
    // 마지막 페이지
    paginationContainer.appendChild(createLink("»", totalPages, false, currentPage === totalPages));
  }

  // 초기 상태 설정
  if (generalInput) generalInput.style.display = "block";
  if (tagInput) tagInput.style.display = "none";
  
  // 초기 카테고리 활성화
  const firstCategoryLink = categoryLinks[0];
  if (firstCategoryLink) {
    firstCategoryLink.parentElement.classList.add("active");
  }
  
  applyFilters();
  setupPostCardEvents();

  // 스크롤 이벤트
  if (topBtn) {
    window.addEventListener("scroll", () => {
      topBtn.classList.toggle("show", window.pageYOffset > 300);
    });

    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});