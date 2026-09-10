const OPTION_LABELS = ["A", "B", "C", "D"];

const setupView = document.getElementById("setup-view");
const loadingView = document.getElementById("loading-view");
const quizView = document.getElementById("quiz-view");
const resultsView = document.getElementById("results-view");

const setupForm = document.getElementById("setup-form");
const setupError = document.getElementById("setup-error");
const generateBtn = document.getElementById("generate-btn");

const quizTopicEl = document.getElementById("quiz-topic");
const quizLevelEl = document.getElementById("quiz-level");
const progressTextEl = document.getElementById("progress-text");
const questionListEl = document.getElementById("question-list");
const submitQuizBtn = document.getElementById("submit-quiz-btn");
const cancelBtn = document.getElementById("cancel-btn");

const scoreValueEl = document.getElementById("score-value");
const scorePercentEl = document.getElementById("score-percent");
const resultsListEl = document.getElementById("results-list");
const retryBtn = document.getElementById("retry-btn");

let currentQuiz = null;
const answers = new Map();

function showView(view) {
  for (const el of [setupView, loadingView, quizView, resultsView]) {
    el.hidden = el !== view;
  }
}

function updateProgress() {
  const total = currentQuiz.questions.length;
  const answered = answers.size;
  progressTextEl.textContent = `${answered} / ${total} answered`;
  submitQuizBtn.disabled = answered !== total;
}

function renderQuiz(quiz) {
  quizTopicEl.textContent = quiz.topic;
  quizLevelEl.textContent = quiz.level;

  questionListEl.innerHTML = "";
  answers.clear();

  for (const q of quiz.questions) {
    const li = document.createElement("li");
    li.className = "question-card";
    li.innerHTML = `
      <p class="question-card-title">
        <span class="question-number">Q${q.number}.</span>
        <span>${escapeHtml(q.question)}</span>
      </p>
      <div class="options" data-question="${q.number}">
        ${OPTION_LABELS.filter((label) => q.options[label])
          .map(
            (label) => `
              <label class="option" data-label="${label}">
                <input type="radio" name="q${q.number}" value="${label}" />
                <span>${label}. ${escapeHtml(q.options[label])}</span>
              </label>
            `
          )
          .join("")}
      </div>
    `;
    questionListEl.appendChild(li);
  }

  updateProgress();
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

questionListEl.addEventListener("change", (event) => {
  const input = event.target;
  if (input.tagName !== "INPUT") return;

  const questionNumber = Number(input.name.slice(1));
  answers.set(questionNumber, input.value);

  const group = input.closest(".options");
  group.querySelectorAll(".option").forEach((opt) => opt.classList.remove("selected"));
  input.closest(".option").classList.add("selected");

  updateProgress();
});

setupForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setupError.hidden = true;

  const topic = document.getElementById("topic").value.trim();
  const level = document.getElementById("level").value;

  if (!topic) {
    setupError.textContent = "Please enter a topic.";
    setupError.hidden = false;
    return;
  }

  generateBtn.disabled = true;
  showView(loadingView);

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, level }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong. Please try again.");
    }

    currentQuiz = data;
    renderQuiz(currentQuiz);
    showView(quizView);
  } catch (err) {
    setupError.textContent = err.message;
    setupError.hidden = false;
    showView(setupView);
  } finally {
    generateBtn.disabled = false;
  }
});

cancelBtn.addEventListener("click", () => {
  currentQuiz = null;
  showView(setupView);
});

submitQuizBtn.addEventListener("click", () => {
  if (!currentQuiz || answers.size !== currentQuiz.questions.length) return;
  renderResults();
  showView(resultsView);
});

retryBtn.addEventListener("click", () => {
  currentQuiz = null;
  answers.clear();
  setupForm.reset();
  showView(setupView);
});

function renderResults() {
  const total = currentQuiz.questions.length;
  let score = 0;

  resultsListEl.innerHTML = "";

  for (const q of currentQuiz.questions) {
    const selected = answers.get(q.number);
    const isCorrect = selected === q.answer;
    if (isCorrect) score += 1;

    const li = document.createElement("li");
    li.className = "question-card";
    li.innerHTML = `
      <p class="question-card-title">
        <span class="question-number">Q${q.number}.</span>
        <span>${escapeHtml(q.question)}</span>
        <span class="result-tag ${isCorrect ? "correct" : "incorrect"}">
          ${isCorrect ? "Correct" : "Incorrect"}
        </span>
      </p>
      <div class="options">
        ${OPTION_LABELS.filter((label) => q.options[label])
          .map((label) => {
            let cls = "option";
            if (label === q.answer) cls += " correct";
            else if (label === selected) cls += " incorrect";
            return `
              <label class="${cls}">
                <input type="radio" disabled ${label === selected ? "checked" : ""} />
                <span>${label}. ${escapeHtml(q.options[label])}</span>
              </label>
            `;
          })
          .join("")}
      </div>
      ${
        q.explanation
          ? `<p class="explanation"><strong>Explanation:</strong> ${escapeHtml(q.explanation)}</p>`
          : ""
      }
    `;
    resultsListEl.appendChild(li);
  }

  scoreValueEl.textContent = `${score} / ${total}`;
  scorePercentEl.textContent = `${Math.round((score / total) * 100)}% correct`;
}
