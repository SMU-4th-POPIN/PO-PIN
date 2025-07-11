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
  const categoryLinks = document.querySelectorAll(".menu ul li a, .girl ul li a, .boy ul li a");
  const postlistContainer = document.querySelector(".postlist");
  const paginationContainer = document.querySelector(".pagination");

  let currentImageIndex = 0;
  let imageList = [];
  let currentPage = 1;
  const postsPerPage = 2;
  let selectedCategory = "전체보기";

  // 신고 버튼
  window.reportBtn = function () {
    alert("신고");
  };

  // 이미지 모달 동작
  document.getElementById("modalPostImages").addEventListener("click", (e) => {
    if (e.target.tagName === "IMG") {
      const clickedSrc = e.target.src;
      imageList = Array.from(document.querySelectorAll("#modalPostImages img")).map(img => img.src);
      currentImageIndex = imageList.indexOf(clickedSrc);
      modalImage.src = clickedSrc;
      imageModal.style.display = "flex";
    }
  });

  imageModal.addEventListener("click", (e) => {
    if (e.target !== modalImage) imageModal.style.display = "none";
  });

  prevBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex - 1 + imageList.length) % imageList.length;
    modalImage.src = imageList[currentImageIndex];
  });

  nextBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex + 1) % imageList.length;
    modalImage.src = imageList[currentImageIndex];
  });

  // 모달 열기
  window.openPostModal = function (artistText, regionText, ptypeText, title, date, place, desc, imgListStr = "", tags = [], wdate = "") {
    document.getElementById("modalPostArtist").textContent = artistText || "";
    document.getElementById("modalPostArtist").className = "artist";
    document.getElementById("modalPostPtype").textContent = ptypeText || "";
    document.getElementById("modalPostPtype").className = "ptype";
    document.getElementById("modalPostRegion").textContent = regionText || "";
    document.getElementById("modalPostRegion").className = "region";
    document.getElementById("modalPostTitle").textContent = title || "";
    document.getElementById("modalPostDate").textContent = `📅 ${date || ""}`;
    document.getElementById("modalPostPlace").textContent = `📍 ${place || ""}`;
    document.getElementById("modalPostDescription").textContent = desc || "";
    document.getElementById("modalPostCreated").textContent = wdate || "";

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
      prevBtn.style.display = nextBtn.style.display = imageList.length > 1 ? "block" : "none";
      imageContainer.style.display = "flex";
    } else {
      imageContainer.style.display = prevBtn.style.display = nextBtn.style.display = "none";
    }

    postModal.style.display = "block";
    topBtn.style.pointerEvents = "none";
    topBtn.style.opacity = "0.4";
  };

  window.closePostModal = () => {
    postModal.style.display = "none";
    topBtn.style.pointerEvents = "auto";
    topBtn.style.opacity = "1";
  };

  window.onclick = (e) => {
    if (e.target === postModal) closePostModal();
  };

  function setupPostCardEvents() {
    document.querySelectorAll(".post-card").forEach(card => {
      card.replaceWith(card.cloneNode(true));
    });
    document.querySelectorAll(".post-card").forEach(card => {
      card.addEventListener("click", (e) => {
        if (e.target.closest(".report-btn, .join-btn, .post-actions")) return;

        const artistText = card.querySelector(".artist")?.textContent.trim() || "";
        const regionText = card.querySelector(".region")?.textContent.trim() || "";
        const ptypeText = card.querySelector(".ptype")?.textContent.trim() || "";
        const title = card.querySelector(".post-title")?.textContent.trim() || "";
        const date = card.querySelector(".info-date span:nth-child(2)")?.textContent.trim() || "";
        const place = card.querySelector(".info-place span:nth-child(2)")?.textContent.trim() || "";
        const desc = card.querySelector(".post-description")?.textContent.trim() || "";
        const wdate = card.querySelector(".post-meta")?.textContent.trim() || "";
        const imgListStr = card.getAttribute("data-imgs") || "";
        const tags = Array.from(card.querySelectorAll(".post-tag")).map(tag => tag.textContent.replace('#', '').trim());

        openPostModal(artistText, regionText, ptypeText, title, date, place, desc, imgListStr, tags, wdate);
      });
    });
  }

  let searchMode = "general";
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      toggleBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      searchMode = btn.dataset.type;
      generalInput.style.display = searchMode === "general" ? "block" : "none";
      tagInput.style.display = searchMode === "tag" ? "block" : "none";
      generalInput.value = tagInput.value = "";
      currentPage = 1;
      applyFilters();
    });
  });

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

  [generalInput, tagInput, stateFilter, sortSelect].forEach(input => {
    if (!input) return;
    input.addEventListener(input.tagName === "SELECT" ? "change" : "input", () => {
      currentPage = 1;
      applyFilters();
    });
  });

  function applyFilters() {
    const keyword = (searchMode === "general" ? generalInput.value : tagInput.value).toLowerCase();
    const selectedState = stateFilter?.value;
    const sortBy = sortSelect?.value;
    const allCards = Array.from(document.querySelectorAll(".post-card"));

    let filteredCards = allCards.filter(card => {
      const title = card.querySelector(".post-title")?.textContent.toLowerCase() || "";
      const tags = Array.from(card.querySelectorAll(".post-tag")).map(t => t.textContent.toLowerCase());
      const stype = card.querySelector(".stype")?.textContent.trim() || card.querySelector(".region")?.textContent.trim();
      const category = card.getAttribute("data-category") || "";

      const matchesSearch = !keyword || (searchMode === "general" ? title.includes(keyword) : tags.some(tag => tag.includes(keyword)));
      const matchesState = !selectedState || selectedState === "전체" || stype === selectedState;
      const matchesCategory = selectedCategory === "전체보기" || category === selectedCategory;

      return matchesSearch && matchesState && matchesCategory;
    });

    if (sortBy === "최신순") {
      filteredCards.sort((a, b) => new Date(b.querySelector(".post-meta")?.textContent) - new Date(a.querySelector(".post-meta")?.textContent));
    } else if (sortBy === "조회순") {
      filteredCards.sort((a, b) => {
        const viewsA = parseInt(a.querySelector(".participants span")?.textContent.replace(/\D/g, "") || "0");
        const viewsB = parseInt(b.querySelector(".participants span")?.textContent.replace(/\D/g, "") || "0");
        return viewsB - viewsA;
      });
    }

    const total = filteredCards.length;
    const start = (currentPage - 1) * postsPerPage;
    const paginated = filteredCards.slice(start, start + postsPerPage);

    allCards.forEach(card => card.style.display = "none");
    paginated.forEach(card => card.style.display = "block");

    if (postlistContainer && paginationContainer) {
      filteredCards.forEach(card => postlistContainer.insertBefore(card, paginationContainer));
    }

    renderPagination(total);
    setupPostCardEvents();
  }

  function renderPagination(totalPosts) {
    if (!paginationContainer) return;

    if (totalPosts <= postsPerPage) {
      paginationContainer.innerHTML = "";
      paginationContainer.style.display = "none";
      return;
    } else {
      paginationContainer.style.display = "flex";
    }

    const totalPages = Math.ceil(totalPosts / postsPerPage);
    if (currentPage > totalPages) currentPage = totalPages;

    paginationContainer.innerHTML = "";
    const createLink = (text, page, isActive = false, isDisabled = false) => {
      const a = document.createElement("a");
      a.href = "#";
      a.textContent = text;
      if (isActive) a.classList.add("active");
      if (isDisabled) a.classList.add("disabled");

      a.addEventListener("click", e => {
        e.preventDefault();
        if (isActive || isDisabled) return;
        currentPage = page;
        applyFilters();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });

      return a;
    };

    paginationContainer.appendChild(createLink("«", 1, false, currentPage === 1));
    paginationContainer.appendChild(createLink("‹", Math.max(currentPage - 1, 1), false, currentPage === 1));

    const maxButtons = 5;
    let start = Math.max(currentPage - Math.floor(maxButtons / 2), 1);
    let end = Math.min(start + maxButtons - 1, totalPages);
    if (end - start < maxButtons - 1) start = Math.max(end - maxButtons + 1, 1);

    for (let i = start; i <= end; i++) {
      paginationContainer.appendChild(createLink(i, i, i === currentPage));
    }

    paginationContainer.appendChild(createLink("›", Math.min(currentPage + 1, totalPages), false, currentPage === totalPages));
    paginationContainer.appendChild(createLink("»", totalPages, false, currentPage === totalPages));
  }

  applyFilters();
  setupPostCardEvents();

  window.addEventListener("scroll", () => {
    topBtn.classList.toggle("show", window.pageYOffset > 300);
  });

  topBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});