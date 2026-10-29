/**
 * Tevfik İleri İHO Soru Hazırlama & Soru Bankası Sistemi
 * Frontend Uygulama Mantığı (Gelişmiş Çoklu Sayfalama & Soru Bankası Entegrasyonu)
 */

// Uygulama Durumu (State)
const state = {
  user: null,
  config: {},
  curriculum: {},
  currentExam: {
    id: null,
    title: "Din Kültürü ve Ahlak Bilgisi 1. Yazılı",
    exam_type: "yazili_sinav", // 'yazili_sinav', 'etut_calisma', 'yaprak_test'
    subject: "dkab",
    subject_name: "Din Kültürü ve Ahlak Bilgisi",
    grade: 5,
    term: "1. Dönem",
    exam_no: "1. Yazılı",
    scenario: "Senaryo 1",
    layout: "2_column", // "2_column" veya "1_column"
    total_points: 100,
    questions: []
  },
  activeTab: "exam", // "exam", "answer_key", "source_verification"
  currentView: "exam_maker", // "exam_maker" veya "question_bank"
  savedExams: [],
  questionBankItems: [],
  isLoading: false
};

// --- BAŞLANGIÇ ---
document.addEventListener("DOMContentLoaded", async () => {
  await loadConfig();
  await loadCurriculum();
  checkAuth();
  setupEventListeners();
  loadSavedExamsList();
  
  // Başlangıçta canlı başlıkları ayarla
  updatePaperHeaderLive();
  
  // 15 Saniyede Bir Otomatik Taslak Kaydetme Motorunu Başlat
  startAutoSaveEngine();

  // Varsa önceki oturumdan kalan taslağı geri yükle (Veri Kaybı Önleme)
  await checkAndRestoreDraft();
});

// --- AYARLAR VE VERİ YÜKLEME ---
async function loadConfig() {
  try {
    const res = await fetch("/api/config");
    state.config = await res.json();
    updateSchoolHeaderDisplay();
  } catch (e) {
    console.error("Config yüklenemedi:", e);
  }
}

async function loadCurriculum() {
  try {
    const res = await fetch("/api/curriculum");
    state.curriculum = await res.json();
    populateCurriculumUI();
  } catch (e) {
    console.error("Müfredat yüklenemedi:", e);
  }
}

function updateSchoolHeaderDisplay() {
  const elHeader = document.getElementById("headerSchoolTitle");
  if (elHeader) {
    elHeader.textContent = state.config.school_name || "Tevfik İleri İmam Hatip Ortaokulu";
  }
  const elGreeting = document.getElementById("userGreeting");
  if (elGreeting) {
    elGreeting.textContent = `Hoş Geldiniz, ${state.config.teacher_name || "Öğretmenim"}`;
  }
}

// Canlı Başlık Güncelleyici
function updatePaperHeaderLive() {
  const subjectSelect = document.getElementById("examSubject");
  const subjectId = subjectSelect ? subjectSelect.value : state.currentExam.subject;
  const subjName = (state.curriculum[subjectId] && state.curriculum[subjectId].name) 
                   ? state.curriculum[subjectId].name 
                   : "DİN KÜLTÜRÜ VE AHLAK BİLGİSİ";
  
  const grade = document.getElementById("examGrade") ? document.getElementById("examGrade").value : state.currentExam.grade;
  const term = document.getElementById("examTerm") ? document.getElementById("examTerm").value : state.currentExam.term;
  const exam_no = document.getElementById("examNo") ? document.getElementById("examNo").value : state.currentExam.exam_no;
  const scenario = document.getElementById("examScenario") ? document.getElementById("examScenario").value : state.currentExam.scenario;
  const exam_type = document.getElementById("examTypeSelect") ? document.getElementById("examTypeSelect").value : state.currentExam.exam_type;

  state.currentExam.subject = subjectId;
  state.currentExam.subject_name = subjName;
  state.currentExam.grade = parseInt(grade, 10);
  state.currentExam.term = term || "1. Dönem";
  state.currentExam.exam_no = exam_no || "1. Yazılı";
  state.currentExam.scenario = scenario || "Senaryo 1";
  state.currentExam.exam_type = exam_type || "yazili_sinav";
}

// --- KULLANICI GİRİŞ (AUTH) ---
function checkAuth() {
  const savedUser = localStorage.getItem("ti_user");
  if (savedUser) {
    try {
      state.user = JSON.parse(savedUser);
      showApp();
      return;
    } catch (e) {}
  }
  showLogin();
}

function showLogin() {
  document.getElementById("loginScreen").classList.remove("hidden");
  document.getElementById("mainAppScreen").classList.add("hidden");
}

function showApp() {
  document.getElementById("loginScreen").classList.add("hidden");
  document.getElementById("mainAppScreen").classList.remove("hidden");
  updateSchoolHeaderDisplay();
}

async function handleLogin(e) {
  e.preventDefault();
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value.trim();
  const errEl = document.getElementById("loginError");
  errEl.classList.add("hidden");

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Giriş başarısız.");
    }
    const data = await res.json();
    state.user = data.user;
    localStorage.setItem("ti_user", JSON.stringify(data.user));
    showApp();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove("hidden");
  }
}

function handleLogout() {
  localStorage.removeItem("ti_user");
  state.user = null;
  showLogin();
}

// ==============================================================
// OTOMATİK TASLAK KAYIT MOTORU (15 SANİYEDE BİR ÇALIŞIR)
// Soru hazırlandığında 1 defa hemen kaydeder, sonra her 15 saniyede
// bir arka planda sessizce taslak alır; olası kapanmalarda sıfır veri kaybı!
// ==============================================================
let _autoSaveTimer = null;
let _isDraftDirty = false;

function startAutoSaveEngine() {
  if (_autoSaveTimer) clearInterval(_autoSaveTimer);
  _autoSaveTimer = setInterval(async () => {
    if (state.currentExam && state.currentExam.questions && state.currentExam.questions.length > 0) {
      await saveDraft(false); // Sessiz periyodik kayıt
    }
  }, 15000); // Tam 15 saniyede bir
}

async function saveDraft(showVisualIndicator = true) {
  if (!state.currentExam || !state.currentExam.questions || state.currentExam.questions.length === 0) {
    return;
  }

  const indicator = document.getElementById("autoSaveIndicator");
  const indicatorText = document.getElementById("autoSaveText");
  const now = new Date();
  const timeStr = now.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });

  try {
    // 1. Tarayıcı Yerel Belleğine Anında Kaydet (Sıfır milisaniye)
    localStorage.setItem("ti_active_draft", JSON.stringify(state.currentExam));

    // 2. Sunucuya Arka Planda Sessizce Kaydet
    fetch("/api/draft", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state.currentExam)
    }).catch(e => console.warn("Backend draft save warning:", e));

    if (indicator && indicatorText) {
      indicator.classList.remove("hidden");
      indicatorText.textContent = `Taslak Korundu (${timeStr})`;
    }
  } catch (e) {
    console.error("Taslak kaydetme hatası:", e);
  }
}

async function checkAndRestoreDraft() {
  // 1. Önce localStorage kontrolü
  let draftData = null;
  const localDraft = localStorage.getItem("ti_active_draft");
  if (localDraft) {
    try {
      draftData = JSON.parse(localDraft);
    } catch (e) {}
  }

  // 2. localStorage boşsa backend /api/draft kontrolü
  if (!draftData || !draftData.questions || draftData.questions.length === 0) {
    try {
      const res = await fetch("/api/draft");
      const data = await res.json();
      if (data.status === "success" && data.draft && data.draft.questions) {
        draftData = data.draft;
      }
    } catch (e) {}
  }

  // Eğer geçerli bir taslak varsa geri yükle
  if (draftData && draftData.questions && draftData.questions.length > 0) {
    state.currentExam = draftData;
    
    // Sol panel kontrollerini taslağa göre senkronize et
    if (document.getElementById("examSubject") && draftData.subject) {
      document.getElementById("examSubject").value = draftData.subject;
    }
    if (document.getElementById("examGrade") && draftData.grade) {
      document.getElementById("examGrade").value = draftData.grade;
    }
    if (document.getElementById("examTerm") && draftData.term) {
      document.getElementById("examTerm").value = draftData.term;
    }
    if (document.getElementById("examNo") && draftData.exam_no) {
      document.getElementById("examNo").value = draftData.exam_no;
    }
    if (document.getElementById("examQuestionCount")) {
      document.getElementById("examQuestionCount").value = draftData.questions.length;
    }

    recalculateTotalPoints();
    renderExamPages();

    const indicator = document.getElementById("autoSaveIndicator");
    const indicatorText = document.getElementById("autoSaveText");
    if (indicator && indicatorText) {
      indicator.classList.remove("hidden");
      indicatorText.textContent = "Taslak Geri Yüklendi";
    }

    showToast("Önceki oturumunuzdan kalan taslak sınav otomatik olarak geri yüklendi (Veri kaybı önlendi).", "success");
  } else {
    renderExamPages();
  }
}

// --- MÜFREDAT VE FORM KONTROLLERİ ---
function populateCurriculumUI() {
  const subjectSelect = document.getElementById("examSubject");
  if (!subjectSelect) return;
  subjectSelect.innerHTML = "";
  
  for (const [id, data] of Object.entries(state.curriculum)) {
    const opt = document.createElement("option");
    opt.value = id;
    opt.textContent = data.name;
    subjectSelect.appendChild(opt);
  }
  onSubjectOrGradeChange();
}

function onSubjectOrGradeChange() {
  const subjectId = document.getElementById("examSubject").value;
  const grade = parseInt(document.getElementById("examGrade").value, 10);
  const unitsContainer = document.getElementById("unitsContainer");
  unitsContainer.innerHTML = "";

  if (state.curriculum[subjectId] && state.curriculum[subjectId].grades[grade]) {
    const units = state.curriculum[subjectId].grades[grade].units;
    units.forEach((u, idx) => {
      const div = document.createElement("div");
      div.className = "flex items-start space-x-2 text-xs py-1 px-1.5 hover:bg-slate-100 rounded";
      div.innerHTML = `
        <input type="checkbox" id="unit_${u.id}" value="${u.id}" class="unit-checkbox mt-0.5 rounded text-blue-600 focus:ring-blue-500" ${idx === 0 ? "checked" : ""}>
        <label for="unit_${u.id}" class="text-slate-700 cursor-pointer font-medium select-none">
          ${u.name}
          <span class="block text-[10px] text-slate-400 font-normal">Konular: ${u.topics.slice(0, 3).join(", ")}...</span>
        </label>
      `;
      unitsContainer.appendChild(div);
    });
  }
  updatePaperHeaderLive();
}

function onScenarioChange() {
  const scenario = document.getElementById("examScenario").value;
  const qCountInput = document.getElementById("examQuestionCount");
  if (scenario === "Senaryo 1") {
    qCountInput.value = 6;
  } else if (scenario === "Senaryo 2") {
    qCountInput.value = 8;
  }
  updatePaperHeaderLive();
}

// --- SINAV HAZIRLAMA (API İSTEĞİ) ---
async function handleGenerateExam() {
  const subject = document.getElementById("examSubject").value;
  const grade = parseInt(document.getElementById("examGrade").value, 10);
  const term = document.getElementById("examTerm").value;
  const exam_no = document.getElementById("examNo").value;
  const scenario = document.getElementById("examScenario").value;
  const question_count = parseInt(document.getElementById("examQuestionCount").value, 10) || 6;
  const difficulty = document.getElementById("examDifficulty").value;
  const exam_type = document.getElementById("examTypeSelect").value;

  const checkedUnits = Array.from(document.querySelectorAll(".unit-checkbox:checked")).map(cb => cb.value);

  setLoading(true, "MEB Kitapları taranıyor ve sorular hazırlanıyor...");

  try {
    const res = await fetch("/api/generate-exam", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject,
        grade,
        exam_type,
        term,
        exam_no,
        scenario,
        question_count,
        selected_units: checkedUnits,
        difficulty
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Soru hazırlama başarısız.");
    }

    const data = await res.json();
    const questions = data.data.questions || [];

    const subjName = state.curriculum[subject]?.name || subject;
    state.currentExam = {
      id: null,
      title: `${grade}. Sınıf ${subjName} ${term} ${exam_no}`,
      exam_type,
      subject,
      subject_name: subjName,
      grade,
      term,
      exam_no,
      scenario,
      layout: state.currentExam.layout || "2_column",
      total_points: 100,
      questions
    };

    recalculateTotalPoints();
    renderExamPages();
    
    // Soru hazırlandığında 1 defa ANINDA taslak kaydet (Kullanıcı Talebi)
    await saveDraft(true);

    showToast("Sınav ve sorular başarıyla hazırlandı!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

// ==============================================================
// GELİŞMİŞ ÇOKLU SAYFALAMA MOTORU (PAGINATION ENGINE)
// 10 soru gibi uzun sınavlarda sorular asla kağıt dışına taşmaz!
// Otomatik olarak Sayfa 1, Sayfa 2 vb. bağımsız A4 kağıtları üretir.
// ==============================================================
function renderExamPages() {
  const container = document.getElementById("examPagesContainer");
  if (!container) return;
  container.innerHTML = "";

  const exam = state.currentExam;
  const questions = exam.questions || [];

  if (questions.length === 0) {
    container.innerHTML = `
      <div class="a4-sheet flex flex-col justify-center items-center text-slate-400">
        <div class="text-5xl mb-3">📝</div>
        <div class="font-bold text-base text-slate-700">Henüz Soru Hazırlanmadı</div>
        <div class="text-xs text-slate-500 mt-1 max-w-sm text-center">
          Sol menüden ders, sınıf ve soru adedini belirleyip <strong>"Sınavı Hazırla"</strong> butonuna basınız.
        </div>
      </div>
    `;
    renderAnswerKeySheet();
    renderSourceVerificationSheet();
    return;
  }

  // Sayfalama Limiti Hesabı:
  // 2 sütunlu düzende 1 sayfaya en fazla 4 ila 5 soru sığar.
  // 1 sütunlu düzende 1 sayfaya en fazla 3 soru sığar.
  const is2Col = (exam.layout === "2_column");
  const questionsPerPage = is2Col ? 5 : 3;
  const totalPages = Math.ceil(questions.length / questionsPerPage);

  for (let pageIdx = 0; pageIdx < totalPages; pageIdx++) {
    const pageQuestions = questions.slice(pageIdx * questionsPerPage, (pageIdx + 1) * questionsPerPage);
    const sheetDiv = document.createElement("div");
    sheetDiv.className = "a4-sheet";
    sheetDiv.dataset.pageNumber = pageIdx + 1;

    // 1. Sayfa MEB Resmi Anteti; 2. ve sonraki sayfalar için Devam Başlığı
    let headerHtml = "";
    if (pageIdx === 0) {
      const typeTitle = exam.exam_type === "etut_calisma" ? "ÇALIŞMA VE ETÜT KAĞIDI" 
                      : exam.exam_type === "yaprak_test" ? "KAZANIM DEĞERLENDİRME TESTİ" 
                      : `${(exam.term || "1. Dönem").toUpperCase()} ${(exam.exam_no || "1. Yazılı").toUpperCase()} SINAVI (${(exam.scenario || "Senaryo 1").toUpperCase()})`;

      headerHtml = `
        <div class="meb-header">
          <h3>${state.config.school_header || "T.C. MİLLÎ EĞİTİM BAKANLIĞI"}</h3>
          <h3>${state.config.school_name || "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu"}</h3>
          <h4>2025-2026 EĞİTİM ÖĞRETİM YILI ${exam.grade}. SINIF ${(exam.subject_name || "DİN KÜLTÜRÜ").toUpperCase()} DERSİ</h4>
          <div class="exam-sub">${typeTitle}</div>
        </div>

        <table class="student-info-table">
          <tr>
            <td class="label">Adı Soyadı:</td>
            <td class="val">..................................................................</td>
            <td class="label">ALDIĞI NOT:</td>
            <td class="score-box">
              <span class="text-slate-400">....</span> / <span id="sheetTotalPoints">${exam.total_points || 100}</span>
            </td>
          </tr>
          <tr>
            <td class="label">Sınıfı / No:</td>
            <td class="val">${exam.grade} / ..... &nbsp;&nbsp;&nbsp;&nbsp; No: ................</td>
            <td class="label">Tarih / İmza:</td>
            <td class="val text-center text-[8.5pt]">..... / ..... / 2026</td>
          </tr>
        </table>
      `;
    } else {
      headerHtml = `
        <div class="meb-header-continuation">
          <span>${state.config.school_name || "Tevfik İleri İmam Hatip Ortaokulu"}</span>
          <span>${exam.grade}. Sınıf ${(exam.subject_name || "Ders").toUpperCase()} • (Sayfa ${pageIdx + 1} / ${totalPages})</span>
        </div>
      `;
    }

    // Soruların Yerleşimi (2 Sütun veya 1 Sütun)
    let questionsHtml = "";
    if (is2Col) {
      const mid = Math.ceil(pageQuestions.length / 2);
      const col1 = pageQuestions.slice(0, mid);
      const col2 = pageQuestions.slice(mid);

      const renderCol = (list, offset) => list.map((q, idx) => createQuestionCardHtml(q, pageIdx * questionsPerPage + offset + idx)).join("");

      questionsHtml = `
        <div class="exam-layout-2col">
          <div class="column-container">${renderCol(col1, 0)}</div>
          <div class="column-container">${renderCol(col2, mid)}</div>
        </div>
      `;
    } else {
      questionsHtml = `
        <div class="exam-layout-1col">
          ${pageQuestions.map((q, idx) => createQuestionCardHtml(q, pageIdx * questionsPerPage + idx)).join("")}
        </div>
      `;
    }

    // Alt Bilgi
    const footerHtml = `
      <div class="exam-footer">
        <span>Sınav süresi 40 dakikadır. Başarılar dilerim.</span>
        <span>Sayfa ${pageIdx + 1} / ${totalPages}</span>
      </div>
    `;

    sheetDiv.innerHTML = headerHtml + questionsHtml + footerHtml;
    container.appendChild(sheetDiv);
  }

  // Diğer sekmeleri de güncelle
  renderAnswerKeySheet();
  renderSourceVerificationSheet();
}

// Cevap Uzunluğuna Göre Dengeli Çizgi Sayısı Hesaplayıcı (Kullanıcı Talebi)
function calculateOptimalAnswerLines(q) {
  if (q.options && q.options.length > 0) return 0;
  
  const ans = (q.answer_text || "").trim();
  const newlineCount = (ans.match(/\n/g) || []).length + 1;
  const charCount = ans.length;

  if (charCount > 300 || newlineCount >= 4) {
    return 4; // Uzun ve maddeli analiz soruları
  } else if (charCount > 100 || newlineCount >= 2) {
    return 3; // Orta uzunlukta sorular
  } else {
    return 3; // Kısa cevaplı sorular
  }
}

function createQuestionCardHtml(q, index) {
  const arabicHtml = q.arabic_text ? `<div class="arabic-text" contenteditable="true" onblur="updateArabicText(${index}, this.innerText)">${q.arabic_text}</div>` : "";
  
  // Çoktan seçmeli test şıkları varsa göster
  let optionsHtml = "";
  if (q.options && Array.isArray(q.options) && q.options.length > 0) {
    optionsHtml = `
      <div class="options-list">
        ${q.options.map(opt => `<div class="p-1 bg-slate-50 border rounded text-[8pt]">${opt}</div>`).join("")}
      </div>
    `;
  }

  // Cevap anahtarındaki çözüm uzunluğuna göre dengelenmiş satır sayısı
  const optimalLines = calculateOptimalAnswerLines(q);
  let answerLinesHtml = "";
  if (optimalLines > 0) {
    let linesDotted = "";
    for (let l = 0; l < optimalLines; l++) {
      linesDotted += `<div class="answer-line"></div>`;
    }
    answerLinesHtml = `
      <div class="answer-space">
        <div class="answer-header-row">
          <span class="text-[7.5pt] text-slate-400 font-semibold">Cevap:</span>
        </div>
        ${linesDotted}
      </div>
    `;
  }

  return `
    <div class="question-item" data-index="${index}">
      <div class="question-header">
        <div class="flex items-center gap-1.5">
          <span class="question-badge">Soru ${index + 1})</span>
          <div class="flex items-center text-[10px] font-bold text-blue-900 bg-blue-50 px-1 py-0.2 rounded border border-blue-200">
            <input type="number" min="1" max="100" value="${q.points || 10}" 
                   class="question-points-input" 
                   onchange="updateQuestionPoints(${index}, this.value)">
            <span class="ml-0.5 text-[9px]">P</span>
          </div>
        </div>
        <div class="q-actions no-print">
          <button type="button" class="q-btn" title="Bu soruyu yapay zeka ile yeniden üret" onclick="regenerateSingleQuestion(${index})">
            🔄 Yenile
          </button>
          <button type="button" class="q-btn delete" title="Soruyu Sil" onclick="deleteQuestion(${index})">
            🗑️ Sil
          </button>
        </div>
      </div>

      ${q.learning_outcome ? `<span class="outcome-tag no-print">Kazanım: ${q.learning_outcome}</span>` : ""}
      ${arabicHtml}

      <div class="question-text-editable" contenteditable="true" onblur="updateQuestionText(${index}, this.innerText)">
        ${q.question_text || ""}
      </div>

      ${optionsHtml}
      ${answerLinesHtml}
    </div>
  `;
}

// --- TEK MERKEZLİ GÜNCELLEMELER ---
function updateQuestionText(idx, newText) {
  if (state.currentExam.questions[idx]) {
    state.currentExam.questions[idx].question_text = newText.trim();
    renderAnswerKeySheet();
    renderSourceVerificationSheet();
    saveDraft(false); // Canlı taslağa anında kaydet
  }
}

function updateArabicText(idx, newText) {
  if (state.currentExam.questions[idx]) {
    state.currentExam.questions[idx].arabic_text = newText.trim();
    saveDraft(false);
  }
}

function updateQuestionPoints(idx, newPoints) {
  const pts = parseInt(newPoints, 10) || 0;
  if (state.currentExam.questions[idx]) {
    state.currentExam.questions[idx].points = pts;
    recalculateTotalPoints();
    saveDraft(false);
  }
}

function recalculateTotalPoints() {
  const total = state.currentExam.questions.reduce((sum, q) => sum + (parseInt(q.points, 10) || 0), 0);
  state.currentExam.total_points = total;
  const badge = document.getElementById("sheetTotalPoints");
  if (badge) badge.textContent = total;
  const topTotal = document.getElementById("topTotalPointsBadge");
  if (topTotal) topTotal.textContent = `${total} P`;
}

function deleteQuestion(idx) {
  if (confirm("Bu soruyu silmek istediğinize emin misiniz?")) {
    state.currentExam.questions.splice(idx, 1);
    state.currentExam.questions.forEach((q, i) => q.q_order = i + 1);
    
    // Sol panel soru sayısını senkronize et
    const qCountInput = document.getElementById("examQuestionCount");
    if (qCountInput) qCountInput.value = state.currentExam.questions.length;

    recalculateTotalPoints();
    renderExamPages();
  }
}

function addNewQuestion() {
  const newQ = {
    q_order: state.currentExam.questions.length + 1,
    points: 10,
    learning_outcome: "Öğretmen tarafından eklenen soru",
    question_type: state.currentExam.exam_type === "yaprak_test" ? "coktan_secmeli" : "acik_uclu",
    cognitive_level: "Yorumlama",
    difficulty: "Orta",
    source_book: `${state.currentExam.grade}. Sınıf ${state.currentExam.subject_name} Ders Kitabı`,
    source_page: "Öğretmen Belirlemesi",
    source_context: "Öğretmenin derste vurguladığı özel konu veya kazanım.",
    arabic_text: "",
    question_text: "Yeni sorunuzu buraya yazınız...",
    options: state.currentExam.exam_type === "yaprak_test" ? ["A) Seçenek 1", "B) Seçenek 2", "C) Seçenek 3", "D) Seçenek 4"] : [],
    answer_text: "Beklenen örnek cevap / çözüm...",
    rubric: [
      { criterion: "Doğru açıklama ve gerekçelendirme", points: 10 }
    ]
  };

  state.currentExam.questions.push(newQ);
  
  // Sol paneldeki soru sayısı inputunu güncelle (Kullanıcı talebi)
  const qCountInput = document.getElementById("examQuestionCount");
  if (qCountInput) qCountInput.value = state.currentExam.questions.length;

  recalculateTotalPoints();
  renderExamPages();
  showToast("Yeni soru başarıyla eklendi!", "info");
}

async function regenerateSingleQuestion(idx) {
  const checkedUnits = Array.from(document.querySelectorAll(".unit-checkbox:checked")).map(cb => cb.value);
  setLoading(true, `${idx + 1}. soru yeniden üretiliyor...`);

  try {
    const res = await fetch("/api/regenerate-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: state.currentExam.subject,
        grade: state.currentExam.grade,
        term: state.currentExam.term || "1. Dönem",
        exam_no: state.currentExam.exam_no || "1. Yazılı",
        q_order: idx + 1,
        selected_units: checkedUnits,
        exam_type: state.currentExam.exam_type || "yazili_sinav"
      })
    });
    if (!res.ok) throw new Error("Yeniden üretilemedi.");
    const data = await res.json();
    if (data.question) {
      data.question.points = state.currentExam.questions[idx].points || 10;
      state.currentExam.questions[idx] = data.question;
      renderExamPages();
      showToast(`${idx + 1}. soru güncellendi!`, "success");
    }
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

// --- DÜZEN DEĞİŞTİRME (2 SÜTUN / 1 SÜTUN) ---
function toggleLayout(layout) {
  state.currentExam.layout = layout;
  const btn2 = document.getElementById("btnLayout2Col");
  const btn1 = document.getElementById("btnLayout1Col");
  
  if (layout === "2_column") {
    btn2.className = "px-2.5 py-1 text-xs font-semibold rounded bg-blue-600 text-white shadow";
    btn1.className = "px-2.5 py-1 text-xs font-semibold rounded bg-slate-200 text-slate-700 hover:bg-slate-300";
  } else {
    btn1.className = "px-2.5 py-1 text-xs font-semibold rounded bg-blue-600 text-white shadow";
    btn2.className = "px-2.5 py-1 text-xs font-semibold rounded bg-slate-200 text-slate-700 hover:bg-slate-300";
  }
  
  // Sayfalama motorunu anında yeniden çalıştır!
  renderExamPages();
  showToast(`Sayfa düzeni ${layout === "2_column" ? "2 Sütunlu MEB" : "Tek Sütunlu"} olarak ayarlandı.`, "info");
}

// --- 3 ANA SEKME GEÇİŞİ (Öğrenci Kağıdı, Cevap Anahtarı, Kitap Doğrulama) ---
function switchTab(tab) {
  state.activeTab = tab;
  const examContainer = document.getElementById("examPagesContainer");
  const answerSheet = document.getElementById("answerSheetContainer");
  const sourceSheet = document.getElementById("sourceVerificationContainer");

  const tabExam = document.getElementById("tabExamBtn");
  const tabAnswer = document.getElementById("tabAnswerBtn");
  const tabSource = document.getElementById("tabSourceBtn");

  // Önce hepsini gizle
  examContainer.classList.add("hidden");
  answerSheet.classList.add("hidden");
  sourceSheet.classList.add("hidden");

  tabExam.className = "px-3 py-1.5 text-xs font-semibold rounded-md text-slate-600 hover:text-blue-600 transition flex items-center gap-1.5";
  tabAnswer.className = "px-3 py-1.5 text-xs font-semibold rounded-md text-slate-600 hover:text-blue-600 transition flex items-center gap-1.5";
  tabSource.className = "px-3 py-1.5 text-xs font-semibold rounded-md text-slate-600 hover:text-blue-600 transition flex items-center gap-1.5";

  if (tab === "exam") {
    examContainer.classList.remove("hidden");
    tabExam.className = "px-3 py-1.5 text-xs font-semibold rounded-md bg-blue-600 text-white shadow transition flex items-center gap-1.5";
  } else if (tab === "answer_key") {
    answerSheet.classList.remove("hidden");
    tabAnswer.className = "px-3 py-1.5 text-xs font-semibold rounded-md bg-blue-600 text-white shadow transition flex items-center gap-1.5";
    renderAnswerKeySheet();
  } else if (tab === "source_verification") {
    sourceSheet.classList.remove("hidden");
    tabSource.className = "px-3 py-1.5 text-xs font-semibold rounded-md bg-blue-600 text-white shadow transition flex items-center gap-1.5";
    renderSourceVerificationSheet();
  }
}

// --- 2. SEKME: CEVAP ANAHTARI & RUBRİK RENDER ---
function renderAnswerKeySheet() {
  const container = document.getElementById("answerKeyContent");
  if (!container) return;
  container.innerHTML = "";

  const exam = state.currentExam;

  const hdr = document.createElement("div");
  hdr.className = "mb-4 pb-2 border-b-2 border-blue-900 text-center";
  hdr.innerHTML = `
    <h3 class="font-bold text-sm text-slate-900">${state.config.school_name || "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu"}</h3>
    <h4 class="font-bold text-blue-900 text-sm">${exam.grade}. SINIF ${(exam.subject_name || "").toUpperCase()} ${(exam.term || "").toUpperCase()} ${(exam.exam_no || "").toUpperCase()}</h4>
    <div class="text-xs font-semibold text-emerald-800 mt-1">CEVAP ANAHTARI VE DERECELİ PUANLAMA ANAHTARI (RUBRİK)</div>
  `;
  container.appendChild(hdr);

  if (!exam.questions || exam.questions.length === 0) {
    container.innerHTML += `<div class="text-center text-xs text-slate-400 py-8">Henüz soru üretilmedi.</div>`;
    return;
  }

  exam.questions.forEach((q, idx) => {
    const item = document.createElement("div");
    item.className = "mb-4 p-3 bg-white border border-slate-200 rounded-lg shadow-sm";

    let rubricHtml = "";
    if (q.rubric && Array.isArray(q.rubric)) {
      rubricHtml = `
        <div class="rubric-box">
          <div class="font-semibold text-slate-700 text-[11px] mb-1">Dereceli Puanlama Anahtarı (Kısmi Puan Kriterleri):</div>
          ${q.rubric.map(r => `
            <div class="rubric-item">
              <span class="text-slate-600">• ${r.criterion || r}</span>
              <span class="font-bold text-blue-900">${r.points || ""} Puan</span>
            </div>
          `).join("")}
        </div>
      `;
    }

    item.innerHTML = `
      <div class="flex items-center justify-between border-b pb-1 mb-2">
        <span class="font-bold text-xs text-blue-950">SORU ${idx + 1} (${q.points} Puan)</span>
        <span class="text-[10px] text-slate-500 italic">Kazanım: ${q.learning_outcome || "Genel"}</span>
      </div>
      <div class="text-xs text-slate-700 mb-2"><strong>Soru Metni:</strong> <span contenteditable="true" onblur="updateQuestionText(${idx}, this.innerText)">${q.question_text || ""}</span></div>
      <div class="text-xs bg-emerald-50 text-emerald-950 p-2 rounded border border-emerald-200 mb-2">
        <strong class="text-emerald-800">Beklenen Örnek Çözüm / Model Cevap:</strong><br>
        <div contenteditable="true" onblur="updateAnswerText(${idx}, this.innerText)">${q.answer_text || ""}</div>
      </div>
      ${rubricHtml}
    `;
    container.appendChild(item);
  });
}

function updateAnswerText(idx, newText) {
  if (state.currentExam.questions[idx]) {
    state.currentExam.questions[idx].answer_text = newText.trim();
  }
}

// --- 3. SEKME: KİTAP İLİŞKİSİ VE PEDAGOJİK DOĞRULAMA (YENİ TALEP) ---
function renderSourceVerificationSheet() {
  const container = document.getElementById("sourceVerificationContent");
  if (!container) return;
  container.innerHTML = "";

  const exam = state.currentExam;

  const hdr = document.createElement("div");
  hdr.className = "mb-4 pb-2 border-b-2 border-amber-800 text-center";
  hdr.innerHTML = `
    <h3 class="font-bold text-sm text-slate-900">${state.config.school_name || "Tevfik İleri İmam Hatip Ortaokulu"}</h3>
    <h4 class="font-bold text-amber-900 text-sm">${exam.grade}. SINIF ${(exam.subject_name || "").toUpperCase()} • KİTAP İLİŞKİSİ VE PEDAGOJİK DOĞRULAMA RAPORU</h4>
    <p class="text-[11px] text-slate-500 mt-1">Soruların MEB ders kitabındaki yerleri, bilişsel basamakları ve kazanım gerekçeleri aşağıda listelenmiştir.</p>
  `;
  container.appendChild(hdr);

  if (!exam.questions || exam.questions.length === 0) {
    container.innerHTML += `<div class="text-center text-xs text-slate-400 py-8">Henüz soru üretilmedi.</div>`;
    return;
  }

  exam.questions.forEach((q, idx) => {
    const card = document.createElement("div");
    card.className = "mb-4 p-4 bg-white border border-slate-200 rounded-lg shadow-sm space-y-2.5 text-xs";

    card.innerHTML = `
      <div class="flex items-center justify-between border-b pb-1.5 flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <span class="font-bold text-sm text-blue-950">SORU ${idx + 1}</span>
          <span class="badge-tag bg-blue-100 text-blue-800">${q.cognitive_level || "Analiz"}</span>
          <span class="badge-tag ${q.difficulty === "Zor" ? "bg-red-100 text-red-800" : q.difficulty === "Kolay" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}">
            Güçlük: ${q.difficulty || "Orta"}
          </span>
        </div>
        <div class="text-[11px] font-semibold text-indigo-900 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
          📖 Kaynak: ${q.source_book || `${exam.grade}. Sınıf Ders Kitabı`} | ${q.source_page || "İlgili Ünite"}
        </div>
      </div>

      <div class="bg-slate-50 p-2.5 rounded border border-slate-200 text-slate-700">
        <strong class="text-slate-900">Soru Metni (Doğrudan Düzenlenebilir):</strong>
        <div class="mt-1 text-slate-800 p-1 rounded hover:bg-white" contenteditable="true" onblur="updateQuestionText(${idx}, this.innerText)">
          ${q.question_text || ""}
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div class="p-2 bg-amber-50/60 rounded border border-amber-200">
          <strong class="text-amber-900">📚 Kitaptaki Pedagojik Bağlam & Sayfa Özeti:</strong>
          <div class="mt-1 text-amber-950 text-[11px] leading-relaxed">
            ${q.source_context || "Bu soru MEB ders kitabındaki kazanım ve ünite temaları taranarak bağlam temelli olarak modellenmiştir."}
          </div>
        </div>

        <div class="p-2 bg-emerald-50/60 rounded border border-emerald-200">
          <strong class="text-emerald-900">🎯 MEB 2026 Öğrenme Çıktısı (Kazanım):</strong>
          <div class="mt-1 text-emerald-950 text-[11px] font-medium">
            ${q.learning_outcome || "Müfredat kazanımı"}
          </div>
          <div class="mt-2 text-[10px] text-slate-500">
            <strong>Model Cevap:</strong> ${q.answer_text ? q.answer_text.slice(0, 100) + "..." : "Çözüm tanımlı."}
          </div>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// --- DIŞA AKTARMA (PDF & WORD) ---
function handlePrintPDF() {
  window.print();
}

async function handleExportDocx(docType = "exam") {
  setLoading(true, "Word (.docx) belgesi oluşturuluyor...");
  try {
    const res = await fetch("/api/export/docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        exam_data: {
          ...state.currentExam,
          header_info: {
            school_header: state.config.school_header,
            school_name: state.config.school_name
          }
        },
        type: docType,
        layout: state.currentExam.layout
      })
    });
    if (!res.ok) throw new Error("Word belgesi oluşturulamadı.");
    
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = docType === "answer_key" 
      ? `Cevap_Anahtari_${state.currentExam.subject_name}_${state.currentExam.grade}Sinif.docx` 
      : docType === "source_verification"
      ? `Kitap_Dogrulama_${state.currentExam.subject_name}_${state.currentExam.grade}Sinif.docx`
      : `Sinav_Kagidi_${state.currentExam.subject_name}_${state.currentExam.grade}Sinif.docx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("Word belgesi başarıyla indirildi!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

// --- SINAVI KAYDETME & ARŞİV ---
async function handleSaveExam() {
  if (!state.currentExam.questions || state.currentExam.questions.length === 0) {
    showToast("Kaydedilecek soru bulunmuyor.", "warning");
    return;
  }

  setLoading(true, "Sınav kaydediliyor ve sorular soru bankasına arşivleniyor...");
  try {
    const res = await fetch("/api/save-exam", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...state.currentExam,
        header_info: {
          school_header: state.config.school_header,
          school_name: state.config.school_name,
          teacher_name: state.config.teacher_name
        }
      })
    });
    if (!res.ok) throw new Error("Sınav kaydedilemedi.");
    const data = await res.json();
    state.currentExam.id = data.exam_id;
    showToast("Sınav ve sorular soru bankasına başarıyla kaydedildi!", "success");
    loadSavedExamsList();
    loadQuestionBank();
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function loadSavedExamsList() {
  try {
    const res = await fetch("/api/exams");
    const data = await res.json();
    state.savedExams = data.exams || [];
    renderSavedExamsUI();
  } catch (e) {
    console.error("Geçmiş sınavlar alınamadı:", e);
  }
}

function renderSavedExamsUI() {
  const container = document.getElementById("savedExamsList");
  if (!container) return;
  container.innerHTML = "";

  if (state.savedExams.length === 0) {
    container.innerHTML = `<div class="text-xs text-slate-400 p-2 italic">Henüz kaydedilmiş sınav yok.</div>`;
    return;
  }

  state.savedExams.forEach(ex => {
    const div = document.createElement("div");
    div.className = "flex items-center justify-between p-2 hover:bg-slate-50 border-b border-slate-100 rounded text-xs";
    div.innerHTML = `
      <div class="cursor-pointer flex-1" onclick="loadExamById(${ex.id})">
        <div class="font-semibold text-slate-800">${ex.title}</div>
        <div class="text-[10px] text-slate-400">${ex.grade}. Sınıf • ${ex.scenario || "MEB"} • ${ex.question_count} Soru • ${ex.updated_at.slice(0, 10)}</div>
      </div>
      <button type="button" class="text-red-500 hover:text-red-700 p-1" title="Sil" onclick="deleteSavedExam(${ex.id})">
        🗑️
      </button>
    `;
    container.appendChild(div);
  });
}

async function loadExamById(id) {
  setLoading(true, "Sınav yükleniyor...");
  try {
    const res = await fetch(`/api/exams/${id}`);
    if (!res.ok) throw new Error("Sınav açılamadı.");
    const data = await res.json();
    state.currentExam = data.exam;
    recalculateTotalPoints();
    renderExamPages();
    showToast("Sınav yüklendi.", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function deleteSavedExam(id) {
  if (confirm("Bu kayıtlı sınavı silmek istediğinize emin misiniz?")) {
    try {
      await fetch(`/api/exams/${id}`, { method: "DELETE" });
      loadSavedExamsList();
      showToast("Sınav silindi.", "info");
    } catch (e) {
      showToast("Silinemedi.", "error");
    }
  }
}

// ==============================================================
// SORU BANKASI VE HAVUZ YÖNETİMİ (YENİ TALEP)
// ==============================================================
async function loadQuestionBank() {
  const subj = document.getElementById("bankFilterSubject")?.value || "";
  const grade = document.getElementById("bankFilterGrade")?.value || "";
  const diff = document.getElementById("bankFilterDifficulty")?.value || "";
  const search = document.getElementById("bankSearchInput")?.value || "";

  let url = `/api/question-bank?`;
  if (subj) url += `subject=${subj}&`;
  if (grade) url += `grade=${grade}&`;
  if (diff) url += `difficulty=${diff}&`;
  if (search) url += `search=${encodeURIComponent(search)}&`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    state.questionBankItems = data.items || [];
    renderQuestionBankUI();
  } catch (e) {
    console.error("Soru bankası yüklenemedi:", e);
  }
}

function renderQuestionBankUI() {
  const container = document.getElementById("bankCardsGrid");
  const countBadge = document.getElementById("bankTotalCountBadge");
  if (!container) return;
  container.innerHTML = "";

  if (countBadge) {
    countBadge.textContent = `${state.questionBankItems.length} Soru`;
  }

  if (state.questionBankItems.length === 0) {
    container.innerHTML = `
      <div class="col-span-2 text-center py-12 text-slate-400">
        <div class="text-4xl mb-2">📭</div>
        <div class="font-bold text-sm text-slate-700">Soru Havuzunda Henüz Soru Yok</div>
        <div class="text-xs text-slate-400 mt-1">Sınav hazırlayıp kaydettiğinizde veya "Kitaptan Soru Üret" butonuna bastığınızda sorular burada birikir.</div>
      </div>
    `;
    return;
  }

  state.questionBankItems.forEach(item => {
    const card = document.createElement("div");
    card.className = "bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between text-xs space-y-3";

    // Kullanım Rozeti
    const usageCount = item.usage_count || 0;
    const usageBadgeHtml = usageCount > 0 
      ? `<button onclick="openUsageModal(${item.id})" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 hover:bg-emerald-200 cursor-pointer flex items-center gap-1" title="Hangi sınavlarda kullanıldığını gör">
           <span>📌</span> ${usageCount} Sınavda Kullanıldı (Gör)
         </button>`
      : `<span class="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
           Henüz Kullanılmadı
         </span>`;

    const arabicHtml = item.arabic_text ? `<div class="arabic-text text-sm my-1">${item.arabic_text}</div>` : "";

    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between border-b pb-2 mb-2 flex-wrap gap-1">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="badge-tag bg-blue-100 text-blue-900 font-bold">${item.grade}. Sınıf ${(item.subject || "").toUpperCase()}</span>
            <span class="badge-tag bg-slate-100 text-slate-700">${item.cognitive_level || "Analiz"}</span>
            <span class="badge-tag ${item.difficulty === "Zor" ? "bg-red-100 text-red-700" : "bg-amber-100 text-amber-700"}">${item.difficulty || "Orta"}</span>
          </div>
          ${usageBadgeHtml}
        </div>

        <div class="font-semibold text-slate-900 text-xs leading-relaxed mb-2">
          ${item.question_text}
        </div>
        ${arabicHtml}

        <div class="text-[11px] text-slate-500 italic mb-2">
          🎯 Kazanım: ${item.learning_outcome || "Genel"}
        </div>
        <div class="text-[11px] text-indigo-900 bg-indigo-50/70 p-1.5 rounded">
          📖 Kaynak: ${item.source_book || "Ders Kitabı"} ${item.source_page ? `(${item.source_page})` : ""}
        </div>
      </div>

      <div class="flex items-center justify-between pt-2 border-t border-slate-100 mt-2">
        <button onclick="addBankQuestionToExam(${item.id})" class="px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white font-bold text-xs rounded shadow flex items-center gap-1">
          <span>➕</span> Bu Soruyu Sınava Ekle
        </button>
        <button onclick="deleteBankQuestion(${item.id})" class="text-red-500 hover:text-red-700 text-xs p-1" title="Havuzdan Sil">
          🗑️ Sil
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function openUsageModal(bankId) {
  const item = state.questionBankItems.find(q => q.id === bankId);
  if (!item) return;

  const content = document.getElementById("usageModalContent");
  content.innerHTML = "";

  if (item.used_in_exams_list && item.used_in_exams_list.length > 0) {
    item.used_in_exams_list.forEach((examTitle, idx) => {
      const row = document.createElement("div");
      row.className = "p-2 bg-slate-50 border border-slate-200 rounded flex items-center gap-2";
      row.innerHTML = `<span class="font-bold text-blue-900">${idx + 1}.</span> <span>${examTitle}</span>`;
      content.appendChild(row);
    });
  } else {
    content.innerHTML = `<div class="text-slate-400 italic">Bu soru henüz hiçbir sınavda kullanılmadı.</div>`;
  }

  document.getElementById("usageDetailModal").classList.remove("hidden");
}

function closeUsageModal() {
  document.getElementById("usageDetailModal").classList.add("hidden");
}

function addBankQuestionToExam(bankId) {
  const item = state.questionBankItems.find(q => q.id === bankId);
  if (!item) return;

  const cloned = {
    q_order: state.currentExam.questions.length + 1,
    points: 10,
    learning_outcome: item.learning_outcome || "",
    question_type: item.question_type || "acik_uclu",
    cognitive_level: item.cognitive_level || "Analiz",
    difficulty: item.difficulty || "Orta",
    source_book: item.source_book || "",
    source_page: item.source_page || "",
    source_context: item.source_context || "",
    arabic_text: item.arabic_text || "",
    question_text: item.question_text || "",
    options: item.options || [],
    answer_text: item.answer_text || "",
    rubric: item.rubric || []
  };

  state.currentExam.questions.push(cloned);
  
  // Sol panel soru sayısı inputunu güncelle
  const qCountInput = document.getElementById("examQuestionCount");
  if (qCountInput) qCountInput.value = state.currentExam.questions.length;

  recalculateTotalPoints();
  renderExamPages();
  showToast("Soru bankasındaki soru sınava eklendi!", "success");
  
  // Sınav ekranına geçiş yap
  switchView("exam_maker");
}

async function deleteBankQuestion(id) {
  if (confirm("Bu soruyu soru bankasından silmek istediğinize emin misiniz?")) {
    try {
      await fetch(`/api/question-bank/${id}`, { method: "DELETE" });
      loadQuestionBank();
      showToast("Soru silindi.", "info");
    } catch (e) {
      showToast("Silinemedi.", "error");
    }
  }
}

// Soru Bankasına Kitaptan Soru Üretme
function openGenerateToBankModal() {
  document.getElementById("generateToBankModal").classList.remove("hidden");
}

function closeGenerateToBankModal() {
  document.getElementById("generateToBankModal").classList.add("hidden");
}

async function handleGenerateToBank(e) {
  e.preventDefault();
  const subject = document.getElementById("bankGenSubject").value;
  const grade = parseInt(document.getElementById("bankGenGrade").value, 10);
  const count = parseInt(document.getElementById("bankGenCount").value, 10) || 5;
  const question_type = document.getElementById("bankGenType").value;

  closeGenerateToBankModal();
  setLoading(true, "Kitap taranarak soru bankasına sorular üretiliyor...");

  try {
    const res = await fetch("/api/generate-bank-questions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject,
        grade,
        count,
        question_type,
        difficulty: "Dengeli"
      })
    });
    if (!res.ok) throw new Error("Sorular üretilemedi.");
    const data = await res.json();
    showToast(`${data.saved_count || count} soru başarıyla soru bankasına eklendi!`, "success");
    loadQuestionBank();
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

// Görünüm Değiştirici (Sınav Hazırlama vs. Soru Bankası)
function switchView(view) {
  state.currentView = view;
  const examView = document.getElementById("viewExamMaker");
  const bankView = document.getElementById("viewQuestionBank");
  const btnExam = document.getElementById("navExamMakerBtn");
  const btnBank = document.getElementById("navQuestionBankBtn");

  if (view === "exam_maker") {
    examView.classList.remove("hidden");
    bankView.classList.add("hidden");
    btnExam.className = "px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white transition flex items-center gap-1.5 shadow-sm";
    btnBank.className = "px-3 py-1 text-xs font-bold rounded text-blue-200 hover:text-white transition flex items-center gap-1.5";
  } else {
    examView.classList.add("hidden");
    bankView.classList.remove("hidden");
    btnBank.className = "px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white transition flex items-center gap-1.5 shadow-sm";
    btnExam.className = "px-3 py-1 text-xs font-bold rounded text-blue-200 hover:text-white transition flex items-center gap-1.5";
    loadQuestionBank();
  }
}

// ==============================================================
// MÜFREDAT VE KONU YÖNETİM MASASI (YENİ TALEP)
// ==============================================================
state.managerData = {
  subject: "dkab",
  grade: 5,
  units: []
};

async function openCurriculumManager() {
  const subject = document.getElementById("examSubject") ? document.getElementById("examSubject").value : "dkab";
  const grade = document.getElementById("examGrade") ? parseInt(document.getElementById("examGrade").value, 10) : 5;

  setLoading(true, "Ünite ve konular yükleniyor...");
  try {
    const res = await fetch(`/api/curriculum-manager?subject=${subject}&grade=${grade}`);
    const data = await res.json();
    state.managerData = {
      subject,
      grade,
      subject_name: data.subject_name || "Ders",
      units: JSON.parse(JSON.stringify(data.units || []))
    };

    document.getElementById("currManagerSubtitle").textContent = 
      `${grade}. Sınıf ${state.managerData.subject_name} dersinin ünite, konu ve sayfa aralıklarını aşağıdan yönetebilirsiniz.`;

    renderCurriculumManagerUI();
    document.getElementById("curriculumManagerModal").classList.remove("hidden");
  } catch (err) {
    showToast("Üniteler yüklenemedi: " + err.message, "error");
  } finally {
    setLoading(false);
  }
}

function closeCurriculumModal() {
  document.getElementById("curriculumManagerModal").classList.add("hidden");
}

function renderCurriculumManagerUI() {
  const container = document.getElementById("curriculumUnitsList");
  if (!container) return;
  container.innerHTML = "";

  const units = state.managerData.units;

  if (units.length === 0) {
    container.innerHTML = `<div class="text-center py-8 text-xs text-slate-400">Bu ders için tanımlı ünite bulunamadı. Yeni ünite ekleyebilirsiniz.</div>`;
    return;
  }

  units.forEach((u, uIdx) => {
    const card = document.createElement("div");
    card.className = "p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3";

    // Ünite Başlığı ve Sayfa Aralığı
    const headerRow = `
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div class="flex-1 min-w-[240px]">
          <label class="text-[10px] font-bold text-slate-500 uppercase block mb-0.5">Ünite Adı</label>
          <input type="text" value="${u.name || ""}" 
                 class="w-full text-xs font-bold text-slate-900 px-2.5 py-1.5 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-600"
                 onchange="updateUnitTitle(${uIdx}, this.value)">
        </div>
        <div class="flex items-center gap-2">
          <div>
            <label class="text-[10px] font-bold text-slate-500 uppercase block mb-0.5">Kitap Sayfaları</label>
            <div class="flex items-center gap-1 text-xs">
              <input type="number" min="1" value="${(u.page_range && u.page_range[0]) || 1}" 
                     class="w-16 px-2 py-1 text-center bg-white border border-slate-300 rounded font-semibold text-blue-900"
                     onchange="updateUnitPageRange(${uIdx}, 0, this.value)">
              <span class="text-slate-400">-</span>
              <input type="number" min="1" value="${(u.page_range && u.page_range[1]) || 50}" 
                     class="w-16 px-2 py-1 text-center bg-white border border-slate-300 rounded font-semibold text-blue-900"
                     onchange="updateUnitPageRange(${uIdx}, 1, this.value)">
            </div>
          </div>
          <div class="pt-3">
            <button type="button" onclick="deleteUnit(${uIdx})" class="p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded" title="Bu Üniteyi Sil">
              🗑️
            </button>
          </div>
        </div>
      </div>
    `;

    // Alt Konular Listesi
    let topicsListHtml = "";
    if (u.topics && Array.isArray(u.topics)) {
      topicsListHtml = u.topics.map((top, tIdx) => {
        // Diğer ünitelere aktarma seçenekleri
        const otherUnitsOptions = units.map((otherU, otherIdx) => {
          if (otherIdx === uIdx) return "";
          return `<option value="${otherIdx}">${otherU.name ? otherU.name.slice(0, 24) : `Ünite ${otherIdx+1}`}...</option>`;
        }).join("");

        return `
          <div class="flex items-center justify-between gap-2 p-1.5 bg-white border border-slate-200 rounded text-xs">
            <div class="flex items-center gap-1.5 flex-1">
              <span class="text-slate-400 font-bold text-[10px] w-4">${tIdx + 1}.</span>
              <input type="text" value="${top || ""}" 
                     class="w-full text-xs text-slate-800 px-2 py-1 border border-transparent hover:border-slate-300 focus:border-blue-600 rounded"
                     onchange="updateTopicTitle(${uIdx}, ${tIdx}, this.value)">
            </div>
            
            <div class="flex items-center gap-1">
              ${otherUnitsOptions ? `
                <select class="text-[10px] py-1 px-1.5 bg-slate-100 hover:bg-blue-50 border border-slate-200 rounded text-slate-600 font-medium cursor-pointer"
                        onchange="moveTopicToAnotherUnit(${uIdx}, ${tIdx}, this.value); this.selectedIndex = 0;">
                  <option value="" disabled selected>➡️ Başka Üniteye Aktar</option>
                  ${otherUnitsOptions}
                </select>
              ` : ""}
              <button type="button" onclick="deleteTopic(${uIdx}, ${tIdx})" class="p-1 text-slate-400 hover:text-red-600" title="Konuyu Sil">
                ✕
              </button>
            </div>
          </div>
        `;
      }).join("");
    }

    card.innerHTML = `
      ${headerRow}
      <div class="space-y-1.5 pt-1">
        <label class="text-[10px] font-bold text-slate-600 uppercase flex items-center justify-between">
          <span>Kapsamdaki Alt Konular (${(u.topics || []).length})</span>
          <button type="button" onclick="addNewTopicToUnit(${uIdx})" class="text-[10px] text-blue-700 hover:text-blue-900 font-bold flex items-center gap-0.5">
            ➕ Konu Ekle
          </button>
        </label>
        <div class="space-y-1">
          ${topicsListHtml}
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}

function updateUnitTitle(uIdx, title) {
  if (state.managerData.units[uIdx]) {
    state.managerData.units[uIdx].name = title.trim();
  }
}

function updateUnitPageRange(uIdx, pos, val) {
  if (state.managerData.units[uIdx]) {
    if (!state.managerData.units[uIdx].page_range) {
      state.managerData.units[uIdx].page_range = [1, 50];
    }
    state.managerData.units[uIdx].page_range[pos] = parseInt(val, 10) || 1;
  }
}

function updateTopicTitle(uIdx, tIdx, val) {
  if (state.managerData.units[uIdx] && state.managerData.units[uIdx].topics) {
    state.managerData.units[uIdx].topics[tIdx] = val.trim();
  }
}

function addNewTopicToUnit(uIdx) {
  if (state.managerData.units[uIdx]) {
    if (!state.managerData.units[uIdx].topics) state.managerData.units[uIdx].topics = [];
    state.managerData.units[uIdx].topics.push("Yeni Konu Başlığı");
    renderCurriculumManagerUI();
  }
}

function deleteTopic(uIdx, tIdx) {
  if (state.managerData.units[uIdx] && state.managerData.units[uIdx].topics) {
    state.managerData.units[uIdx].topics.splice(tIdx, 1);
    renderCurriculumManagerUI();
  }
}

// Bir konuyu başka bir üniteye aktarma (Kullanıcı Talebi)
function moveTopicToAnotherUnit(fromUnitIdx, topicIdx, toUnitIdxStr) {
  const toUnitIdx = parseInt(toUnitIdxStr, 10);
  const units = state.managerData.units;
  
  if (units[fromUnitIdx] && units[toUnitIdx]) {
    const topicText = units[fromUnitIdx].topics.splice(topicIdx, 1)[0];
    if (!units[toUnitIdx].topics) units[toUnitIdx].topics = [];
    units[toUnitIdx].topics.push(topicText);
    renderCurriculumManagerUI();
    showToast(`Konu "${units[toUnitIdx].name || 'Hedef Ünite'}"ye aktarıldı.`, "info");
  }
}

function addNewUnitToManager() {
  const newNum = state.managerData.units.length + 1;
  const newUnit = {
    id: `${state.managerData.subject}${state.managerData.grade}_u${Date.now()}`,
    name: `${newNum}. Ünite: Yeni Ünite`,
    topics: ["Yeni Konu 1"],
    page_range: [1, 50]
  };
  state.managerData.units.push(newUnit);
  renderCurriculumManagerUI();
  showToast("Yeni ünite eklendi. Konu ve sayfalarını düzenleyebilirsiniz.", "info");
}

function deleteUnit(uIdx) {
  if (confirm("Bu üniteyi ve altındaki konuları silmek istediğinize emin misiniz?")) {
    state.managerData.units.splice(uIdx, 1);
    renderCurriculumManagerUI();
  }
}

async function saveCurriculumManagerChanges() {
  setLoading(true, "Müfredat değişiklikleri kaydediliyor...");
  try {
    const res = await fetch("/api/curriculum-manager/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: state.managerData.subject,
        grade: state.managerData.grade,
        units: state.managerData.units
      })
    });
    if (!res.ok) throw new Error("Kaydedilemedi.");
    await loadCurriculum();
    onSubjectOrGradeChange();
    closeCurriculumModal();
    showToast("Üniteler ve konular başarıyla güncellendi!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function resetCurriculumToDefault() {
  if (confirm("Müfredatı MEB orijinal fabrika ayarlarına sıfırlamak istediğinize emin misiniz?")) {
    setLoading(true, "Sıfırlanıyor...");
    try {
      await fetch("/api/curriculum-manager/reset", { method: "POST" });
      await loadCurriculum();
      onSubjectOrGradeChange();
      await openCurriculumManager(); // Yeniden yükle
      showToast("MEB orijinal müfredatına dönüldü.", "info");
    } catch (err) {
      showToast("Sıfırlanamadı.", "error");
    } finally {
      setLoading(false);
    }
  }
}

// --- AYARLAR MODALI ---
function openSettingsModal() {
  document.getElementById("settingsSchoolHeader").value = state.config.school_header || "";
  document.getElementById("settingsSchoolName").value = state.config.school_name || "";
  document.getElementById("settingsTeacherName").value = state.config.teacher_name || "";
  document.getElementById("settingsGeminiApiKey").value = state.config.gemini_api_key || "";
  document.getElementById("settingsGeminiModel").value = state.config.gemini_model || "gemini-2.5-flash";
  document.getElementById("settingsModal").classList.remove("hidden");
}

function closeSettingsModal() {
  document.getElementById("settingsModal").classList.add("hidden");
}

async function handleSaveSettings(e) {
  e.preventDefault();
  const updateData = {
    school_header: document.getElementById("settingsSchoolHeader").value.trim(),
    school_name: document.getElementById("settingsSchoolName").value.trim(),
    teacher_name: document.getElementById("settingsTeacherName").value.trim(),
    gemini_api_key: document.getElementById("settingsGeminiApiKey").value.trim(),
    gemini_model: document.getElementById("settingsGeminiModel").value.trim(),
  };

  try {
    const res = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData)
    });
    if (!res.ok) throw new Error("Ayarlar kaydedilemedi.");
    await loadConfig();
    renderExamPages();
    closeSettingsModal();
    showToast("Ayarlar başarıyla kaydedildi!", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
}

// --- EVENT LISTENERS ---
function setupEventListeners() {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) loginForm.addEventListener("submit", handleLogin);

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);

  // Navigasyon
  document.getElementById("navExamMakerBtn")?.addEventListener("click", () => switchView("exam_maker"));
  document.getElementById("navQuestionBankBtn")?.addEventListener("click", () => switchView("question_bank"));

  // Sınav Parametreleri
  document.getElementById("examTypeSelect")?.addEventListener("change", updatePaperHeaderLive);
  document.getElementById("examSubject")?.addEventListener("change", onSubjectOrGradeChange);
  document.getElementById("examGrade")?.addEventListener("change", onSubjectOrGradeChange);
  document.getElementById("examTerm")?.addEventListener("change", updatePaperHeaderLive);
  document.getElementById("examNo")?.addEventListener("change", updatePaperHeaderLive);
  document.getElementById("examScenario")?.addEventListener("change", onScenarioChange);

  document.getElementById("btnGenerateExam")?.addEventListener("click", handleGenerateExam);
  document.getElementById("btnAddQuestion")?.addEventListener("click", addNewQuestion);

  // Düzen Değiştirme
  document.getElementById("btnLayout2Col")?.addEventListener("click", () => toggleLayout("2_column"));
  document.getElementById("btnLayout1Col")?.addEventListener("click", () => toggleLayout("1_column"));

  // 3 Ana Sekme
  document.getElementById("tabExamBtn")?.addEventListener("click", () => switchTab("exam"));
  document.getElementById("tabAnswerBtn")?.addEventListener("click", () => switchTab("answer_key"));
  document.getElementById("tabSourceBtn")?.addEventListener("click", () => switchTab("source_verification"));

  // Dışa Aktarma Butonları
  document.getElementById("btnPrintPdf")?.addEventListener("click", handlePrintPDF);
  document.getElementById("btnExportDocx")?.addEventListener("click", () => handleExportDocx("exam"));
  document.getElementById("btnExportAnswerDocx")?.addEventListener("click", () => handleExportDocx("answer_key"));
  document.getElementById("btnExportSourceDocx")?.addEventListener("click", () => handleExportDocx("source_verification"));
  document.getElementById("btnSaveExam")?.addEventListener("click", handleSaveExam);

  // Soru Bankası Buton ve Filtreleri
  document.getElementById("btnOpenGenerateToBankModal")?.addEventListener("click", openGenerateToBankModal);
  document.getElementById("generateToBankForm")?.addEventListener("submit", handleGenerateToBank);
  document.getElementById("bankFilterSubject")?.addEventListener("change", loadQuestionBank);
  document.getElementById("bankFilterGrade")?.addEventListener("change", loadQuestionBank);
  document.getElementById("bankFilterDifficulty")?.addEventListener("change", loadQuestionBank);
  document.getElementById("bankSearchInput")?.addEventListener("input", debounce(loadQuestionBank, 300));

  // Müfredat ve Konu Yöneticisi Butonu (YENİ TALEP)
  document.getElementById("btnOpenCurriculumManager")?.addEventListener("click", openCurriculumManager);

  // Ayarlar Modalı
  document.getElementById("btnOpenSettings")?.addEventListener("click", openSettingsModal);
  document.getElementById("btnCloseSettings")?.addEventListener("click", closeSettingsModal);
  document.getElementById("settingsForm")?.addEventListener("submit", handleSaveSettings);
}

function debounce(func, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => func.apply(this, args), delay);
  };
}

function setLoading(loading, text = "Lütfen bekleyiniz...") {
  state.isLoading = loading;
  const overlay = document.getElementById("loadingOverlay");
  const overlayText = document.getElementById("loadingText");
  if (overlay) {
    if (loading) {
      if (overlayText) overlayText.textContent = text;
      overlay.classList.remove("hidden");
    } else {
      overlay.classList.add("hidden");
    }
  }
}

function showToast(message, type = "info") {
  const toast = document.getElementById("toastNotification");
  if (!toast) return;
  toast.textContent = message;
  toast.className = `fixed bottom-5 right-5 z-50 px-4 py-2.5 rounded-lg shadow-lg text-xs font-semibold text-white transition-all transform duration-300 ${
    type === "success" ? "bg-emerald-600" : type === "error" ? "bg-red-600" : "bg-blue-600"
  }`;
  toast.classList.remove("hidden", "opacity-0", "translate-y-2");
  setTimeout(() => {
    toast.classList.add("opacity-0", "translate-y-2");
    setTimeout(() => toast.classList.add("hidden"), 300);
  }, 3500);
}
