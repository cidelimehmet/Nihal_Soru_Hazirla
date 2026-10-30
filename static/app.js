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
  showAnswerLines: true, // Noktalı cevap çizgilerini göster/gizle
  showScenarioInHeader: true, // Başlıkta senaryo adı ve konu detayını göster/gizle
  showBepInHeader: true, // BEP sınavlarında başlıkta BEP ibaresini göster/gizle
  activeTab: "exam", // "exam", "answer_key", "source_verification"
  currentView: "exam_maker", // "exam_maker", "exam_archive", "question_bank"
  savedExams: [],
  archiveViewMode: "layered", // "layered" (sınıf & ders katmanlı) veya "grid"
  archiveFilters: {
    search: "",
    grade: "",
    subject: "",
    term: "",
    type: ""
  },
  questionBankItems: [],
  scenariosData: null,
  activeScenarioList: [],
  activeScenarioObj: null,
  bepOptions: {
    font_size: "13pt", // "13pt" (12-14pt Standart BEP) veya "16pt" (Disleksi / Görme Güçlüğü)
    question_style: "karma", // "karma", "coktan_secmeli_3", "eslestirme_dy_bosluk"
    accommodation: "ek_sure", // "ek_sure" veya "okuyucu_kodlayici"
    show_bep_header: true,
    custom_outcomes: ""
  },
  isLoading: false
};

/**
 * Türkçe karakter kurallarına uygun büyütme fonksiyonu.
 * 'i' -> 'İ', 'ı' -> 'I' dönüşümünü ve geçmiş hatalı büyük harf metinlerini garantiler.
 */
function toTurkishUpper(str) {
  if (!str) return "";
  let s = String(str);
  // Daha önce yanlış İngilizce dönüşümle 'I' yapılmış yaygın MEB ders / senaryo kelimelerini düzelt
  s = s.replace(/\bDIN\b/g, "DİN")
       .replace(/\bBILGISI\b/g, "BİLGİSİ")
       .replace(/\bAHIRET\b/g, "AHİRET")
       .replace(/\bILISKI\b/g, "İLİŞKİ")
       .replace(/\bEGITIM\b/g, "EĞİTİM")
       .replace(/\bOGRETIM\b/g, "ÖĞRETİM");
  try {
    return s.toLocaleUpperCase("tr-TR");
  } catch (e) {
    return s.replace(/i/g, "İ").replace(/ı/g, "I").toUpperCase();
  }
}

function syncHeaderOptionsUI() {
  const chkAns = document.getElementById("chkShowAnswerLines");
  if (chkAns) chkAns.checked = (state.showAnswerLines !== false);
  const chkScen = document.getElementById("chkShowScenarioInHeader");
  if (chkScen) chkScen.checked = (state.showScenarioInHeader !== false);
  const chkBep = document.getElementById("chkShowBepInHeader");
  if (chkBep) chkBep.checked = (state.showBepInHeader !== false);

  const currentType = document.getElementById("examTypeSelect")?.value || state.currentExam?.exam_type || "yazili_sinav";
  const isBep = (currentType === "bep_sinav");

  const bepWrapper = document.getElementById("bepHeaderCheckboxWrapper");
  if (bepWrapper) {
    bepWrapper.classList.toggle("hidden", !isBep);
  }
  const scenWrapper = document.getElementById("scenarioHeaderCheckboxWrapper");
  if (scenWrapper) {
    scenWrapper.classList.toggle("hidden", isBep);
  }
}

// --- BAŞLANGIÇ ---
document.addEventListener("DOMContentLoaded", async () => {
  // 1. Önce hiçbir ağ isteğini beklemeden tüm form ve buton dinleyicilerini anında bağla!
  setupEventListeners();

  // 2. Kullanıcı oturumunu kontrol et
  checkAuth();

  // 3. Arka plan servislerini yükle (hata alsalar dahi giriş ekranı asla kilitlenmesin)
  try { await loadConfig(); } catch (e) { console.error("Config yükleme hatası:", e); }
  try { await loadScenarios(); } catch (e) { console.error("Senaryo yükleme hatası:", e); }
  try { await loadCurriculum(); } catch (e) { console.error("Müfredat yükleme hatası:", e); }
  try { loadSavedExamsList(); } catch (e) { console.error("Sınav listesi hatası:", e); }
  try { updatePaperHeaderLive(); } catch (e) {}
  try { startAutoSaveEngine(); } catch (e) {}
  try { await checkAndRestoreDraft(); } catch (e) { console.error("Taslak yükleme hatası:", e); }
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

async function loadScenarios() {
  try {
    const res = await fetch("/api/scenarios");
    const data = await res.json();
    if (data.status === "success" && data.scenarios_data) {
      state.scenariosData = data.scenarios_data;
    }
  } catch (e) {
    console.error("MEB Senaryoları yüklenemedi:", e);
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

window.quickLogin = function() {
  const uInput = document.getElementById("loginUsername");
  const pInput = document.getElementById("loginPassword");
  if (uInput) uInput.value = "nihal";
  if (pInput) pInput.value = "1234";
  window.handleLogin(null);
};

window.handleLogin = async function(e) {
  if (e && e.preventDefault) e.preventDefault();
  const uInput = document.getElementById("loginUsername");
  const pInput = document.getElementById("loginPassword");
  const username = uInput ? uInput.value.trim() : "nihal";
  const password = pInput ? pInput.value.trim() : "1234";
  const errEl = document.getElementById("loginError");
  if (errEl) errEl.classList.add("hidden");

  const btn = document.getElementById("btnLoginSubmit") || document.querySelector("#loginForm button[type='submit']");
  const origText = btn ? btn.innerHTML : "Öğretmen Girişi Yap";
  if (btn) {
    btn.innerHTML = `<span>⏳</span> Giriş Yapılıyor...`;
    btn.disabled = true;
  }

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || "Kullanıcı adı veya şifre hatalı!");
    }
    state.user = data.user;
    try {
      localStorage.setItem("ti_user", JSON.stringify(data.user));
    } catch (err) {}

    showApp();
    populateCurriculumUI();
    updatePaperHeaderLive();
    renderExamPages();
    showToast(`Hoş Geldiniz, ${data.user.teacher_name || "Nihal Öğretmen"}!`, "success");
  } catch (err) {
    if (errEl) {
      errEl.textContent = err.message || "Giriş yapılırken bir hata oluştu.";
      errEl.classList.remove("hidden");
    }
  } finally {
    if (btn) {
      btn.innerHTML = origText;
      btn.disabled = false;
    }
  }
};
const handleLogin = window.handleLogin;

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
    if (draftData.show_answer_lines !== undefined) {
      state.showAnswerLines = draftData.show_answer_lines;
    }
    if (draftData.show_scenario_in_header !== undefined) {
      state.showScenarioInHeader = draftData.show_scenario_in_header;
    }
    syncHeaderOptionsUI();
    
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

function getLocalScenariosFor(subjectId, grade, term) {
  if (!state.scenariosData || !state.scenariosData.levels) return [];
  const prefixMap = { dkab: "DKAB", siyer: "SIYER", kuran: "KURAN" };
  const prefix = prefixMap[subjectId] || "DKAB";
  const targetCode = `${prefix}-${grade}`;

  const lvl = state.scenariosData.levels.find(l => parseInt(l.grade, 10) === parseInt(grade, 10));
  if (!lvl || !lvl.courses) return [];

  const course = lvl.courses.find(c => c.course_code === targetCode || (c.course_code || "").startsWith(prefix));
  if (!course || !course.terms) return [];

  const termObj = course.terms.find(t => t.term === term);
  return termObj && Array.isArray(termObj.scenarios) ? termObj.scenarios : [];
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
        <input type="checkbox" id="unit_${u.id}" value="${u.id}" data-unit-no="${idx + 1}" class="unit-checkbox mt-0.5 rounded text-blue-600 focus:ring-blue-500" ${idx === 0 ? "checked" : ""}>
        <label for="unit_${u.id}" class="text-slate-700 cursor-pointer font-medium select-none">
          ${u.name}
          <span class="block text-[10px] text-slate-400 font-normal">Konular: ${(u.topics || []).slice(0, 3).join(", ")}...</span>
        </label>
      `;
      unitsContainer.appendChild(div);
    });
  }
  populateScenarioDropdown();
}

function populateScenarioDropdown() {
  const subjectId = document.getElementById("examSubject")?.value || "dkab";
  const grade = parseInt(document.getElementById("examGrade")?.value || "5", 10);
  const term = document.getElementById("examTerm")?.value || "1. Dönem";
  const scenarioSelect = document.getElementById("examScenario");
  if (!scenarioSelect) return;

  const scenarios = getLocalScenariosFor(subjectId, grade, term);
  state.activeScenarioList = scenarios;

  const prevVal = scenarioSelect.value;
  scenarioSelect.innerHTML = "";

  scenarios.forEach((sc, idx) => {
    const opt = document.createElement("option");
    opt.value = sc.name || `Senaryo ${sc.scenario_id || idx + 1}`;
    opt.textContent = `${sc.name} (${sc.total_questions || 6} Soru)`;
    scenarioSelect.appendChild(opt);
  });

  // Özel seçeneğini her zaman en sona ekle
  const customOpt = document.createElement("option");
  customOpt.value = "Özel";
  customOpt.textContent = "✨ Özel (Serbest Konu & Soru Seçimi)";
  scenarioSelect.appendChild(customOpt);

  // Eğer önceden Özel seçiliyse koru, yoksa ilk MEB senaryosunu seç
  if (prevVal === "Özel") {
    scenarioSelect.value = "Özel";
  } else if (scenarios.some(s => s.name === prevVal)) {
    scenarioSelect.value = prevVal;
  } else if (scenarios.length > 0) {
    scenarioSelect.value = scenarios[0].name;
  }

  onScenarioChange();
}

function toggleQuickBepMode() {
  const typeSelect = document.getElementById("examTypeSelect");
  if (!typeSelect) return;
  if (typeSelect.value === "bep_sinav") {
    typeSelect.value = "yazili_sinav";
  } else {
    typeSelect.value = "bep_sinav";
  }
  onExamTypeChange();
}

function onExamTypeChange() {
  const typeSelect = document.getElementById("examTypeSelect");
  const examType = typeSelect ? typeSelect.value : "yazili_sinav";
  const isBep = (examType === "bep_sinav");

  const quickBtn = document.getElementById("btnQuickBepToggle");
  const quickBtnText = document.getElementById("btnQuickBepToggleText");
  if (quickBtn && quickBtnText) {
    if (isBep) {
      quickBtn.className = "text-[10px] bg-teal-700 hover:bg-teal-800 text-white border border-teal-800 px-2 py-0.5 rounded-full font-extrabold transition flex items-center gap-1 shadow";
      quickBtnText.textContent = "BEP Modu Aktif ✓";
    } else {
      quickBtn.className = "text-[10px] bg-teal-100 hover:bg-teal-200 text-teal-900 border border-teal-300 px-2 py-0.5 rounded-full font-extrabold transition flex items-center gap-1 shadow-xs";
      quickBtnText.textContent = "BEP Sınavı Seç";
    }
  }

  const scenarioSelect = document.getElementById("examScenario");
  const qCountInput = document.getElementById("examQuestionCount");
  const diffSelect = document.getElementById("examDifficulty");

  if (isBep) {
    // 1. MEB BEP Yönetmeliği: Tek sütun düzenini otomatik seç
    state.currentExam.layout = "1_column";
    const btn2 = document.getElementById("btnLayout2Col");
    const btn1 = document.getElementById("btnLayout1Col");
    if (btn1 && btn2) {
      btn1.className = "px-2.5 py-1 text-xs font-semibold rounded bg-blue-600 text-white shadow";
      btn2.className = "px-2.5 py-1 text-xs font-semibold rounded bg-slate-200 text-slate-700 hover:bg-slate-300";
    }

    // 2. Soru sayısını 5 (5x20=100 Puan) veya 4 (4x25=100 Puan) bandına çek
    if (qCountInput && parseInt(qCountInput.value, 10) > 5) {
      qCountInput.value = 5;
    }

    // 3. Zorluk seviyesini Kolay (BEP Temel Seviye) yap
    if (diffSelect) {
      diffSelect.value = "Kolay";
    }

    // 4. Senaryo kutusuna "BEP Bireysel Kazanım" ekle ve seç
    if (scenarioSelect) {
      if (!Array.from(scenarioSelect.options).some(o => o.value === "BEP Bireysel Kazanım")) {
        const bepOpt = document.createElement("option");
        bepOpt.value = "BEP Bireysel Kazanım";
        bepOpt.textContent = "♿ BEP Bireysel Kazanım Planı (Senaryodan Muaf)";
        scenarioSelect.insertBefore(bepOpt, scenarioSelect.firstChild);
      }
      scenarioSelect.value = "BEP Bireysel Kazanım";
    }

    renderBepSummaryBox();
    updatePaperHeaderLive();
    syncHeaderOptionsUI();
    renderExamPages();
    showToast("♿ BEP Sınav Modu aktif edildi: Tek sütun, 12-14/16 punto okunaklı yazı tipi, 5 soru (5x20p) ve sadeleştirilmiş soru tipleri ayarlandı.", "info");
  } else {
    populateScenarioDropdown();
    updatePaperHeaderLive();
    syncHeaderOptionsUI();
    renderExamPages();
  }
}

function updateBepOption(field, value) {
  if (!state.bepOptions) state.bepOptions = {};
  state.bepOptions[field] = value;
  if (state.currentExam) {
    state.currentExam.bep_options = { ...state.bepOptions };
  }
  if (field === "font_size" || field === "accommodation") {
    renderExamPages();
  }
}

function applyQuickBepQuestionCount(cnt) {
  const qCountInput = document.getElementById("examQuestionCount");
  if (qCountInput) {
    qCountInput.value = cnt;
  }
  renderBepSummaryBox();
}

function renderBepSummaryBox() {
  const box = document.getElementById("activeScenarioSummaryBox");
  if (!box) return;

  const opts = state.bepOptions || {
    font_size: "13pt",
    question_style: "karma",
    accommodation: "ek_sure",
    custom_outcomes: ""
  };
  const qCnt = parseInt(document.getElementById("examQuestionCount")?.value || "5", 10);

  box.className = "bg-teal-50/80 border-2 border-teal-300 rounded-xl p-3 space-y-2.5 shadow-xs";
  box.innerHTML = `
    <div class="flex items-center justify-between border-b border-teal-200 pb-1.5">
      <div class="text-xs font-extrabold text-teal-950 flex items-center gap-1.5">
        <span>♿</span> BEP Sınavı Hızlı Uyarlama Paneli
      </div>
      <span class="bg-teal-700 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
        Senaryodan Muaf
      </span>
    </div>

    <p class="text-[10px] text-teal-900 leading-snug">
      MEB Özel Eğitim Yönetmeliği gereği <strong>Tek Sütun</strong>, <strong>1.5 Satır Aralığı</strong> ve <strong>Olumlu/Sade Yönerge</strong> kuralları otomatiktir.
    </p>

    <!-- Hızlı Soru & Net Puan Seçimi (4x25p veya 5x20p) -->
    <div>
      <label class="block text-[10px] font-bold text-teal-950 mb-1">1. Soru Sayısı ve Net Puanlama:</label>
      <div class="grid grid-cols-2 gap-1.5">
        <button type="button" onclick="applyQuickBepQuestionCount(4)"
                class="py-1 px-2 rounded border text-[10px] font-bold transition ${qCnt === 4 ? 'bg-teal-700 text-white border-teal-800 shadow-xs' : 'bg-white text-teal-900 border-teal-200 hover:bg-teal-100'}">
          4 Soru × 25 Puan = 100
        </button>
        <button type="button" onclick="applyQuickBepQuestionCount(5)"
                class="py-1 px-2 rounded border text-[10px] font-bold transition ${qCnt === 5 ? 'bg-teal-700 text-white border-teal-800 shadow-xs' : 'bg-white text-teal-900 border-teal-200 hover:bg-teal-100'}">
          5 Soru × 20 Puan = 100
        </button>
      </div>
    </div>

    <!-- Soru Çeşitliliği Şablonu -->
    <div>
      <label class="block text-[10px] font-bold text-teal-950 mb-1">2. BEP Soru Tipleri Dağılımı:</label>
      <select onchange="updateBepOption('question_style', this.value)"
              class="w-full text-[11px] py-1.5 px-2 bg-white border border-teal-300 rounded font-semibold text-slate-800">
        <option value="karma" ${opts.question_style === 'karma' ? 'selected' : ''}>⭐ Karma BEP (Eşleştirme + D/Y + Kelime Havuzlu + 3 Şıklı)</option>
        <option value="coktan_secmeli_3" ${opts.question_style === 'coktan_secmeli_3' ? 'selected' : ''}>🔘 Sadece 3 Seçenekli Çoktan Seçmeli (A, B, C)</option>
        <option value="eslestirme_dy_bosluk" ${opts.question_style === 'eslestirme_dy_bosluk' ? 'selected' : ''}>✍️ Eşleştirme + Doğru/Yanlış + Kelime Havuzlu Boşluk</option>
      </select>
    </div>

    <!-- Punto ve Tipografi + Sınav Tedbiri -->
    <div class="grid grid-cols-2 gap-1.5">
      <div>
        <label class="block text-[10px] font-bold text-teal-950 mb-0.5">3. Yazı Büyüklüğü (Punto):</label>
        <select onchange="updateBepOption('font_size', this.value)"
                class="w-full text-[10px] py-1 px-1.5 bg-white border border-teal-300 rounded font-semibold text-slate-800">
          <option value="13pt" ${opts.font_size !== '16pt' ? 'selected' : ''}>12-14 pt (Standart BEP)</option>
          <option value="16pt" ${opts.font_size === '16pt' ? 'selected' : ''}>16 pt (Disleksi / Görme)</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] font-bold text-teal-950 mb-0.5">4. Sınav Tedbiri Notu:</label>
        <select onchange="updateBepOption('accommodation', this.value)"
                class="w-full text-[10px] py-1 px-1.5 bg-white border border-teal-300 rounded font-semibold text-slate-800">
          <option value="ek_sure" ${opts.accommodation !== 'okuyucu_kodlayici' ? 'selected' : ''}>+%25-%50 Ek Süre</option>
          <option value="okuyucu_kodlayici" ${opts.accommodation === 'okuyucu_kodlayici' ? 'selected' : ''}>Okuyucu/Kodlayıcı + Ek Süre</option>
        </select>
      </div>
    </div>

    <!-- İsteğe Bağlı Bireysel BEP Kazanımı -->
    <div>
      <label class="block text-[10px] font-bold text-teal-950 mb-0.5">5. Bireysel BEP Dosyası Kazanımı (İsteğe Bağlı):</label>
      <textarea rows="2" placeholder="Boş bırakırsanız seçili ünitenin en temel BEP kazanımları otomatik kullanılır..."
                oninput="updateBepOption('custom_outcomes', this.value)"
                class="w-full text-[10px] p-1.5 bg-white border border-teal-300 rounded text-slate-800 leading-snug">${opts.custom_outcomes || ""}</textarea>
    </div>
  `;
}

function onScenarioChange() {
  const examType = document.getElementById("examTypeSelect")?.value || "yazili_sinav";
  if (examType === "bep_sinav") {
    renderBepSummaryBox();
    updatePaperHeaderLive();
    return;
  }

  const box = document.getElementById("activeScenarioSummaryBox");
  if (box) {
    box.className = "bg-indigo-50/60 border border-indigo-200 rounded-lg p-2.5 space-y-1.5";
  }

  const scenarioVal = document.getElementById("examScenario")?.value || "Senaryo 1";
  const qCountInput = document.getElementById("examQuestionCount");
  const scenarios = state.activeScenarioList || [];

  if (scenarioVal === "Özel" || scenarioVal === "BEP Bireysel Kazanım") {
    state.activeScenarioObj = null;
    renderActiveScenarioSummaryBox(null);
    updatePaperHeaderLive();
    return;
  }

  const matchedSc = scenarios.find(s => s.name === scenarioVal) || scenarios[0] || null;
  state.activeScenarioObj = matchedSc;

  if (matchedSc) {
    // 1. Soru adedini senaryodaki toplam soru sayısına eşitle
    const totalQ = (matchedSc.items || []).reduce((acc, it) => acc + (parseInt(it.question_count, 10) || 0), 0) || matchedSc.total_questions || 6;
    if (qCountInput) {
      qCountInput.value = totalQ;
    }

    // 2. Senaryodaki unit_no değerlerine göre Ders Kitabı Üniteleri checkbox'larını otomatik işaretle
    const targetUnitNos = new Set((matchedSc.items || []).map(it => parseInt(it.unit_no, 10)));
    if (targetUnitNos.size > 0) {
      document.querySelectorAll(".unit-checkbox").forEach(cb => {
        const uNo = parseInt(cb.getAttribute("data-unit-no") || "0", 10);
        cb.checked = targetUnitNos.has(uNo);
      });
    }
  }

  renderActiveScenarioSummaryBox(matchedSc);
  updatePaperHeaderLive();
}

function renderActiveScenarioSummaryBox(scenarioObj) {
  const box = document.getElementById("activeScenarioSummaryBox");
  if (!box) return;

  if (!scenarioObj) {
    box.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-bold text-amber-900 flex items-center gap-1">
          <span>✨</span> Özel Mod (Serbest Konu & Soru Seçimi)
        </span>
        <button type="button" onclick="openScenarioManager()" class="text-[10px] text-indigo-700 hover:underline font-bold">
          Senaryoları Gör
        </button>
      </div>
      <p class="text-[10px] text-slate-600 leading-snug">
        Aşağıdaki <strong>Soru Adedi</strong> ve <strong>Ders Kitabı Üniteleri</strong> alanlarından istediğiniz ünite ve soru sayısını serbestçe seçerek soru oluşturabilirsiniz.
      </p>
    `;
    return;
  }

  const items = scenarioObj.items || [];
  const totalQ = items.reduce((acc, it) => acc + (parseInt(it.question_count, 10) || 0), 0) || scenarioObj.total_questions || 6;

  const itemsHtml = items.map(it => `
    <div class="flex items-start justify-between gap-1.5 bg-white/90 border border-indigo-100 rounded px-2 py-1 text-[10px]">
      <div class="flex-1 min-w-0">
        <span class="font-bold text-indigo-900">[${it.outcome_code || "Kazanım"}]</span>
        <span class="text-slate-700">${it.outcome_description || ""}</span>
        <span class="block text-[9px] text-slate-400 font-medium">${it.unit_no}. Ünite: ${it.unit_title || ""}</span>
      </div>
      <span class="shrink-0 bg-indigo-100 text-indigo-900 font-extrabold px-1.5 py-0.5 rounded text-[10px]">
        ${it.question_count} Soru
      </span>
    </div>
  `).join("");

  box.innerHTML = `
    <div class="flex items-center justify-between border-b border-indigo-200/70 pb-1">
      <div class="text-[11px] font-extrabold text-indigo-950 truncate" title="${scenarioObj.name}">
        🎯 ${scenarioObj.name}
      </div>
      <div class="flex items-center gap-1.5 shrink-0">
        <span class="bg-indigo-700 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">
          Toplam ${totalQ} Soru
        </span>
        <button type="button" onclick="openScenarioManager()" 
                class="text-[10px] bg-white hover:bg-indigo-100 text-indigo-800 border border-indigo-300 px-1.5 py-0.5 rounded font-bold transition"
                title="Bu senaryodaki kazanımları, konuları ve soru adetlerini düzenle">
          ✏️ Düzenle
        </button>
      </div>
    </div>
    <div class="space-y-1 max-h-36 overflow-y-auto pr-0.5">
      ${itemsHtml}
    </div>
  `;
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
  const scenario_items = (exam_type !== "bep_sinav" && scenario !== "Özel" && state.activeScenarioObj && Array.isArray(state.activeScenarioObj.items))
    ? state.activeScenarioObj.items
    : [];

  setLoading(true, exam_type === "bep_sinav"
    ? "MEB Özel Eğitim & BEP Yönergesine uygun bireyselleştirilmiş sorular hazırlanıyor..."
    : "MEB Senaryosu ve Ders Kitapları taranarak sorular hazırlanıyor...");

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
        scenario: exam_type === "bep_sinav" ? "BEP Bireysel Kazanım" : scenario,
        question_count,
        selected_units: checkedUnits,
        difficulty: exam_type === "bep_sinav" ? "Kolay" : difficulty,
        scenario_items,
        bep_options: state.bepOptions || {}
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Soru hazırlama başarısız.");
    }

    const data = await res.json();
    const questions = data.data.questions || [];

    const subjName = state.curriculum[subject]?.name || subject;
    const isBepExam = (exam_type === "bep_sinav");
    state.currentExam = {
      id: null,
      title: isBepExam
        ? `${grade}. Sınıf ${subjName} ${term} ${exam_no} (BEP Kapsamındaki Öğrenci Sınavı)`
        : `${grade}. Sınıf ${subjName} ${term} ${exam_no}`,
      exam_type,
      subject,
      subject_name: subjName,
      grade,
      term,
      exam_no,
      scenario: isBepExam ? "BEP Bireysel Kazanım" : scenario,
      layout: isBepExam ? "1_column" : (state.currentExam.layout || "2_column"),
      show_answer_lines: (state.showAnswerLines !== false),
      show_scenario_in_header: (state.showScenarioInHeader !== false),
      bep_options: isBepExam ? { ...(state.bepOptions || {}) } : {},
      total_points: 100,
      questions
    };

    recalculateTotalPoints();
    renderExamPages();
    
    // Soru hazırlandığında 1 defa ANINDA taslak kaydet (Kullanıcı Talebi)
    await saveDraft(true);

    showToast(isBepExam ? "♿ BEP Kapsamındaki Öğrenci Sınavı başarıyla hazırlandı!" : "Sınav ve sorular başarıyla hazırlandı!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

// ==============================================================
// GELİŞMİŞ ÇOKLU SAYFALAMA VE DENGELİ DAĞITIM MOTORU (PAGINATION ENGINE)
// Standart ve BEP sınavlarında soruların görsel yüksekliğini hesaplar,
// tek sayfaya sığıyorsa homojen sığdırır, 2. sayfaya taşıyorsa (örn. 5 soruda 3+2,
// 4 uzun soruda 2+2, 6 soruda 3+3) sayfalar arasında dengeli dağıtır ve taşmayı önler.
// ==============================================================
function getEffectiveQuestionOptions(q, isBep = false, bepOpts = {}) {
  const opts = Array.isArray(q.options) ? q.options : [];
  if (opts.length === 0) return [];
  if (isBep) {
    const qType = String(q.question_type || "");
    const qTxt = String(q.question_text || "");
    const qStyle = bepOpts.question_style || "karma";
    if (
      qStyle !== "coktan_secmeli_3" &&
      (
        qType === "bep_eslestirme" ||
        qType === "bep_dogru_yanlis" ||
        qType === "bep_bosluk_doldurma" ||
        qTxt.includes("KELİME HAVUZU") ||
        qTxt.includes("( ..... )") ||
        qTxt.includes(".... ( a )")
      )
    ) {
      return [];
    }
  }
  return opts;
}

function isShortThreeColOptions(opts) {
  if (!Array.isArray(opts) || opts.length !== 3) return false;
  return opts.every(o => String(o || "").trim().length <= 36);
}

function estimateQuestionVisualWeight(q, ctx = {}) {
  const isBep = Boolean(ctx.isBep);
  const isLargeBepFont = Boolean(ctx.isLargeBepFont);
  const is2Col = Boolean(ctx.is2Col);
  const bepOpts = ctx.bepOpts || {};

  const rawText = String(q.question_text || "").trim();
  const cleanText = isBep ? rawText.replace(/\n{2,}/g, "\n") : rawText;
  const explicitLines = cleanText.split("\n").length;
  const charsPerLine = is2Col ? (isBep ? 42 : 52) : (isLargeBepFont ? 62 : (isBep ? 75 : 88));
  const wrappedLines = cleanText.split("\n").reduce((acc, line) => {
    return acc + Math.max(1, Math.ceil(line.length / charsPerLine));
  }, 0);

  let weight = 2.2 + Math.max(explicitLines, wrappedLines) * (isLargeBepFont ? 1.35 : (isBep ? 1.15 : 1.0));

  if (q.arabic_text && String(q.arabic_text).trim().length > 0) {
    weight += isLargeBepFont ? 2.4 : 1.9;
  }

  const effectiveOpts = getEffectiveQuestionOptions(q, isBep, bepOpts);
  if (effectiveOpts.length > 0) {
    if (isShortThreeColOptions(effectiveOpts) && !is2Col) {
      weight += 1.6;
    } else {
      weight += effectiveOpts.length * (isLargeBepFont ? 1.35 : 1.1);
    }
  } else {
    const ansLines = calculateOptimalAnswerLines(q, { is2Col, colQuestionCount: 3, pageIdx: 0 });
    if (ansLines > 0) {
      weight += ansLines * 0.95;
    }
  }

  return Math.max(3, Math.round(weight * 10) / 10);
}

function splitQuestionsIntoBalancedPages(questions, totalPages, ctx = {}) {
  if (totalPages <= 1 || questions.length <= 1) {
    return [{ items: questions.slice(), startIndex: 0 }];
  }

  const clampedPages = Math.min(totalPages, questions.length);
  const weights = questions.map(q => estimateQuestionVisualWeight(q, ctx));
  const result = [];
  let cursor = 0;

  for (let p = 0; p < clampedPages; p++) {
    const remainingQuestions = questions.length - cursor;
    const remainingPages = clampedPages - p;

    if (remainingPages <= 1) {
      result.push({
        items: questions.slice(cursor),
        startIndex: cursor
      });
      break;
    }

    // Temel dengeli adet: örn. 5 soru / 2 sayfa => Sayfa 1: 3 soru, Sayfa 2: 2 soru
    // 4 soru / 2 sayfa => 2 + 2; 6 soru / 2 sayfa => 3 + 3; 7 soru / 2 sayfa => 4 + 3
    let idealCount = Math.ceil(remainingQuestions / remainingPages);

    // Eğer 1. sayfada antet + öğrenci tablosu varken ilk sorular aşırı uzunsa (örn. 5 soruda ilk 3 sorunun ağırlığı
    // kalan 2 sorunun ağırlığının 1.65 katından fazlaysa), 2 + 3 veya dengeli ağırlık kesimini tercih et
    if (remainingPages === 2 && remainingQuestions >= 4) {
      const lowCount = Math.floor(remainingQuestions / 2);
      const highCount = Math.ceil(remainingQuestions / 2);
      if (lowCount !== highCount && lowCount >= 2) {
        const weightHigh = weights.slice(cursor, cursor + highCount).reduce((a, b) => a + b, 0) + (p === 0 ? 2.5 : 0);
        const weightRestAfterHigh = weights.slice(cursor + highCount).reduce((a, b) => a + b, 0);
        const weightLow = weights.slice(cursor, cursor + lowCount).reduce((a, b) => a + b, 0) + (p === 0 ? 2.5 : 0);
        const weightRestAfterLow = weights.slice(cursor + lowCount).reduce((a, b) => a + b, 0);

        if (Math.abs(weightLow - weightRestAfterLow) + 1.5 < Math.abs(weightHigh - weightRestAfterHigh)) {
          idealCount = lowCount;
        }
      }
    }

    result.push({
      items: questions.slice(cursor, cursor + idealCount),
      startIndex: cursor
    });
    cursor += idealCount;
  }

  return result;
}

function renderExamPages(forcedPageCount = null) {
  const container = document.getElementById("examPagesContainer");
  if (!container) return;
  container.innerHTML = "";

  const exam = state.currentExam;
  const questions = exam.questions || [];
  syncHeaderOptionsUI();

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

  const isBep = (exam.exam_type === "bep_sinav");
  const bepOpts = exam.bep_options || state.bepOptions || {};
  const isLargeBepFont = (isBep && bepOpts.font_size === "16pt");
  const showBepBanner = (isBep && state.showBepInHeader !== false && bepOpts.show_bep_header !== false);
  syncHeaderOptionsUI();

  // Kullanıcının "Tek Sütun" / "2 Sütun" tercihine saygı duy (BEP seçildiğinde varsayılan 1_column olarak gelir,
  // ancak öğretmen 2 Sütun'a tıklarsa 2 sütunlu dengeli yerleşim de çalışır)
  const is2Col = (exam.layout === "2_column");

  const weightCtx = { isBep, isLargeBepFont, is2Col, bepOpts };
  const totalWeight = questions.reduce((sum, q) => sum + estimateQuestionVisualWeight(q, weightCtx), 0);

  // Başlangıç hedef sayfa sayısı:
  let totalPages = 1;
  if (typeof forcedPageCount === "number" && forcedPageCount >= 1) {
    totalPages = Math.min(forcedPageCount, questions.length);
  } else if (is2Col) {
    const maxPer2ColPage = isLargeBepFont ? 4 : 6;
    totalPages = Math.ceil(questions.length / maxPer2ColPage);
  } else if (isBep) {
    if (isLargeBepFont) {
      // 16pt Disleksi/Görme Güçlüğü modunda 1 sayfaya en fazla 3 soru sığar; 4-5 soruda dengeli 2 sayfaya (2+2 veya 3+2) bölünür
      totalPages = (questions.length > 3 || totalWeight > 25) ? Math.ceil(questions.length / 3) : 1;
    } else {
      // 13pt Standart BEP modunda: 4-5 soru normal uzunluktaysa 1 sayfaya sığar; 6+ soru veya çok uzun 5 soruysa 2 sayfaya dengeli (3+2 / 3+3) bölünür
      const singlePageWeightLimit = 36.5;
      if (questions.length > 5 || totalWeight > singlePageWeightLimit) {
        totalPages = Math.max(2, Math.ceil(questions.length / 4));
      } else {
        totalPages = 1;
      }
    }
  } else {
    // Standart yazılı Tek Sütun
    const maxPer1ColPage = 4;
    totalPages = (questions.length > maxPer1ColPage || totalWeight > 34)
      ? Math.ceil(questions.length / 3)
      : 1;
  }

  const pageBuckets = splitQuestionsIntoBalancedPages(questions, totalPages, weightCtx);
  const actualTotalPages = pageBuckets.length;

  for (let pageIdx = 0; pageIdx < actualTotalPages; pageIdx++) {
    const bucket = pageBuckets[pageIdx];
    const pageQuestions = bucket.items;
    const baseIndex = bucket.startIndex;

    const sheetDiv = document.createElement("div");
    sheetDiv.className = `a4-sheet${isBep ? " bep-sheet" : ""}${isLargeBepFont ? " bep-font-16" : ""}`;
    sheetDiv.dataset.pageNumber = pageIdx + 1;

    // 1. Sayfa MEB Resmi Anteti; 2. ve sonraki sayfalar için Devam Başlığı
    let headerHtml = "";
    if (pageIdx === 0) {
      const showScenario = (state.showScenarioInHeader !== false);
      const scenarioPart = (!isBep && showScenario && exam.scenario) ? ` (${toTurkishUpper(exam.scenario)})` : "";
      const typeTitle = isBep
        ? `${toTurkishUpper(exam.term || "1. Dönem")} ${toTurkishUpper(exam.exam_no || "1. Yazılı")} SINAVI`
        : exam.exam_type === "etut_calisma" ? "ÇALIŞMA VE ETÜT KAĞIDI" 
        : exam.exam_type === "yaprak_test" ? "KAZANIM DEĞERLENDİRME TESTİ" 
        : `${toTurkishUpper(exam.term || "1. Dönem")} ${toTurkishUpper(exam.exam_no || "1. Yazılı")} SINAVI${scenarioPart}`;

      const bepBannerHtml = showBepBanner
        ? `<div class="bep-official-banner">♿ BEP KAPSAMINDAKİ ÖĞRENCİ SINAVI (BİREYSELLEŞTİRİLMİŞ EĞİTİM PROGRAMI)</div>`
        : "";

      const schoolHdr = toTurkishUpper(state.config.school_header || "T.C. MİLLÎ EĞİTİM BAKANLIĞI");
      const schoolName = toTurkishUpper(state.config.school_name || "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu");
      const subjectTitle = toTurkishUpper(exam.subject_name || "DİN KÜLTÜRÜ VE AHLAK BİLGİSİ");

      headerHtml = `
        <div class="meb-header">
          <h3>${schoolHdr}</h3>
          <h3>${schoolName}</h3>
          <h4>2026-2027 EĞİTİM ÖĞRETİM YILI ${exam.grade}. SINIF ${subjectTitle} DERSİ</h4>
          <div class="exam-sub">${typeTitle}</div>
          ${bepBannerHtml}
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
          <span>${toTurkishUpper(state.config.school_name || "Tevfik İleri İmam Hatip Ortaokulu")}</span>
          <span>${exam.grade}. Sınıf ${toTurkishUpper(exam.subject_name || "Ders")} ${showBepBanner ? "• BEP SINAVI" : ""} • (Sayfa ${pageIdx + 1} / ${actualTotalPages})</span>
        </div>
      `;
    }

    // Soruların Yerleşimi (2 Sütun veya 1 Sütun)
    let questionsHtml = "";
    if (is2Col) {
      const mid = Math.ceil(pageQuestions.length / 2);
      const col1 = pageQuestions.slice(0, mid);
      const col2 = pageQuestions.slice(mid);

      const renderCol = (list, offset, colQuestionCount) =>
        list.map((q, idx) => createQuestionCardHtml(q, baseIndex + offset + idx, {
          is2Col: true,
          isBep,
          isLargeBepFont,
          bepOpts,
          colQuestionCount,
          maxColQuestions: mid,
          pageIdx
        })).join("");

      questionsHtml = `
        <div class="exam-layout-2col">
          <div class="column-container col-count-${col1.length}">${renderCol(col1, 0, col1.length)}</div>
          <div class="column-container col-count-${col2.length}">${renderCol(col2, mid, col2.length)}</div>
        </div>
      `;
    } else {
      questionsHtml = `
        <div class="exam-layout-1col onecol-count-${pageQuestions.length}">
          ${pageQuestions.map((q, idx) => createQuestionCardHtml(q, baseIndex + idx, {
            is2Col: false,
            isBep,
            isLargeBepFont,
            bepOpts,
            colQuestionCount: pageQuestions.length,
            maxColQuestions: pageQuestions.length,
            pageIdx
          })).join("")}
        </div>
      `;
    }

    // Alt Bilgi
    const accomNote = (bepOpts.accommodation === "okuyucu_kodlayici")
      ? "Okuyucu/Kodlayıcı Desteği & +%25-%50 Ek Süre"
      : "+%25-%50 BEP Ek Süresi";
    const footerLeftText = isBep
      ? `BEP Kapsamındaki Öğrenci Sınavı (${accomNote}) • Yazım/noktalama hatalarından puan kırılmaz.`
      : "Sınav süresi 40 dakikadır. Başarılar dilerim.";

    const footerHtml = `
      <div class="exam-footer">
        <span>${footerLeftText}</span>
        <span>Sayfa ${pageIdx + 1} / ${actualTotalPages}</span>
      </div>
    `;

    sheetDiv.innerHTML = headerHtml + questionsHtml + footerHtml;
    container.appendChild(sheetDiv);
  }

  // Gerçek DOM Yükseklik & Taşma Kontrolü (Auto-Fit veya Dengeli Alt Sayfaya Bölme):
  // Eğer sorular tek sayfada (veya mevcut sayfada) piksel olarak taşıyorsa:
  // 1) Önce hafif sıkılaştırma (bep-compact-1 / bep-compact-2) dene.
  // 2) Hâlâ taşıyorsa (örn. 5 uzun BEP sorusu tek sayfaya sığmıyorsa) otomatik olarak sayfa sayısını 1 artırıp
  //    soruları 3 + 2 (veya 2 + 2) şeklinde dengeli iki sayfaya böl!
  const sheets = Array.from(container.querySelectorAll(".a4-sheet"));
  let needsMorePages = false;

  for (const sheetEl of sheets) {
    const layoutEl = sheetEl.querySelector(".exam-layout-1col, .exam-layout-2col");
    if (!layoutEl) continue;

    const isOverflowing = () => layoutEl.scrollHeight > layoutEl.clientHeight + 3;

    if (isOverflowing()) {
      if (isBep && !isLargeBepFont) {
        sheetEl.classList.add("bep-compact-1");
        if (isOverflowing() && actualTotalPages === 1 && questions.length <= 5) {
          sheetEl.classList.add("bep-compact-2");
        }
      }
      if (isOverflowing()) {
        const qItemsInSheet = sheetEl.querySelectorAll(".question-item").length;
        if (qItemsInSheet >= 2) {
          needsMorePages = true;
          break;
        }
      }
    }
  }

  const maxReasonablePages = Math.max(1, Math.ceil(questions.length / 2));
  if (needsMorePages && actualTotalPages < maxReasonablePages) {
    renderExamPages(actualTotalPages + 1);
    return;
  }

  // Diğer sekmeleri de güncelle
  renderAnswerKeySheet();
  renderSourceVerificationSheet();
}

// Cevap Uzunluğuna, Sütun Soru Sayısına ve Sayfa Yüksekliğine Göre Dengeli Çizgi Sayısı Hesaplayıcı
function calculateOptimalAnswerLines(q, layoutCtx = {}) {
  if (q.options && q.options.length > 0) return 0;

  const qType = String(q.question_type || "");
  const qTxt = String(q.question_text || "");
  // BEP yapılandırılmış sorularda (Eşleştirme, Doğru-Yanlış, Kelime Havuzlu Boşluk Doldurma) soru metninin kendisi boşluk/tablo içerdiğinden ekstra noktalı satır basılmaz
  if (
    qType === "bep_eslestirme" ||
    qType === "bep_dogru_yanlis" ||
    qType === "bep_bosluk_doldurma" ||
    qType === "bep_coktan_secmeli_3" ||
    qTxt.includes("KELİME HAVUZU") ||
    qTxt.includes("( ..... )") ||
    qTxt.includes(".... ( a )")
  ) {
    return 0;
  }

  const is2Col = layoutCtx.is2Col !== undefined ? layoutCtx.is2Col : true;
  const colCount = layoutCtx.colQuestionCount || 3;
  const pageIdx = layoutCtx.pageIdx || 0;

  // Sütundaki soru adedine ve sayfa antet yüksekliğine göre temel satır sayısı
  let lines = 4;
  if (is2Col) {
    if (colCount >= 3) {
      lines = pageIdx === 0 ? 4 : 5;
    } else if (colCount === 2) {
      lines = pageIdx === 0 ? 5 : 6;
    } else {
      lines = 6;
    }
  } else {
    lines = pageIdx === 0 ? 4 : 5;
  }

  const ans = (q.answer_text || "").trim();
  const newlineCount = (ans.match(/\n/g) || []).length + 1;
  const charCount = ans.length;
  const qTextLen = (q.question_text || "").trim().length;
  const hasArabic = Boolean(q.arabic_text && q.arabic_text.trim().length > 0);

  // Cevap anahtarındaki çözüm uzunsa +1 satır ekle
  if (charCount > 220 || newlineCount >= 3) {
    lines += 1;
  }

  // Arapça ayet kutusu veya çok uzun soru köklerinde kart boyunu dengelemek için -1 satır
  if (hasArabic) {
    lines -= 1;
  }
  if (qTextLen > 260) {
    lines -= 1;
  }

  return Math.max(3, Math.min(7, lines));
}

function createQuestionCardHtml(q, index, layoutCtx = {}) {
  const isBep = Boolean(layoutCtx.isBep);
  const bepOpts = layoutCtx.bepOpts || {};
  const is2Col = Boolean(layoutCtx.is2Col);
  const arabicHtml = q.arabic_text ? `<div class="arabic-text" contenteditable="true" onblur="updateArabicText(${index}, this.innerText)">${q.arabic_text}</div>` : "";
  
  // Çoktan seçmeli test şıkları varsa göster (BEP eşleştirme/boşluk/D-Y sorularında mükerrer şık kutusu basılmaz)
  const effectiveOptions = getEffectiveQuestionOptions(q, isBep, bepOpts);
  let optionsHtml = "";
  if (effectiveOptions.length > 0) {
    const use3ColRow = (!is2Col && isShortThreeColOptions(effectiveOptions));
    optionsHtml = `
      <div class="options-list${use3ColRow ? " options-3col-row" : ""}">
        ${effectiveOptions.map(opt => `<div class="p-1 bg-slate-50 border rounded text-[8pt]">${opt}</div>`).join("")}
      </div>
    `;
  }

  // Cevap anahtarındaki çözüm uzunluğuna ve soru görsel yüksekliğine göre dengeli esneme (flex) ağırlığı
  const optimalLines = calculateOptimalAnswerLines(q, layoutCtx);
  const ansLen = (q.answer_text || "").trim().length;
  let flexWeight = ansLen > 240 ? "1.15" : "1";
  if (isBep) {
    const qWeight = estimateQuestionVisualWeight(q, layoutCtx);
    flexWeight = String(Math.max(0.85, Math.min(1.5, Math.round((qWeight / 6.5) * 100) / 100)));
  }

  const displayQuestionText = isBep
    ? String(q.question_text || "").replace(/\n{2,}/g, "\n").trim()
    : (q.question_text || "");

  let answerLinesHtml = "";
  if (optimalLines > 0) {
    if (state.showAnswerLines !== false) {
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
    } else {
      answerLinesHtml = `
        <div class="answer-space">
          <div class="answer-header-row">
            <span class="text-[7.5pt] text-slate-400 font-semibold">Cevap:</span>
          </div>
          <div class="answer-blank-box"></div>
        </div>
      `;
    }
  }

  return `
    <div class="question-item" data-index="${index}" style="flex: ${flexWeight} 1 auto;">
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

      <div class="question-text-editable" contenteditable="true" onblur="updateQuestionText(${index}, this.innerText)">${displayQuestionText}</div>

      ${optionsHtml}
      ${answerLinesHtml}
    </div>
  `;
}

// --- TEK MERKEZLİ GÜNCELLEMELER ---
function updateQuestionText(idx, newText) {
  if (state.currentExam.questions[idx]) {
    state.currentExam.questions[idx].question_text = newText.trim();
    if (state.activeTab !== "exam") {
      renderExamPages();
    } else {
      renderAnswerKeySheet();
      renderSourceVerificationSheet();
    }
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
    renderAnswerKeySheet();
    renderSourceVerificationSheet();
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
    saveDraft(false);
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
  saveDraft(false);
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
        exam_type: state.currentExam.exam_type || "yazili_sinav",
        bep_options: state.currentExam.bep_options || state.bepOptions || {}
      })
    });
    if (!res.ok) throw new Error("Yeniden üretilemedi.");
    const data = await res.json();
    if (data.question) {
      data.question.points = state.currentExam.questions[idx].points || 10;
      state.currentExam.questions[idx] = data.question;
      renderExamPages();
      saveDraft(false);
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

  const schoolName = toTurkishUpper(state.config.school_name || "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu");
  const subjectName = toTurkishUpper(exam.subject_name || "Din Kültürü ve Ahlak Bilgisi");
  const termName = toTurkishUpper(exam.term || "");
  const examNoName = toTurkishUpper(exam.exam_no || "");
  const isBep = (exam.exam_type === "bep_sinav");

  const hdr = document.createElement("div");
  hdr.className = "mb-4 pb-2 border-b-2 border-blue-900 text-center";
  hdr.innerHTML = `
    <h3 class="font-bold text-sm text-slate-900">${schoolName}</h3>
    <h4 class="font-bold text-blue-900 text-sm">${exam.grade}. SINIF ${subjectName} ${termName} ${examNoName}</h4>
    <div class="text-xs font-semibold text-emerald-800 mt-1">
      ${isBep ? "♿ BEP KAPSAMINDAKİ ÖĞRENCİ SINAVI — CEVAP ANAHTARI VE DEĞERLENDİRME RUBRİĞİ" : "CEVAP ANAHTARI VE DERECELİ PUANLAMA ANAHTARI (RUBRİK)"}
    </div>
  `;
  container.appendChild(hdr);

  if (isBep) {
    const bepRubricBanner = document.createElement("div");
    bepRubricBanner.className = "mb-4 p-3 bg-teal-50 border border-teal-300 rounded-xl text-xs text-teal-950 space-y-1";
    bepRubricBanner.innerHTML = `
      <div class="font-extrabold text-teal-900 flex items-center gap-1.5">
        <span>♿</span> MEB Özel Eğitim Hizmetleri Yönetmeliği & Ölçme Değerlendirme Yönergesi BEP Esasları:
      </div>
      <ul class="list-disc list-inside text-[11px] space-y-0.5 text-teal-900">
        <li><strong>Puanlama ve Rubrik:</strong> Yazım hataları, noktalama işaretleri veya bozuk el yazısı nedeniyle puan kırılmaz. Öğrencinin sorunun özünü kavradığını gösteren her türlü doğru ifadeye ve işaretlemeye tam puan verilir.</li>
        <li><strong>Sınav Uygulaması:</strong> Öğrenciye standart sınav süresine ek olarak %25 ila %50 ek süre tanınır; ihtiyaç halinde okuyucu/kodlayıcı öğretmen desteği sağlanır.</li>
        <li><strong>e-Okul & Resmî Evrak Kaydı:</strong> Sınav kağıdı zümre BEP dosyasında saklanır ve e-Okul sistemine öğrencinin BEP statüsü kontrol edilerek 100 üzerinden girilir.</li>
      </ul>
    `;
    container.appendChild(bepRubricBanner);
  }

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
    renderSourceVerificationSheet();
    saveDraft(false);
  }
}

// --- 3. SEKME: KİTAP İLİŞKİSİ VE PEDAGOJİK DOĞRULAMA (YENİ TALEP) ---
function renderSourceVerificationSheet() {
  const container = document.getElementById("sourceVerificationContent");
  if (!container) return;
  container.innerHTML = "";

  const exam = state.currentExam;

  const schoolName = toTurkishUpper(state.config.school_name || "Tevfik İleri İmam Hatip Ortaokulu");
  const subjectName = toTurkishUpper(exam.subject_name || "Din Kültürü ve Ahlak Bilgisi");

  const hdr = document.createElement("div");
  hdr.className = "mb-4 pb-2 border-b-2 border-amber-800 text-center";
  hdr.innerHTML = `
    <h3 class="font-bold text-sm text-slate-900">${schoolName}</h3>
    <h4 class="font-bold text-amber-900 text-sm">${exam.grade}. SINIF ${subjectName} • KİTAP İLİŞKİSİ VE PEDAGOJİK DOĞRULAMA RAPORU</h4>
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
          show_answer_lines: (state.showAnswerLines !== false),
          show_scenario_in_header: (state.showScenarioInHeader !== false),
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

// --- SINAVI KAYDETME & ARŞİV (GÖRSEL ONAY & GERİBİLDİRİM ÖZELLİĞİ) ---
async function handleSaveExam() {
  const btn = document.getElementById("btnSaveExam");
  if (!state.currentExam.questions || state.currentExam.questions.length === 0) {
    showToast("Kaydedilecek soru bulunmuyor. Önce sınav sorularını oluşturunuz.", "warning");
    return;
  }

  // Buton üzerinde canlı kaydetme animasyonu
  const origBtnText = btn ? btn.innerHTML : "💾 Kaydet";
  const origBtnClass = btn ? btn.className : "";
  if (btn) {
    btn.innerHTML = `<span>⏳</span> Kaydediliyor...`;
    btn.disabled = true;
  }

  setLoading(true, "Sınav kaydediliyor ve sorular soru bankasına arşivleniyor...");
  try {
    const res = await fetch("/api/save-exam", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...state.currentExam,
        show_answer_lines: (state.showAnswerLines !== false),
        show_scenario_in_header: (state.showScenarioInHeader !== false),
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

    // KULLANICI TALEBİ: Ekrandan kaydet deyince kaydedildiğini net gösteren özellik!
    if (btn) {
      btn.innerHTML = `<span>✅</span> Sınav Başarıyla Kaydedildi!`;
      btn.className = `px-3 py-1 text-xs font-extrabold rounded bg-emerald-600 text-white shadow-lg ring-2 ring-emerald-300 transition-all transform scale-105`;
    }

    showToast("🎉 Sınav başarıyla arşive kaydedildi! Üst menüdeki '📂 Sınav Arşivi' ekranından dilediğiniz an inceleyebilir veya yazdırabilirsiniz.", "success");
    await loadSavedExamsList();
    loadQuestionBank();

    // 3.5 saniye sonra butonu normal haline döndür
    setTimeout(() => {
      if (btn) {
        btn.innerHTML = origBtnText;
        btn.className = origBtnClass;
        btn.disabled = false;
      }
    }, 3500);

  } catch (err) {
    if (btn) {
      btn.innerHTML = origBtnText;
      btn.className = origBtnClass;
      btn.disabled = false;
    }
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

    // Sayaçları senkronize et
    const count = state.savedExams.length;
    const badge1 = document.getElementById("archiveExamCountBadge");
    if (badge1) badge1.textContent = count;
    const badge2 = document.getElementById("sidebarArchiveCountText");
    if (badge2) badge2.textContent = count;
    const badge3 = document.getElementById("archiveTotalBadge");
    if (badge3) badge3.textContent = `${count} Sınav`;

    renderExamArchiveScreen();
  } catch (e) {
    console.error("Geçmiş sınavlar alınamadı:", e);
  }
}

// ==============================================================
// KAYITLI SINAV VE ÇALIŞMA ARŞİVİ EKRANI (SINIF & DERS KATMANLARI)
// ==============================================================
function setArchiveViewMode(mode) {
  state.archiveViewMode = mode;
  const btnLayered = document.getElementById("btnArchiveViewLayered");
  const btnGrid = document.getElementById("btnArchiveViewGrid");
  if (btnLayered && btnGrid) {
    if (mode === "layered") {
      btnLayered.className = "px-2.5 py-1 text-xs font-bold rounded-md bg-white text-indigo-950 shadow-xs transition";
      btnGrid.className = "px-2.5 py-1 text-xs font-semibold rounded-md text-slate-600 hover:text-slate-900 transition";
    } else {
      btnGrid.className = "px-2.5 py-1 text-xs font-bold rounded-md bg-white text-indigo-950 shadow-xs transition";
      btnLayered.className = "px-2.5 py-1 text-xs font-semibold rounded-md text-slate-600 hover:text-slate-900 transition";
    }
  }
  renderExamArchiveScreen();
}

function renderExamArchiveScreen() {
  const container = document.getElementById("archiveExamsContainer");
  if (!container) return;
  container.innerHTML = "";

  const qSearch = (document.getElementById("archiveSearchInput")?.value || "").toLowerCase().trim();
  const fGrade = document.getElementById("archiveFilterGrade")?.value || "";
  const fSubject = document.getElementById("archiveFilterSubject")?.value || "";
  const fTerm = document.getElementById("archiveFilterTerm")?.value || "";
  const fType = document.getElementById("archiveFilterType")?.value || "";

  // Filtreleme
  let filtered = state.savedExams.filter(ex => {
    if (fGrade && String(ex.grade) !== String(fGrade)) return false;
    if (fSubject && ex.subject !== fSubject) return false;
    if (fTerm && ex.term !== fTerm) return false;
    if (fType && (ex.exam_type || "yazili_sinav") !== fType) return false;
    if (qSearch) {
      const matchText = `${ex.title || ""} ${ex.scenario || ""} ${ex.exam_no || ""} ${ex.term || ""}`.toLowerCase();
      if (!matchText.includes(qSearch)) return false;
    }
    return true;
  });

  const totalFilteredBadge = document.getElementById("archiveTotalBadge");
  if (totalFilteredBadge) {
    totalFilteredBadge.textContent = `${filtered.length} Sınav`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm max-w-lg mx-auto my-8">
        <div class="text-5xl mb-3">📂</div>
        <h4 class="text-base font-bold text-slate-800">Kayıtlı Sınav Bulunamadı</h4>
        <p class="text-xs text-slate-500 mt-1 mb-5">
          ${state.savedExams.length === 0 ? "Henüz arşive kaydedilmiş bir sınavınız yok. Sınav hazırlayıp '💾 Kaydet' butonuna basarak arşivleyebilirsiniz." : "Seçtiğiniz arama ve filtre kriterlerine uygun kayıtlı sınav bulunamadı."}
        </p>
        <button type="button" onclick="switchView('exam_maker')" 
                class="px-4 py-2 text-xs font-bold rounded-lg bg-indigo-900 hover:bg-indigo-800 text-white shadow transition inline-flex items-center gap-1.5">
          <span>➕</span> Yeni Sınav Hazırla
        </button>
      </div>
    `;
    return;
  }

  // 1. KATMANLI / KADEMELİ GÖRÜNÜM (KULLANICI TALEBİ: Sınıf & Ders Katmanları)
  if (state.archiveViewMode === "layered") {
    // Sınıf bazında grupla (5, 6, 7, 8)
    const gradeGroups = {};
    filtered.forEach(ex => {
      const g = ex.grade || 5;
      if (!gradeGroups[g]) gradeGroups[g] = [];
      gradeGroups[g].push(ex);
    });

    const sortedGrades = Object.keys(gradeGroups).sort((a, b) => parseInt(a, 10) - parseInt(b, 10));

    sortedGrades.forEach(gKey => {
      const examsInGrade = gradeGroups[gKey];
      const gradeCard = document.createElement("div");
      gradeCard.className = "bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden mb-6";

      // Sınıf Katman Başlığı (Accordion)
      const gradeHeader = document.createElement("div");
      gradeHeader.className = "bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white px-5 py-3.5 flex items-center justify-between cursor-pointer select-none";
      gradeHeader.innerHTML = `
        <div class="flex items-center gap-2.5">
          <span class="text-xl">🎓</span>
          <span class="text-sm font-extrabold tracking-wide">${gKey}. Sınıf ${gKey === "8" ? "(LGS Seviyesi)" : "Kademesi"}</span>
          <span class="bg-indigo-700/80 text-white text-[10px] font-bold px-2 py-0.5 rounded-full ml-1">
            ${examsInGrade.length} Sınav
          </span>
        </div>
        <span class="text-xs font-bold text-indigo-300">▼ Göster / Gizle</span>
      `;

      const gradeContent = document.createElement("div");
      gradeContent.className = "p-5 space-y-6";

      gradeHeader.addEventListener("click", () => {
        gradeContent.classList.toggle("hidden");
      });

      // Sınıf İçinde Ders Bazında Alt Katmanlar (DKAB, Siyer, Kur'an)
      const subjectGroups = {};
      examsInGrade.forEach(ex => {
        const s = ex.subject || "dkab";
        if (!subjectGroups[s]) subjectGroups[s] = [];
        subjectGroups[s].push(ex);
      });

      const subjectNameMap = {
        dkab: "Din Kültürü ve Ahlak Bilgisi",
        siyer: "Peygamberimizin Hayatı",
        kuran: "Kur'an-ı Kerim"
      };

      const subjectIconMap = {
        dkab: "📘",
        siyer: "📗",
        kuran: "📙"
      };

      for (const [sKey, examsInSubject] of Object.entries(subjectGroups)) {
        const subjBox = document.createElement("div");
        subjBox.className = "space-y-3";

        const sTitle = subjectNameMap[sKey] || state.curriculum[sKey]?.name || toTurkishUpper(sKey);
        const sIcon = subjectIconMap[sKey] || "📖";

        subjBox.innerHTML = `
          <div class="flex items-center justify-between border-b border-slate-200 pb-2">
            <h5 class="text-xs font-extrabold text-slate-800 flex items-center gap-2">
              <span class="text-base">${sIcon}</span>
              <span>${sTitle}</span>
              <span class="text-[10px] font-semibold text-slate-500">(${examsInSubject.length} Sınav / Çalışma)</span>
            </h5>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            ${examsInSubject.map(ex => renderExamArchiveCardHtml(ex)).join("")}
          </div>
        `;
        gradeContent.appendChild(subjBox);
      }

      gradeCard.appendChild(gradeHeader);
      gradeCard.appendChild(gradeContent);
      container.appendChild(gradeCard);
    });

  } else {
    // 2. DÜZ LİSTE / GRID GÖRÜNÜMÜ
    const gridEl = document.createElement("div");
    gridEl.className = "grid grid-cols-1 md:grid-cols-2 gap-4";
    gridEl.innerHTML = filtered.map(ex => renderExamArchiveCardHtml(ex)).join("");
    container.appendChild(gridEl);
  }
}

function renderExamArchiveCardHtml(ex) {
  const typeMap = {
    yazili_sinav: { label: "📄 Yazılı Sınav", badge: "bg-blue-100 text-blue-900 border-blue-200" },
    bep_sinav: { label: "♿ BEP Sınavı", badge: "bg-teal-100 text-teal-950 border-teal-300 font-extrabold" },
    etut_calisma: { label: "📝 Çalışma Kağıdı", badge: "bg-emerald-100 text-emerald-900 border-emerald-200" },
    yaprak_test: { label: "🎯 Yaprak Test", badge: "bg-purple-100 text-purple-900 border-purple-200" }
  };
  const typeInfo = typeMap[ex.exam_type] || typeMap.yazili_sinav;
  const dateStr = ex.updated_at ? ex.updated_at.slice(0, 10) : "";

  return `
    <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition space-y-3 flex flex-col justify-between">
      <div>
        <!-- Üst Etiketler -->
        <div class="flex items-center justify-between gap-1.5 flex-wrap mb-2">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded border ${typeInfo.badge}">
              ${typeInfo.label}
            </span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
              ${ex.grade}. Sınıf
            </span>
            <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600">
              ${ex.term || "1. Dönem"} • ${ex.exam_no || "1. Yazılı"}
            </span>
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-50 text-indigo-900 border border-indigo-100">
              ${ex.scenario || "Senaryo"}
            </span>
          </div>
          <span class="text-[10px] text-slate-400 font-mono">📅 ${dateStr}</span>
        </div>

        <!-- Başlık -->
        <h4 class="text-sm font-bold text-slate-900 hover:text-blue-900 cursor-pointer transition line-clamp-2" 
            onclick="loadExamById(${ex.id})" title="Tıklayarak Sınavı Aç ve Düzenle">
          ${ex.title}
        </h4>

        <!-- Bilgi Rozetleri -->
        <div class="flex items-center gap-3 mt-2 text-[11px] text-slate-600 font-medium">
          <span class="flex items-center gap-1 font-bold text-slate-800">
            <span>❓</span> ${ex.question_count} Soru
          </span>
          <span class="flex items-center gap-1 font-bold text-amber-800">
            <span>💯</span> ${ex.total_points || 100} Puan
          </span>
          <span class="flex items-center gap-1 text-slate-500">
            <span>📐</span> ${ex.layout === "1_column" ? "Tek Sütun" : "2 Sütun"}
          </span>
        </div>
      </div>

      <!-- Aksiyon Butonları -->
      <div class="pt-3 border-t border-slate-100 flex items-center justify-between flex-wrap gap-1.5 mt-2">
        <div class="flex items-center gap-1.5">
          <button type="button" onclick="loadExamById(${ex.id})"
                  class="px-2.5 py-1 text-xs font-bold rounded-lg bg-blue-900 hover:bg-blue-800 text-white shadow-xs transition flex items-center gap-1"
                  title="Sınavı A4 editöründe aç ve üzerinde düzenlemeler yap">
            <span>👁️</span> Aç ve Düzenle
          </button>
          <button type="button" onclick="printExamFromArchive(${ex.id})"
                  class="px-2.5 py-1 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-xs transition flex items-center gap-1"
                  title="Doğrudan A4 olarak yazdır veya PDF kaydet">
            <span>🖨️</span> Yazdır
          </button>
          <button type="button" onclick="downloadExamDocxFromArchive(${ex.id})"
                  class="px-2 py-1 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-blue-50 text-slate-700 hover:text-blue-900 border border-slate-200 transition"
                  title="Öğrenci Sınav Kağıdını Word (.docx) olarak indir">
            📄 Word
          </button>
          <button type="button" onclick="downloadAnswerDocxFromArchive(${ex.id})"
                  class="px-2 py-1 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-teal-50 text-slate-700 hover:text-teal-900 border border-slate-200 transition"
                  title="Cevap Anahtarını Word (.docx) olarak indir">
            🔑 Rubrik
          </button>
        </div>

        <button type="button" onclick="deleteSavedExam(${ex.id})"
                class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                title="Bu sınavı arşivden sil">
          🗑️
        </button>
      </div>
    </div>
  `;
}

async function loadExamById(id) {
  setLoading(true, "Sınav yükleniyor...");
  try {
    const res = await fetch(`/api/exams/${id}`);
    if (!res.ok) throw new Error("Sınav açılamadı.");
    const data = await res.json();
    const loaded = data.exam;
    if (!loaded.subject_name) {
      loaded.subject_name = state.curriculum[loaded.subject]?.name || loaded.subject || "Din Kültürü ve Ahlak Bilgisi";
    }
    state.currentExam = loaded;
    if (loaded.show_answer_lines !== undefined) {
      state.showAnswerLines = loaded.show_answer_lines;
    }
    if (loaded.show_scenario_in_header !== undefined) {
      state.showScenarioInHeader = loaded.show_scenario_in_header;
    }
    if (loaded.bep_options) {
      state.bepOptions = { ...state.bepOptions, ...loaded.bep_options };
      if (loaded.bep_options.show_bep_header !== undefined) {
        state.showBepInHeader = loaded.bep_options.show_bep_header;
      }
    }
    syncHeaderOptionsUI();

    // Sol panel form kontrollerini yüklenen sınava senkronize et
    if (document.getElementById("examTypeSelect") && loaded.exam_type) {
      document.getElementById("examTypeSelect").value = loaded.exam_type;
    }
    if (document.getElementById("examSubject") && loaded.subject) {
      document.getElementById("examSubject").value = loaded.subject;
    }
    if (document.getElementById("examGrade") && loaded.grade) {
      document.getElementById("examGrade").value = loaded.grade;
    }
    if (document.getElementById("examTerm") && loaded.term) {
      document.getElementById("examTerm").value = loaded.term;
    }
    if (document.getElementById("examNo") && loaded.exam_no) {
      document.getElementById("examNo").value = loaded.exam_no;
    }
    if (loaded.exam_type === "bep_sinav") {
      onExamTypeChange();
    } else if (document.getElementById("examScenario") && loaded.scenario) {
      populateScenarioDropdown();
      document.getElementById("examScenario").value = loaded.scenario;
    }
    if (document.getElementById("examQuestionCount") && loaded.questions) {
      document.getElementById("examQuestionCount").value = loaded.questions.length;
    }

    recalculateTotalPoints();
    renderExamPages();
    saveDraft(false);

    // Otomatik Sınav Hazırlama Ekranına Geç
    switchView("exam_maker");
    showToast(`"${loaded.title}" başarıyla yüklendi. Düzenleyebilirsiniz.`, "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function printExamFromArchive(id) {
  await loadExamById(id);
  setTimeout(() => {
    handlePrintPDF();
  }, 400);
}

async function downloadExamDocxFromArchive(id) {
  setLoading(true, "Word belgesi oluşturuluyor...");
  try {
    const resExam = await fetch(`/api/exams/${id}`);
    const data = await resExam.json();
    const ex = data.exam;

    const res = await fetch("/api/export/docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        exam_data: ex,
        type: "exam",
        layout: ex.layout || "2_column"
      })
    });
    if (!res.ok) throw new Error("Word indirilemedi.");
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${ex.title.replace(/\s+/g, "_")}_Ogrenci.docx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("Word sınav kağıdı indirildi.", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function downloadAnswerDocxFromArchive(id) {
  setLoading(true, "Cevap anahtarı Word belgesi oluşturuluyor...");
  try {
    const resExam = await fetch(`/api/exams/${id}`);
    const data = await resExam.json();
    const ex = data.exam;

    const res = await fetch("/api/export/docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        exam_data: ex,
        type: "answer_key",
        layout: ex.layout || "2_column"
      })
    });
    if (!res.ok) throw new Error("Cevap anahtarı indirilemedi.");
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${ex.title.replace(/\s+/g, "_")}_Cevap_Anahtari.docx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("Cevap anahtarı Word belgesi indirildi.", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function deleteSavedExam(id) {
  if (confirm("Bu kayıtlı sınavı arşivden silmek istediğinize emin misiniz?")) {
    try {
      await fetch(`/api/exams/${id}`, { method: "DELETE" });
      await loadSavedExamsList();
      showToast("Sınav arşivden silindi.", "info");
    } catch (e) {
      showToast("Silinemedi.", "error");
    }
  }
}

// ==============================================================
// SORU BANKASI VE HAVUZ YÖNETİMİ (ÖZET KARTLAR, CEVAP DROPDOWN & AKILLI GÜNCELLEME)
// ==============================================================
state.questionBankStats = null;
state.isBankStatsOpen = true;
state.allBankAnswersOpen = false;
state.editingBankItem = null;

async function loadQuestionBank() {
  const subj = document.getElementById("bankFilterSubject")?.value || "";
  const grade = document.getElementById("bankFilterGrade")?.value || "";
  const diff = document.getElementById("bankFilterDifficulty")?.value || "";
  const origin = document.getElementById("bankFilterOrigin")?.value || "";
  const usage = document.getElementById("bankFilterUsage")?.value || "";
  const search = document.getElementById("bankSearchInput")?.value || "";

  let url = `/api/question-bank?`;
  if (subj) url += `subject=${subj}&`;
  if (grade) url += `grade=${grade}&`;
  if (diff) url += `difficulty=${diff}&`;
  if (origin) url += `origin_type=${origin}&`;
  if (usage) url += `usage_filter=${usage}&`;
  if (search) url += `search=${encodeURIComponent(search)}&`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    state.questionBankItems = data.items || [];
    if (data.stats) {
      state.questionBankStats = data.stats;
    }
    renderBankStatsDashboard();
    renderQuestionBankUI();
  } catch (e) {
    console.error("Soru bankası yüklenemedi:", e);
  }
}

function toggleBankStatsDashboard() {
  state.isBankStatsOpen = !state.isBankStatsOpen;
  const wrapper = document.getElementById("bankStatsDashboardWrapper");
  const chevron = document.getElementById("bankStatsToggleChevron");
  if (!wrapper) return;

  if (state.isBankStatsOpen) {
    wrapper.classList.remove("hidden");
    if (chevron) chevron.textContent = "▲ Gizle";
  } else {
    wrapper.classList.add("hidden");
    if (chevron) chevron.textContent = "▼ Göster";
  }
}

function quickFilterBank(filterType, value) {
  if (filterType === "reset") {
    resetBankFilters();
    return;
  }
  const map = {
    subject: "bankFilterSubject",
    grade: "bankFilterGrade",
    difficulty: "bankFilterDifficulty",
    origin: "bankFilterOrigin",
    usage: "bankFilterUsage"
  };
  const elId = map[filterType];
  if (elId && document.getElementById(elId)) {
    const el = document.getElementById(elId);
    el.value = el.value === String(value) ? "" : String(value);
    loadQuestionBank();
  }
}

function resetBankFilters() {
  ["bankFilterSubject", "bankFilterGrade", "bankFilterDifficulty", "bankFilterOrigin", "bankFilterUsage", "bankSearchInput"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });
  loadQuestionBank();
}

function renderBankStatsDashboard() {
  const grid = document.getElementById("bankStatsCardsGrid");
  if (!grid) return;

  const s = state.questionBankStats || {
    total: state.questionBankItems.length,
    by_subject: { dkab: 0, kuran: 0, siyer: 0 },
    by_grade: { "5": 0, "6": 0, "7": 0, "8": 0 },
    by_difficulty: { Kolay: 0, Orta: 0, Zor: 0 },
    by_origin: { ai: 0, teacher_edited: 0 },
    by_usage: { used: 0, unused: 0, total_exam_usages: 0 },
    by_type: { acik_uclu: 0, coktan_secmeli: 0 }
  };

  const activeSubj = document.getElementById("bankFilterSubject")?.value || "";
  const activeGrade = document.getElementById("bankFilterGrade")?.value || "";
  const activeDiff = document.getElementById("bankFilterDifficulty")?.value || "";
  const activeOrigin = document.getElementById("bankFilterOrigin")?.value || "";
  const activeUsage = document.getElementById("bankFilterUsage")?.value || "";

  grid.innerHTML = `
    <!-- KART 1: TOPLAM SORU HAVUZU -->
    <div onclick="quickFilterBank('reset', '')" 
         class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition cursor-pointer border border-slate-200/80 border-t-4 border-t-blue-600 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">TOPLAM SORU HAVUZU</span>
        <div class="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-base shadow-inner">📚</div>
      </div>
      <div class="my-2">
        <div class="text-3xl font-black text-slate-900 tracking-tight">${s.total}</div>
      </div>
      <div class="text-[11px] text-slate-500 flex items-center justify-between">
        <span>Açık Uçlu: <strong class="text-slate-700">${s.by_type.acik_uclu || 0}</strong></span>
        <span>•</span>
        <span>Test: <strong class="text-slate-700">${s.by_type.coktan_secmeli || 0}</strong></span>
      </div>
    </div>

    <!-- KART 2: DİN KÜLTÜRÜ VE AHLAK BİLGİSİ -->
    <div onclick="quickFilterBank('subject', 'dkab')" 
         class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition cursor-pointer border ${activeSubj === 'dkab' ? 'ring-2 ring-emerald-500 bg-emerald-50/20' : 'border-slate-200/80'} border-t-4 border-t-emerald-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">DİN KÜLTÜRÜ (DKAB)</span>
        <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-base shadow-inner">🕌</div>
      </div>
      <div class="my-2">
        <div class="text-3xl font-black text-slate-900 tracking-tight">${s.by_subject.dkab || 0}</div>
      </div>
      <div class="text-[11px] text-slate-500">
        Kayıtlı DKAB kazanım ve analiz soruları
      </div>
    </div>

    <!-- KART 3: KUR'AN-I KERİM -->
    <div onclick="quickFilterBank('subject', 'kuran')" 
         class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition cursor-pointer border ${activeSubj === 'kuran' ? 'ring-2 ring-amber-500 bg-amber-50/20' : 'border-slate-200/80'} border-t-4 border-t-amber-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">KUR'AN-I KERİM</span>
        <div class="w-9 h-9 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-base shadow-inner">📖</div>
      </div>
      <div class="my-2">
        <div class="text-3xl font-black text-slate-900 tracking-tight">${s.by_subject.kuran || 0}</div>
      </div>
      <div class="text-[11px] text-slate-500">
        Tecvid, mahreç ve sure analiz soruları
      </div>
    </div>

    <!-- KART 4: PEYGAMBERİMİZİN HAYATI -->
    <div onclick="quickFilterBank('subject', 'siyer')" 
         class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition cursor-pointer border ${activeSubj === 'siyer' ? 'ring-2 ring-purple-500 bg-purple-50/20' : 'border-slate-200/80'} border-t-4 border-t-purple-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">PEYGAMBERİMİZİN HAYATI</span>
        <div class="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center text-base shadow-inner">🕋</div>
      </div>
      <div class="my-2">
        <div class="text-3xl font-black text-slate-900 tracking-tight">${s.by_subject.siyer || 0}</div>
      </div>
      <div class="text-[11px] text-slate-500">
        Siyer ve Nebevî örneklik soruları
      </div>
    </div>

    <!-- KART 5: SINIF DÜZEYİ DAĞILIMI (5, 6, 7, 8) -->
    <div class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition border border-slate-200/80 border-t-4 border-t-teal-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">SINIF BAZINDA SORULAR</span>
        <div class="w-9 h-9 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center text-base shadow-inner">🎓</div>
      </div>
      <div class="grid grid-cols-4 gap-1.5 my-2">
        ${["5", "6", "7", "8"].map(g => `
          <button type="button" onclick="quickFilterBank('grade', '${g}')"
                  class="py-1.5 px-1 rounded-lg border text-center transition ${activeGrade === g ? 'bg-teal-600 text-white border-teal-700 font-bold shadow' : 'bg-slate-50 hover:bg-teal-50 text-slate-700 border-slate-200'}">
            <div class="text-[10px] opacity-80">${g}. Sınıf</div>
            <div class="text-sm font-black">${s.by_grade[g] || 0}</div>
          </button>
        `).join("")}
      </div>
      <div class="text-[11px] text-slate-500">
        Sınıf kutucuğuna tıklayarak filtreleyin
      </div>
    </div>

    <!-- KART 6: ZORLUK SEVİYESİ ANALİZİ -->
    <div class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition border border-slate-200/80 border-t-4 border-t-rose-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">GÜÇLÜK DERECESİ</span>
        <div class="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center text-base shadow-inner">🎯</div>
      </div>
      <div class="grid grid-cols-3 gap-1.5 my-2">
        <button type="button" onclick="quickFilterBank('difficulty', 'Kolay')"
                class="py-1.5 px-1.5 rounded-lg border text-center transition ${activeDiff === 'Kolay' ? 'bg-emerald-600 text-white border-emerald-700 font-bold shadow' : 'bg-emerald-50/60 hover:bg-emerald-100 text-emerald-900 border-emerald-200'}">
          <div class="text-[10px]">Kolay</div>
          <div class="text-sm font-black">${s.by_difficulty.Kolay || 0}</div>
        </button>
        <button type="button" onclick="quickFilterBank('difficulty', 'Orta')"
                class="py-1.5 px-1.5 rounded-lg border text-center transition ${activeDiff === 'Orta' ? 'bg-amber-500 text-white border-amber-600 font-bold shadow' : 'bg-amber-50/60 hover:bg-amber-100 text-amber-900 border-amber-200'}">
          <div class="text-[10px]">Orta</div>
          <div class="text-sm font-black">${s.by_difficulty.Orta || 0}</div>
        </button>
        <button type="button" onclick="quickFilterBank('difficulty', 'Zor')"
                class="py-1.5 px-1.5 rounded-lg border text-center transition ${activeDiff === 'Zor' ? 'bg-rose-600 text-white border-rose-700 font-bold shadow' : 'bg-rose-50/60 hover:bg-rose-100 text-rose-900 border-rose-200'}">
          <div class="text-[10px]">Zor</div>
          <div class="text-sm font-black">${s.by_difficulty.Zor || 0}</div>
        </button>
      </div>
      <div class="text-[11px] text-slate-500">
        MEB bilişsel güçlük dağılımı
      </div>
    </div>

    <!-- KART 7: ÜRETİM KAYNAĞI (YAPAY ZEKA vs ÖĞRETMEN MÜDAHALESİ) -->
    <div class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition border border-slate-200/80 border-t-4 border-t-indigo-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">ÜRETİM & MÜDAHALE</span>
        <div class="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-base shadow-inner">✍️</div>
      </div>
      <div class="grid grid-cols-2 gap-2 my-2">
        <button type="button" onclick="quickFilterBank('origin', 'ai')"
                class="py-1.5 px-2 rounded-lg border text-left transition ${activeOrigin === 'ai' ? 'bg-indigo-600 text-white border-indigo-700 font-bold shadow' : 'bg-indigo-50/60 hover:bg-indigo-100 text-indigo-950 border-indigo-200'}">
          <div class="text-[10px] flex items-center gap-1">🤖 Yapay Zeka</div>
          <div class="text-base font-black">${s.by_origin.ai || 0}</div>
        </button>
        <button type="button" onclick="quickFilterBank('origin', 'teacher_edited')"
                class="py-1.5 px-2 rounded-lg border text-left transition ${activeOrigin === 'teacher_edited' ? 'bg-amber-600 text-white border-amber-700 font-bold shadow' : 'bg-amber-50/70 hover:bg-amber-100 text-amber-950 border-amber-300'}">
          <div class="text-[10px] flex items-center gap-1">✍️ Öğretmen</div>
          <div class="text-base font-black">${s.by_origin.teacher_edited || 0}</div>
        </button>
      </div>
      <div class="text-[11px] text-slate-500">
        YZ çıktısı ve öğretmen düzenlemeleri
      </div>
    </div>

    <!-- KART 8: SINAV KULLANIM DURUMU -->
    <div class="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition border border-slate-200/80 border-t-4 border-t-cyan-500 flex flex-col justify-between">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-extrabold tracking-wider text-slate-400 uppercase">SINAV KULLANIMI</span>
        <div class="w-9 h-9 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center text-base shadow-inner">📌</div>
      </div>
      <div class="grid grid-cols-2 gap-2 my-2">
        <button type="button" onclick="quickFilterBank('usage', 'used')"
                class="py-1.5 px-2 rounded-lg border text-left transition ${activeUsage === 'used' ? 'bg-cyan-700 text-white border-cyan-800 font-bold shadow' : 'bg-cyan-50/60 hover:bg-cyan-100 text-cyan-950 border-cyan-200'}">
          <div class="text-[10px]">📌 Kullanılan</div>
          <div class="text-base font-black">${s.by_usage.used || 0}</div>
        </button>
        <button type="button" onclick="quickFilterBank('usage', 'unused')"
                class="py-1.5 px-2 rounded-lg border text-left transition ${activeUsage === 'unused' ? 'bg-slate-700 text-white border-slate-800 font-bold shadow' : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'}">
          <div class="text-[10px]">⏳ Bekleyen</div>
          <div class="text-base font-black">${s.by_usage.unused || 0}</div>
        </button>
      </div>
      <div class="text-[11px] text-slate-500">
        Toplam <strong class="text-slate-700">${s.by_usage.total_exam_usages || 0}</strong> kez sınavlarda yer aldı
      </div>
    </div>
  `;
}

function renderQuestionBankUI() {
  const container = document.getElementById("bankCardsGrid");
  const countBadge = document.getElementById("bankTotalCountBadge");
  if (!container) return;
  container.innerHTML = "";

  if (countBadge) {
    countBadge.textContent = `${state.questionBankItems.length} Soru Gösteriliyor`;
  }

  if (state.questionBankItems.length === 0) {
    container.innerHTML = `
      <div class="col-span-2 text-center py-12 bg-white rounded-2xl border border-slate-200 text-slate-400">
        <div class="text-4xl mb-2">📭</div>
        <div class="font-bold text-sm text-slate-700">Bu Filtreye Uygun Soru Bulunamadı</div>
        <div class="text-xs text-slate-400 mt-1">Filtreleri sıfırlayabilir veya "Kitaptan Soru Üret & Biriktir" butonuna basarak yeni sorular ekleyebilirsiniz.</div>
      </div>
    `;
    return;
  }

  state.questionBankItems.forEach(item => {
    const card = document.createElement("div");
    card.className = "bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between text-xs space-y-3";

    // 1) Kullanım Rozeti
    const usageCount = item.usage_count || 0;
    const usageBadgeHtml = usageCount > 0 
      ? `<button onclick="openUsageModal(${item.id})" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 hover:bg-emerald-200 cursor-pointer flex items-center gap-1" title="Hangi sınavlarda kullanıldığını gör">
           <span>📌</span> ${usageCount} Sınavda Kullanıldı (Gör)
         </button>`
      : `<span class="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
           ⏳ Henüz Kullanılmadı
         </span>`;

    // 2) Kaynak / Kişi Müdahalesi Rozeti (Sadece Soru Bankasında Gösterilir - Kullanıcı Talebi)
    const isTeacherEdited = item.origin_type === "teacher_edited";
    const originBadgeHtml = isTeacherEdited
      ? `<span class="badge-tag bg-amber-100 text-amber-900 border border-amber-300 font-bold flex items-center gap-1 shadow-sm" title="Öğretmen tarafından düzenlenmiş / müdahale edilmiş soru">
           <span>✍️</span> Öğretmen Müdahalesi
         </span>`
      : `<span class="badge-tag bg-indigo-50 text-indigo-800 border border-indigo-200 font-semibold flex items-center gap-1" title="Yapay zeka / sistem tarafından üretilen soru">
           <span>🤖</span> Yapay Zeka Çıktısı
         </span>`;

    const arabicHtml = item.arabic_text ? `<div class="arabic-text text-sm my-1.5">${item.arabic_text}</div>` : "";

    // Çoktan seçmeli şıklar varsa
    let optionsHtml = "";
    if (item.options && Array.isArray(item.options) && item.options.length > 0) {
      optionsHtml = `
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mt-2">
          ${item.options.map(opt => `<div class="p-1.5 bg-slate-50 border border-slate-200 rounded text-[11px] text-slate-700">${opt}</div>`).join("")}
        </div>
      `;
    }

    // Rubrik varsa
    let rubricHtml = "";
    if (item.rubric && Array.isArray(item.rubric) && item.rubric.length > 0) {
      rubricHtml = `
        <div class="mt-2 pt-2 border-t border-emerald-200/70">
          <div class="font-bold text-[10px] text-emerald-900 uppercase mb-1">📊 Dereceli Puanlama Kriterleri (Rubrik):</div>
          <div class="space-y-1">
            ${item.rubric.map(r => `
              <div class="flex items-center justify-between text-[11px] bg-white/80 px-2 py-1 rounded border border-emerald-100">
                <span class="text-slate-700">• ${r.criterion || r}</span>
                <span class="font-bold text-emerald-800 ml-2">${r.points ? r.points + " Puan" : ""}</span>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    const isOpen = state.allBankAnswersOpen;

    card.innerHTML = `
      <div>
        <!-- Üst Etiket ve Rozet Barı -->
        <div class="flex items-center justify-between border-b border-slate-100 pb-2 mb-2.5 flex-wrap gap-1.5">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="badge-tag bg-blue-100 text-blue-900 font-bold">${item.grade}. Sınıf ${toTurkishUpper(item.subject || "")}</span>
            <span class="badge-tag bg-slate-100 text-slate-700">${item.cognitive_level || "Analiz"}</span>
            <span class="badge-tag ${item.difficulty === "Zor" ? "bg-red-100 text-red-700" : item.difficulty === "Kolay" ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"}">${item.difficulty || "Orta"}</span>
            ${originBadgeHtml}
          </div>
          ${usageBadgeHtml}
        </div>

        <!-- Soru Metni -->
        <div class="font-semibold text-slate-900 text-xs leading-relaxed mb-2">
          ${item.question_text}
        </div>
        ${arabicHtml}
        ${optionsHtml}

        <!-- Kazanım ve Kitap Bilgisi -->
        <div class="text-[11px] text-slate-600 italic mt-2 mb-1.5">
          🎯 <strong>Kazanım:</strong> ${item.learning_outcome || "Genel"}
        </div>
        <div class="text-[11px] text-indigo-950 bg-indigo-50/70 px-2.5 py-1.5 rounded-lg border border-indigo-100 flex items-center justify-between flex-wrap gap-1">
          <span>📖 <strong>Kaynak:</strong> ${item.source_book || "MEB Ders Kitabı"}</span>
          <span class="font-bold text-indigo-700">${item.source_page || "İlgili Ünite"}</span>
        </div>

        <!-- AÇ / KAPA CEVAP ANAHTARI VE KİTAP BAĞLAMI DROPDOWN (KULLANICI TALEBİ) -->
        <div class="mt-2.5">
          <button type="button" onclick="toggleBankAnswerDropdown(${item.id})"
                  class="w-full py-2 px-3 bg-emerald-50/80 hover:bg-emerald-100/80 border border-emerald-200 rounded-lg text-xs font-bold text-emerald-900 flex items-center justify-between transition">
            <span class="flex items-center gap-1.5">
              <span>🔑</span> Cevap Anahtarı, Rubrik ve Kitap Bağlamı
            </span>
            <span id="bankAnsChevron_${item.id}" class="text-[10px] bg-white px-2 py-0.5 rounded border border-emerald-200 text-emerald-800">
              ${isOpen ? "▲ Gizle" : "▼ Cevabı Gör"}
            </span>
          </button>

          <div id="bankAnsPanel_${item.id}" class="${isOpen ? "" : "hidden"} mt-1.5 p-3 bg-emerald-50/40 border border-emerald-200 rounded-xl space-y-2 text-xs">
            <div>
              <div class="font-bold text-emerald-900 text-[11px] mb-0.5">✅ Beklenen Örnek Cevap / Çözüm:</div>
              <div class="text-slate-800 leading-relaxed bg-white p-2 rounded border border-emerald-100">
                ${item.answer_text || "Cevap metni tanımlanmamış."}
              </div>
            </div>
            ${rubricHtml}
            <div class="pt-1.5 border-t border-emerald-200/60">
              <div class="font-bold text-amber-900 text-[11px] mb-0.5">📚 Kitaptaki Pedagojik Bağlam ve Sayfa Özeti:</div>
              <div class="text-slate-700 text-[11px] leading-relaxed bg-amber-50/60 p-2 rounded border border-amber-200/70">
                ${item.source_context || "MEB ders kitabı ilgili ünite ve sayfa kazanımları esas alınmıştır."}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alt Aksiyon Butonları -->
      <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 mt-2 gap-2 flex-wrap">
        <div class="flex items-center gap-1.5">
          <button onclick="addBankQuestionToExam(${item.id})" class="px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white font-bold text-xs rounded-lg shadow-sm flex items-center gap-1 transition">
            <span>➕</span> Sınava Ekle
          </button>
          <button onclick="openEditBankQuestionModal(${item.id})" class="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs rounded-lg shadow-sm flex items-center gap-1 transition" title="Soruyu, cevabı, kazanımı ve kitap sayfasını düzenle">
            <span>✏️</span> Düzenle
          </button>
        </div>
        <button onclick="deleteBankQuestion(${item.id})" class="text-red-500 hover:text-red-700 hover:bg-red-50 font-semibold text-xs px-2 py-1 rounded transition" title="Havuzdan Sil">
          🗑️ Sil
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function toggleBankAnswerDropdown(bankId) {
  const panel = document.getElementById(`bankAnsPanel_${bankId}`);
  const chevron = document.getElementById(`bankAnsChevron_${bankId}`);
  if (!panel) return;

  const isHidden = panel.classList.contains("hidden");
  if (isHidden) {
    panel.classList.remove("hidden");
    if (chevron) chevron.textContent = "▲ Gizle";
  } else {
    panel.classList.add("hidden");
    if (chevron) chevron.textContent = "▼ Cevabı Gör";
  }
}

function toggleAllBankAnswers() {
  state.allBankAnswersOpen = !state.allBankAnswersOpen;
  const btnText = document.getElementById("btnToggleAllAnswersText");
  if (btnText) {
    btnText.textContent = state.allBankAnswersOpen ? "Tüm Cevapları Kapat" : "Tüm Cevapları Aç";
  }
  renderQuestionBankUI();
}

// ==============================================================
// SORU BANKASI DÜZENLEME & AKILLI KAYIT KARAR SİSTEMİ
// (Yeni Soru vs. Üzerine Kayıt + Sınavdaki Soruyu Güncelleme Sorusu)
// ==============================================================
function openEditBankQuestionModal(bankId) {
  const item = state.questionBankItems.find(q => q.id === bankId);
  if (!item) return;

  state.editingBankItem = item;

  document.getElementById("editBankQId").value = item.id;
  document.getElementById("editBankSubject").value = item.subject || "dkab";
  document.getElementById("editBankGrade").value = String(item.grade || 5);
  document.getElementById("editBankDifficulty").value = item.difficulty || "Orta";
  document.getElementById("editBankCognitive").value = item.cognitive_level || "Analiz";
  document.getElementById("editBankQuestionText").value = item.question_text || "";
  document.getElementById("editBankArabicText").value = item.arabic_text || "";
  document.getElementById("editBankAnswerText").value = item.answer_text || "";
  document.getElementById("editBankOutcome").value = item.learning_outcome || "";
  document.getElementById("editBankSourceBook").value = item.source_book || `${item.grade || 5}. Sınıf MEB Ders Kitabı`;
  document.getElementById("editBankSourcePage").value = item.source_page || "";
  document.getElementById("editBankSourceContext").value = item.source_context || "";

  // Karar kutusunu başlangıçta gizle, "Değişiklikleri Kaydet..." butonunu göster
  document.getElementById("editBankSaveDecisionPanel").classList.add("hidden");
  document.getElementById("btnPromptBankSaveDecision").classList.remove("hidden");

  document.getElementById("editBankQuestionModal").classList.remove("hidden");
}

function closeEditBankQuestionModal() {
  document.getElementById("editBankQuestionModal").classList.add("hidden");
  state.editingBankItem = null;
}

function showBankSaveDecisionOptions() {
  const item = state.editingBankItem;
  if (!item) return;

  const qText = document.getElementById("editBankQuestionText").value.trim();
  if (!qText) {
    showToast("Soru metni boş bırakılamaz.", "error");
    return;
  }

  const panel = document.getElementById("editBankSaveDecisionPanel");
  const warningBox = document.getElementById("editBankUsageWarningBox");
  const buttonsBox = document.getElementById("editBankDecisionButtons");

  const usageCount = item.usage_count || 0;
  const usedExams = item.used_in_exams_list || [];

  if (usageCount > 0) {
    warningBox.className = "p-3 rounded-lg bg-amber-500/20 border border-amber-400/50 text-amber-100 text-xs space-y-1";
    warningBox.innerHTML = `
      <div class="font-bold text-amber-300 flex items-center gap-1.5">
        <span>⚠️</span> Bu Soru Daha Önce ${usageCount} Sınavda Kullanılmış!
      </div>
      <div class="text-[11px] text-amber-100/90">
        <strong>Kullanıldığı Sınavlar:</strong> ${usedExams.join(" • ")}
      </div>
      <div class="text-[11px] text-white font-medium pt-1">
        Eski sorunun üzerine kaydetmek isterseniz, bu sınav(lar)daki sorunun da yeni haliyle değiştirilip değiştirilmeyeceğini aşağıdan seçebilirsiniz:
      </div>
    `;

    buttonsBox.innerHTML = `
      <button type="button" onclick="submitEditBankQuestion('save_as_new')"
              class="w-full py-2.5 px-3.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow flex items-center justify-between transition text-left">
        <span>🆕 Yeni Soru Olarak Kaydet <span class="font-normal opacity-90">(Eski soru ve sınavlar korunur, yeni soru '✍️ Öğretmen Müdahalesi' olarak eklenir)</span></span>
        <span>→</span>
      </button>

      <button type="button" onclick="submitEditBankQuestion('overwrite_and_sync_exams')"
              class="w-full py-2.5 px-3.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow flex items-center justify-between transition text-left">
        <span>🔄 Eskisinin Üzerine Kaydet VE Kullanıldığı Sınav(lar)daki Soruyu da Güncelle <span class="font-normal">(${usageCount} sınav güncellenir)</span></span>
        <span>→</span>
      </button>

      <button type="button" onclick="submitEditBankQuestion('overwrite_bank_only')"
              class="w-full py-2.5 px-3.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white font-semibold text-xs shadow flex items-center justify-between transition text-left">
        <span>🔒 Eskisinin Üzerine Kaydet AMA Sadece Soru Bankasında Güncelle <span class="font-normal opacity-85">(Kayıtlı sınavlardaki soru değişmez)</span></span>
        <span>→</span>
      </button>
    `;
  } else {
    warningBox.className = "p-2.5 rounded-lg bg-blue-500/20 border border-blue-400/40 text-blue-100 text-xs";
    warningBox.innerHTML = `
      <div class="flex items-center gap-1.5 font-semibold text-blue-200">
        <span>ℹ️</span> Durum Bilgisi: Bu soru henüz hiçbir kayıtlı sınavda kullanılmamıştır.
      </div>
    `;

    buttonsBox.innerHTML = `
      <button type="button" onclick="submitEditBankQuestion('save_as_new')"
              class="w-full py-2.5 px-3.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow flex items-center justify-between transition text-left">
        <span>🆕 Yeni Soru Olarak Kaydet <span class="font-normal opacity-90">(Orijinal soru korunur, yeni soru '✍️ Öğretmen Müdahalesi' simgesiyle eklenir)</span></span>
        <span>→</span>
      </button>

      <button type="button" onclick="submitEditBankQuestion('overwrite_bank_only')"
              class="w-full py-2.5 px-3.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow flex items-center justify-between transition text-left">
        <span>💾 Mevcut Sorunun Üzerine Kaydet <span class="font-normal">(Soru güncellenir ve '✍️ Öğretmen Müdahalesi' simgesi eklenir)</span></span>
        <span>→</span>
      </button>
    `;
  }

  panel.classList.remove("hidden");
  panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function submitEditBankQuestion(saveMode) {
  const item = state.editingBankItem;
  if (!item) return;

  const qid = item.id;
  const oldQuestionText = (item.question_text || "").trim();

  const updatedData = {
    subject: document.getElementById("editBankSubject").value,
    grade: parseInt(document.getElementById("editBankGrade").value, 10) || 5,
    difficulty: document.getElementById("editBankDifficulty").value,
    cognitive_level: document.getElementById("editBankCognitive").value,
    question_text: document.getElementById("editBankQuestionText").value.trim(),
    arabic_text: document.getElementById("editBankArabicText").value.trim(),
    answer_text: document.getElementById("editBankAnswerText").value.trim(),
    learning_outcome: document.getElementById("editBankOutcome").value.trim(),
    source_book: document.getElementById("editBankSourceBook").value.trim(),
    source_page: document.getElementById("editBankSourcePage").value.trim(),
    source_context: document.getElementById("editBankSourceContext").value.trim()
  };

  setLoading(true, "Soru bankası güncelleniyor...");
  try {
    const res = await fetch(`/api/question-bank/${qid}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        save_mode: saveMode,
        question_data: updatedData
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Güncelleme kaydedilemedi.");
    }

    const result = await res.json();

    // Eğer ekranda açık olan aktif sınavda da bu soru varsa ve sınavlarla senkronizasyon seçildiyse canlı sınavı da güncelle
    if (saveMode === "overwrite_and_sync_exams" && state.currentExam && Array.isArray(state.currentExam.questions)) {
      let activeUpdated = false;
      state.currentExam.questions.forEach(q => {
        if (q.question_bank_id === qid || (q.question_text && q.question_text.trim() === oldQuestionText)) {
          q.question_text = updatedData.question_text;
          q.arabic_text = updatedData.arabic_text;
          q.answer_text = updatedData.answer_text;
          q.learning_outcome = updatedData.learning_outcome;
          q.source_book = updatedData.source_book;
          q.source_page = updatedData.source_page;
          q.source_context = updatedData.source_context;
          q.difficulty = updatedData.difficulty;
          q.cognitive_level = updatedData.cognitive_level;
          activeUpdated = true;
        }
      });
      if (activeUpdated) {
        renderExamPages();
        saveDraft(false);
      }
    }

    closeEditBankQuestionModal();
    await loadQuestionBank();
    await loadSavedExamsList();

    if (saveMode === "save_as_new") {
      showToast("Yeni soru '✍️ Öğretmen Müdahalesi' etiketiyle soru bankasına eklendi!", "success");
    } else if (saveMode === "overwrite_and_sync_exams") {
      showToast(`Soru hem soru bankasında hem de kullanıldığı ${result.updated_exams_count || 1} sınavda güncellendi!`, "success");
    } else {
      showToast("Soru bankasındaki kayıt başarıyla güncellendi!", "success");
    }
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
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

// Görünüm Değiştirici (Sınav Hazırlama, Sınav Arşivi, Soru Bankası)
function switchView(view) {
  state.currentView = view;
  const examView = document.getElementById("viewExamMaker");
  const archiveView = document.getElementById("viewExamArchive");
  const bankView = document.getElementById("viewQuestionBank");

  const btnExam = document.getElementById("navExamMakerBtn");
  const btnArchive = document.getElementById("navExamArchiveBtn");
  const btnBank = document.getElementById("navQuestionBankBtn");

  const activeClass = "px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white transition flex items-center gap-1.5 shadow-sm";
  const inactiveClass = "px-3 py-1 text-xs font-bold rounded text-blue-200 hover:text-white transition flex items-center gap-1.5";

  // Tüm görünümleri gizle
  if (examView) examView.classList.add("hidden");
  if (archiveView) archiveView.classList.add("hidden");
  if (bankView) bankView.classList.add("hidden");

  // Navigasyon butonlarını pasif yap
  if (btnExam) btnExam.className = inactiveClass;
  if (btnArchive) btnArchive.className = inactiveClass;
  if (btnBank) btnBank.className = inactiveClass;

  if (view === "exam_maker") {
    if (examView) examView.classList.remove("hidden");
    if (btnExam) btnExam.className = activeClass;
  } else if (view === "exam_archive") {
    if (archiveView) archiveView.classList.remove("hidden");
    if (btnArchive) btnArchive.className = activeClass;
    loadSavedExamsList();
  } else if (view === "question_bank") {
    if (bankView) bankView.classList.remove("hidden");
    if (btnBank) btnBank.className = activeClass;
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

// ==============================================================
// MEB SENARYO ŞABLONLARI VE KAZANIM-SORU DAĞILIM YÖNETİM MASASI
// Kocaeli / Darıca İHO varsayılan senaryolarını görüntüler, konularla
// ilişkilendirir, soru adetlerini ve kazanımları yönetir.
// ==============================================================
state.scenarioManager = {
  subject: "dkab",
  grade: 5,
  term: "1. Dönem",
  scenarios: [],
  units: []
};

async function openScenarioManager() {
  const subj = document.getElementById("examSubject")?.value || "dkab";
  const grade = parseInt(document.getElementById("examGrade")?.value || "5", 10);
  const term = document.getElementById("examTerm")?.value || "1. Dönem";

  const sSel = document.getElementById("scenMgrSubject");
  const gSel = document.getElementById("scenMgrGrade");
  const tSel = document.getElementById("scenMgrTerm");
  if (sSel) sSel.value = subj;
  if (gSel) gSel.value = String(grade);
  if (tSel) tSel.value = term;

  await loadScenarioManagerContext(subj, grade, term);
  document.getElementById("scenarioManagerModal")?.classList.remove("hidden");
}

function closeScenarioModal() {
  document.getElementById("scenarioManagerModal")?.classList.add("hidden");
}

async function onScenarioManagerFilterChange() {
  const subj = document.getElementById("scenMgrSubject")?.value || "dkab";
  const grade = parseInt(document.getElementById("scenMgrGrade")?.value || "5", 10);
  const term = document.getElementById("scenMgrTerm")?.value || "1. Dönem";
  await loadScenarioManagerContext(subj, grade, term);
}

async function loadScenarioManagerContext(subject, grade, term) {
  try {
    const res = await fetch(`/api/scenarios?subject=${encodeURIComponent(subject)}&grade=${grade}&term=${encodeURIComponent(term)}`);
    const data = await res.json();
    state.scenarioManager = {
      subject,
      grade: parseInt(grade, 10),
      term,
      scenarios: JSON.parse(JSON.stringify(data.scenarios || [])),
      units: data.units || []
    };
    renderScenarioManagerUI();
  } catch (e) {
    showToast("Senaryo verileri yüklenemedi.", "error");
  }
}

function renderScenarioManagerUI() {
  const listEl = document.getElementById("scenarioManagerList");
  if (!listEl) return;
  listEl.innerHTML = "";

  const { subject, grade, term, scenarios, units } = state.scenarioManager;
  const prefixMap = { dkab: "DKAB", siyer: "SIYER", kuran: "KURAN" };
  const coursePrefix = prefixMap[subject] || "DKAB";

  if (!scenarios || scenarios.length === 0) {
    listEl.innerHTML = `
      <div class="p-8 text-center bg-slate-50 border border-dashed border-slate-300 rounded-xl text-slate-500 text-xs">
        Bu ders, sınıf ve dönem için tanımlı senaryo bulunmuyor. Aşağıdaki <strong>"➕ Yeni Senaryo Şablonu Ekle"</strong> butonuna tıklayarak hemen oluşturabilirsiniz.
      </div>
    `;
    return;
  }

  scenarios.forEach((sc, sIdx) => {
    const items = sc.items || [];
    const totalQ = items.reduce((acc, it) => acc + (parseInt(it.question_count, 10) || 0), 0);
    sc.total_questions = totalQ;

    const card = document.createElement("div");
    card.className = "bg-slate-50 border border-slate-200 rounded-xl p-4 shadow-sm space-y-3";

    const rowsHtml = items.map((it, iIdx) => {
      const currentUnitNo = parseInt(it.unit_no, 10) || 1;
      // Ders kitabı üniteleriyle eşleştirme seçenekleri
      const unitOptionsHtml = units.map((u, uIdx) => {
        const uNo = uIdx + 1;
        const cleanTitle = (u.name || "").replace(/^\d+\.\s*Ünite:\s*/i, "").trim();
        return `<option value="${uNo}" data-title="${cleanTitle}" ${uNo === currentUnitNo ? "selected" : ""}>${u.name}</option>`;
      }).join("");

      // Seçili ünitenin alt konularından hızlı aktarım seçenekleri
      const matchedUnitObj = units[currentUnitNo - 1] || units[0] || null;
      const quickTopicsHtml = (matchedUnitObj && Array.isArray(matchedUnitObj.topics))
        ? matchedUnitObj.topics.map(tp => `<option value="${tp}">${tp}</option>`).join("")
        : "";

      return `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-2 items-start bg-white p-2.5 rounded-lg border border-slate-200 shadow-xs">
          <!-- 1. İlişkili Ünite Seçimi -->
          <div class="md:col-span-3">
            <label class="block text-[9px] font-bold text-slate-500 uppercase mb-0.5">Ders Kitabı Ünitesi (Ünite No & Başlık)</label>
            <select onchange="onScenarioItemUnitSelect(${sIdx}, ${iIdx}, this)"
                    class="w-full text-[11px] p-1.5 bg-slate-50 border border-slate-300 rounded font-semibold text-slate-800 mb-1">
              ${unitOptionsHtml || `<option value="${currentUnitNo}">${currentUnitNo}. Ünite</option>`}
            </select>
            <input type="text" value="${it.unit_title || ""}"
                   placeholder="Ünite Başlığı"
                   onchange="updateScenarioItemField(${sIdx}, ${iIdx}, 'unit_title', this.value)"
                   class="w-full text-[10px] px-2 py-1 bg-white border border-slate-200 rounded text-slate-700"
                   title="Senaryoda görünecek ünite adı">
          </div>

          <!-- 2. Kazanım Kodu -->
          <div class="md:col-span-2">
            <label class="block text-[9px] font-bold text-slate-500 uppercase mb-0.5">Kazanım Kodu</label>
            <input type="text" value="${it.outcome_code || `${coursePrefix}.${grade}.1.${iIdx + 1}`}"
                   onchange="updateScenarioItemField(${sIdx}, ${iIdx}, 'outcome_code', this.value)"
                   class="w-full text-xs p-1.5 bg-indigo-50/60 border border-indigo-200 rounded font-mono font-bold text-indigo-950">
          </div>

          <!-- 3. Kazanım / Konu Açıklaması + Kitap Konularından Hızlı Seçim -->
          <div class="md:col-span-5">
            <div class="flex items-center justify-between mb-0.5">
              <label class="text-[9px] font-bold text-slate-500 uppercase">Kazanım / Konu Açıklaması</label>
              ${quickTopicsHtml ? `
                <select onchange="onScenarioItemQuickTopicSelect(${sIdx}, ${iIdx}, this.value); this.selectedIndex = 0;"
                        class="text-[9px] bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 rounded px-1 py-0.2 font-semibold cursor-pointer">
                  <option value="" disabled selected>📌 Ünite Konusundan Seç...</option>
                  ${quickTopicsHtml}
                </select>
              ` : ""}
            </div>
            <input type="text" value="${it.outcome_description || ""}"
                   placeholder="Kazanım veya konu açıklaması..."
                   onchange="updateScenarioItemField(${sIdx}, ${iIdx}, 'outcome_description', this.value)"
                   class="w-full text-xs p-1.5 bg-white border border-slate-300 rounded text-slate-800">
          </div>

          <!-- 4. Soru Adedi & Sil -->
          <div class="md:col-span-2 flex items-end justify-between gap-1.5 pt-3 md:pt-0">
            <div class="flex-1">
              <label class="block text-[9px] font-bold text-indigo-800 uppercase mb-0.5 text-center">Soru Adedi</label>
              <input type="number" min="1" max="20" value="${it.question_count || 1}"
                     onchange="updateScenarioItemField(${sIdx}, ${iIdx}, 'question_count', parseInt(this.value, 10) || 1)"
                     class="w-full text-xs p-1.5 text-center bg-indigo-50 border border-indigo-300 rounded font-extrabold text-indigo-950">
            </div>
            <button type="button" onclick="deleteItemFromScenario(${sIdx}, ${iIdx})"
                    class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded mb-0.5"
                    title="Bu kazanım satırını sil">
              🗑️
            </button>
          </div>
        </div>
      `;
    }).join("");

    card.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-slate-200">
        <div class="flex items-center gap-2 flex-1 min-w-[240px]">
          <span class="bg-indigo-900 text-white text-xs font-bold px-2.5 py-1 rounded-lg shadow-xs">
            #${sc.scenario_id || sIdx + 1}
          </span>
          <input type="text" value="${sc.name || `Senaryo ${sIdx + 1}`}"
                 onchange="updateScenarioName(${sIdx}, this.value)"
                 class="flex-1 text-sm font-bold text-slate-900 bg-white border border-slate-300 rounded-lg px-3 py-1 focus:ring-2 focus:ring-indigo-600"
                 placeholder="Senaryo Adı (Örn: Senaryo 1 (Allah İnancı))">
        </div>
        <div class="flex items-center gap-2">
          <span class="bg-indigo-100 text-indigo-900 border border-indigo-200 text-xs font-extrabold px-3 py-1 rounded-lg">
            Toplam Soru: ${totalQ}
          </span>
          <button type="button" onclick="addNewItemToScenario(${sIdx})"
                  class="px-2.5 py-1 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs flex items-center gap-1">
            <span>➕</span> Kazanım / Konu Satırı Ekle
          </button>
          <button type="button" onclick="deleteScenarioFromManager(${sIdx})"
                  class="p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg"
                  title="Bu Senaryoyu Sil">
            🗑️
          </button>
        </div>
      </div>

      <div class="space-y-2">
        ${rowsHtml}
      </div>
    `;

    listEl.appendChild(card);
  });
}

function updateScenarioName(sIdx, val) {
  if (state.scenarioManager.scenarios[sIdx]) {
    state.scenarioManager.scenarios[sIdx].name = val.trim() || `Senaryo ${sIdx + 1}`;
  }
}

function updateScenarioItemField(sIdx, iIdx, field, val) {
  const sc = state.scenarioManager.scenarios[sIdx];
  if (sc && sc.items && sc.items[iIdx]) {
    sc.items[iIdx][field] = val;
    if (field === "question_count") {
      renderScenarioManagerUI();
    }
  }
}

function onScenarioItemUnitSelect(sIdx, iIdx, selectEl) {
  const sc = state.scenarioManager.scenarios[sIdx];
  if (!sc || !sc.items || !sc.items[iIdx]) return;
  const uNo = parseInt(selectEl.value, 10) || 1;
  const selectedOpt = selectEl.options[selectEl.selectedIndex];
  const cleanTitle = selectedOpt?.getAttribute("data-title") || `Ünite ${uNo}`;

  sc.items[iIdx].unit_no = uNo;
  sc.items[iIdx].unit_title = cleanTitle;
  renderScenarioManagerUI();
}

function onScenarioItemQuickTopicSelect(sIdx, iIdx, topicText) {
  const sc = state.scenarioManager.scenarios[sIdx];
  if (!sc || !sc.items || !sc.items[iIdx] || !topicText) return;
  sc.items[iIdx].outcome_description = `${topicText} konusunu açıklar ve yorumlar.`;
  renderScenarioManagerUI();
}

function addNewItemToScenario(sIdx) {
  const sc = state.scenarioManager.scenarios[sIdx];
  if (!sc) return;
  if (!sc.items) sc.items = [];
  const { subject, grade, units } = state.scenarioManager;
  const prefixMap = { dkab: "DKAB", siyer: "SIYER", kuran: "KURAN" };
  const prefix = prefixMap[subject] || "DKAB";
  const firstUnitTitle = units[0] ? (units[0].name || "").replace(/^\d+\.\s*Ünite:\s*/i, "").trim() : "1. Ünite";
  const nextIdx = sc.items.length + 1;

  sc.items.push({
    unit_no: 1,
    unit_title: firstUnitTitle,
    outcome_code: `${prefix}.${grade}.1.${nextIdx}`,
    outcome_description: "Yeni kazanım veya konu açıklaması giriniz.",
    question_count: 1
  });
  renderScenarioManagerUI();
}

function deleteItemFromScenario(sIdx, iIdx) {
  const sc = state.scenarioManager.scenarios[sIdx];
  if (sc && sc.items) {
    sc.items.splice(iIdx, 1);
    renderScenarioManagerUI();
  }
}

function addNewScenarioToManager() {
  const { subject, grade, scenarios, units } = state.scenarioManager;
  const prefixMap = { dkab: "DKAB", siyer: "SIYER", kuran: "KURAN" };
  const prefix = prefixMap[subject] || "DKAB";
  const newId = scenarios.length + 1;
  const firstUnitTitle = units[0] ? (units[0].name || "").replace(/^\d+\.\s*Ünite:\s*/i, "").trim() : "1. Ünite";

  scenarios.push({
    scenario_id: newId,
    name: `Senaryo ${newId} (${firstUnitTitle})`,
    total_questions: 6,
    items: [
      {
        unit_no: 1,
        unit_title: firstUnitTitle,
        outcome_code: `${prefix}.${grade}.1.1`,
        outcome_description: `${firstUnitTitle} ile ilgili temel kavramları açıklar.`,
        question_count: 3
      },
      {
        unit_no: 1,
        unit_title: firstUnitTitle,
        outcome_code: `${prefix}.${grade}.1.2`,
        outcome_description: `${firstUnitTitle} konusunu örneklerle analiz eder.`,
        question_count: 3
      }
    ]
  });
  renderScenarioManagerUI();
  showToast(`Senaryo ${newId} eklendi. Kazanım ve soru adetlerini düzenleyebilirsiniz.`, "info");
}

function deleteScenarioFromManager(sIdx) {
  if (confirm("Bu senaryo şablonunu silmek istediğinize emin misiniz?")) {
    state.scenarioManager.scenarios.splice(sIdx, 1);
    renderScenarioManagerUI();
  }
}

async function saveScenarioManagerChanges() {
  const { subject, grade, term, scenarios } = state.scenarioManager;
  setLoading(true, "MEB Senaryosu ve kazanım dağılımları kaydediliyor...");
  try {
    const res = await fetch("/api/scenarios/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject,
        grade,
        term,
        scenarios
      })
    });
    if (!res.ok) throw new Error("Senaryolar kaydedilemedi.");
    await loadScenarios();
    populateScenarioDropdown();
    closeScenarioModal();
    showToast("MEB Senaryosu ve soru dağılımları başarıyla güncellendi!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    setLoading(false);
  }
}

async function resetScenariosToDefault() {
  if (confirm("Tüm MEB senaryolarını verdiğiniz varsayılan Kocaeli/Darıca İHO şablonuna sıfırlamak istediğinize emin misiniz?")) {
    setLoading(true, "Varsayılan senaryo şablonuna sıfırlanıyor...");
    try {
      await fetch("/api/scenarios/reset", { method: "POST" });
      await loadScenarios();
      const { subject, grade, term } = state.scenarioManager;
      await loadScenarioManagerContext(subject, grade, term);
      populateScenarioDropdown();
      showToast("Varsayılan Kocaeli/Darıca İHO senaryo şablonuna dönüldü.", "info");
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
  document.getElementById("settingsGeminiModel").value = state.config.gemini_model || "gemini-3.8-flash";
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

  // Navigasyon (3 Ana Ekran: Sınav Hazırlama, Sınav Arşivi, Soru Bankası)
  document.getElementById("navExamMakerBtn")?.addEventListener("click", () => switchView("exam_maker"));
  document.getElementById("navExamArchiveBtn")?.addEventListener("click", () => switchView("exam_archive"));
  document.getElementById("navQuestionBankBtn")?.addEventListener("click", () => switchView("question_bank"));

  // Sınav Arşivi Arama ve Filtreleri
  document.getElementById("archiveSearchInput")?.addEventListener("input", debounce(renderExamArchiveScreen, 300));
  document.getElementById("archiveFilterGrade")?.addEventListener("change", renderExamArchiveScreen);
  document.getElementById("archiveFilterSubject")?.addEventListener("change", renderExamArchiveScreen);
  document.getElementById("archiveFilterTerm")?.addEventListener("change", renderExamArchiveScreen);
  document.getElementById("archiveFilterType")?.addEventListener("change", renderExamArchiveScreen);

  // Sınav Parametreleri
  document.getElementById("examTypeSelect")?.addEventListener("change", onExamTypeChange);
  document.getElementById("examSubject")?.addEventListener("change", onSubjectOrGradeChange);
  document.getElementById("examGrade")?.addEventListener("change", onSubjectOrGradeChange);
  document.getElementById("examTerm")?.addEventListener("change", populateScenarioDropdown);
  document.getElementById("examNo")?.addEventListener("change", updatePaperHeaderLive);
  document.getElementById("examScenario")?.addEventListener("change", onScenarioChange);
  document.getElementById("btnOpenScenarioManager")?.addEventListener("click", openScenarioManager);

  document.getElementById("btnGenerateExam")?.addEventListener("click", handleGenerateExam);
  document.getElementById("btnAddQuestion")?.addEventListener("click", addNewQuestion);

  // Düzen Değiştirme
  document.getElementById("btnLayout2Col")?.addEventListener("click", () => toggleLayout("2_column"));
  document.getElementById("btnLayout1Col")?.addEventListener("click", () => toggleLayout("1_column"));

  // Cevap Çizgileri Aç/Kapa
  const chkAnswerLines = document.getElementById("chkShowAnswerLines");
  if (chkAnswerLines) {
    chkAnswerLines.checked = (state.showAnswerLines !== false);
    chkAnswerLines.addEventListener("change", (e) => {
      state.showAnswerLines = e.target.checked;
      if (state.currentExam) {
        state.currentExam.show_answer_lines = state.showAnswerLines;
      }
      renderExamPages();
    });
  }

  // Başlıkta Senaryo Adı Aç/Kapa
  const chkScenarioHeader = document.getElementById("chkShowScenarioInHeader");
  if (chkScenarioHeader) {
    chkScenarioHeader.checked = (state.showScenarioInHeader !== false);
    chkScenarioHeader.addEventListener("change", (e) => {
      state.showScenarioInHeader = e.target.checked;
      if (state.currentExam) {
        state.currentExam.show_scenario_in_header = state.showScenarioInHeader;
      }
      renderExamPages();
    });
  }

  // Başlıkta BEP Sınavı İbaresi Aç/Kapa (Sadece BEP sınavlarında görünür)
  const chkBepHeader = document.getElementById("chkShowBepInHeader");
  if (chkBepHeader) {
    chkBepHeader.checked = (state.showBepInHeader !== false);
    chkBepHeader.addEventListener("change", (e) => {
      state.showBepInHeader = e.target.checked;
      if (!state.bepOptions) state.bepOptions = {};
      state.bepOptions.show_bep_header = state.showBepInHeader;
      if (state.currentExam) {
        state.currentExam.bep_options = {
          ...(state.currentExam.bep_options || {}),
          ...state.bepOptions,
          show_bep_header: state.showBepInHeader
        };
      }
      renderExamPages();
    });
  }

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
  document.getElementById("bankFilterOrigin")?.addEventListener("change", loadQuestionBank);
  document.getElementById("bankFilterUsage")?.addEventListener("change", loadQuestionBank);
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
