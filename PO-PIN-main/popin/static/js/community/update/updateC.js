  let selectedFiles = [];
  let currentRating = 0;
  let selectedExchangeMethod = '';

  document.addEventListener("DOMContentLoaded", function () {
    setupToggleSwitches();
    setupRating();
    setupFileUpload();
    setupButtons();
  });

  // ✅ 파일 크기 포맷 함수 (가장 위에 위치해야 오류 안 남)
  function formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
  }

  function setupToggleSwitches() {
    // 온/오프라인
    const methodMap = {
      onlineToggle: "온라인",
      offlineToggle: "오프라인"
    };
    const methodInput = document.getElementById("methodInput");

    Object.keys(methodMap).forEach(id => {
      const el = document.getElementById(id);
      el.addEventListener("click", () => {
        Object.keys(methodMap).forEach(k => {
          document.getElementById(k).classList.remove("active");


        });
        el.classList.add("active");
        methodInput.value = methodMap[id];
      });
    });

    // 거래 방식
    const transactionMap = {
      saleToggle: "양도",
      exchangeToggle: "교환"
    };
    const transactionInput = document.getElementById("transactionTypeInput");

    Object.keys(transactionMap).forEach(id => {
      const el = document.getElementById(id);
      el.addEventListener("click", () => {
        Object.keys(transactionMap).forEach(k => {
          document.getElementById(k).classList.remove("active");
        });
        el.classList.add("active");
        transactionInput.value = transactionMap[id];
      });
    });
  }

  function setupRating() {
    const stars = document.querySelectorAll('.star');
    const ratingText = document.querySelector('.rating-text');
    const scoreInput = document.getElementById("scoreInput");

    stars.forEach(star => {
      star.addEventListener('click', function () {
        const rating = parseInt(this.dataset.rating);
        currentRating = rating;
        scoreInput.value = rating;

        stars.forEach((s, index) => {
          s.classList.toggle('active', index < rating);
        });



        const ratingTexts = ['매우 불만족', '불만족', '보통', '만족', '매우 만족'];
        ratingText.textContent = `${rating}점 - ${ratingTexts[rating - 1]}`;
      });
    });

    document.querySelector('.rating').addEventListener('mouseleave', () => {
      stars.forEach((s, index) => {
        s.style.color = index < currentRating ? '#FFD700' : '#ddd';
      });
    });
  }

  function setupFileUpload() {
    const fileUploadArea = document.getElementById('fileUploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');

    fileUploadArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function () {
      const files = Array.from(fileInput.files);

      if (selectedFiles.length + files.length > 5) {
        alert("최대 5개까지만 업로드할 수 있습니다.");
        fileInput.value = '';
        return;
      }

      files.forEach(file => {
        selectedFiles.push(file);
        displayFile(file);
      });

      updateFileInput();
    });

    function updateFileInput() {
      const dataTransfer = new DataTransfer();
      selectedFiles.forEach(file => dataTransfer.items.add(file));
      document.getElementById('fileInput').files = dataTransfer.files;
    }

    fileUploadArea.addEventListener('dragover', function (e) {
      e.preventDefault();
      this.classList.add('dragover');
    });

    fileUploadArea.addEventListener('dragleave', function (e) {
      e.preventDefault();
      this.classList.remove('dragover');
    });

    fileUploadArea.addEventListener('drop', function (e) {
      e.preventDefault();
      this.classList.remove('dragover');
      handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
      Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
          if (selectedFiles.length < 5) {
            selectedFiles.push(file);
            displayFile(file);
            updateFileInput();
          } else {
            alert("최대 5개까지만 업로드할 수 있습니다.");
          }
        }
      });
    }
  }


  function displayFile(file) {
    const fileList = document.getElementById('fileList');
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';

    fileItem.innerHTML = `
      <div class="file-info">
        <div class="file-icon">📷</div>
        <div>
          <span class="file-name">${file.name}</span>
          <span class="file-size">${formatFileSize(file.size)}</span>
        </div>
      </div>
      <div class="file-remove" onclick="removeFile('${file.name}')">×</div>
    `;
    fileList.appendChild(fileItem);
  }

  function removeFile(fileName) {
    selectedFiles = selectedFiles.filter(file => file.name !== fileName);
    const fileItems = document.querySelectorAll('.file-item');
    fileItems.forEach(item => {
      if (item.querySelector('.file-name').textContent === fileName) {
        item.remove();
      }
    });

   

    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    document.getElementById('fileInput').files = dataTransfer.files;
  }


  function setupButtons() {
    const writeButton = document.querySelector('button[value="write"]');
    const cancelButton = document.querySelector('button[value="cancel"]');


    writeButton.addEventListener("click", function () {
      const title = document.getElementById("title").value;
      const content = document.getElementById("content").value;
      const partner = document.getElementById("partner").value;


      if (!title || !content || !partner) {
        alert("제목, 후기내용, 교환상대방을 모두 입력해주세요.");
        return;
      }


      if (!document.getElementById("methodInput").value) {
        alert("온/오프라인 방식을 선택해주세요.");
        return;
      }


      if (!document.getElementById("transactionTypeInput").value) {
        alert("거래 방식을 선택해주세요.");
        return;
      }


      if (!document.getElementById("scoreInput").value) {
        alert("총 평점을 선택해주세요.");
        return;
      }

      document.querySelector("form").submit();
    });

    cancelButton.addEventListener("click", function () {
      if (confirm("작성 중인 내용이 모두 삭제됩니다. 정말로 취소하시겠습니까?")) {
        window.location.href = "main.html";
      }
    });
  }