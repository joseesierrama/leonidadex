(function () {
  "use strict";
  var root = document.getElementById("leonidaQuiz");
  if (!root) return;
  var sets = {
    regiones: [
      { q: "Neón, playas y gran ciudad. ¿Qué región de Leonida buscas?", a: ["Vice City", "Ambrosia", "Mount Kalaga"], correct: 0, note: "Vice City es la gran ciudad que Rockstar presenta en Leonida.", scene: "city" },
      { q: "¿Cómo se llama la región de pantanos de Leonida?", a: ["Leonida Keys", "Grassrivers", "Port Gellhorn"], correct: 1, note: "Grassrivers es la región de humedales y pantanos.", scene: "swamp" },
      { q: "¿Cuál de estas regiones es un parque nacional?", a: ["Ambrosia", "Port Gellhorn", "Mount Kalaga"], correct: 2, note: "Su nombre completo es Mount Kalaga National Park.", scene: "mountain" }
    ],
    personajes: [
      { q: "¿Quién pasó por el ejército antes de acabar en los Cayos?", a: ["Cal Hampton", "Jason Duval", "Boobie Ike"], correct: 1, note: "La ficha oficial de Jason menciona su paso por el ejército.", scene: "city" },
      { q: "¿Quién escucha las comunicaciones de los guardacostas?", a: ["Cal Hampton", "Raul Bautista", "Lucia Caminos"], correct: 0, note: "Es una de las aficiones de Cal descritas por Rockstar.", scene: "swamp" },
      { q: "Real Dimez es…", a: ["Un club", "Una emisora", "El dúo Bae-Luxe y Roxy"], correct: 2, note: "Rockstar presenta a Bae-Luxe y Roxy juntas como Real Dimez.", scene: "city" }
    ]
  };
  var mode = "regiones", index = 0, score = 0, answered = false, started = false;
  var question = document.getElementById("quizQuestion"), answers = document.getElementById("quizAnswers");
  var feedback = document.getElementById("quizFeedback"), next = document.getElementById("quizNext");
  function track(name, values) { if (typeof window.leonidaTrack === "function") window.leonidaTrack(name, values); }
  function draw() {
    var item = sets[mode][index];
    answered = false;
    document.getElementById("quizProgress").textContent = "Pregunta " + (index + 1) + " de 3 · " + score + (score === 1 ? " acierto" : " aciertos");
    root.dataset.scene = item.scene;
    question.textContent = item.q;
    answers.replaceChildren(); feedback.textContent = "Elige una respuesta. Sin límite de tiempo.";
    next.hidden = true;
    item.a.forEach(function (text, choice) {
      var button = document.createElement("button"); button.type = "button"; button.className = "quiz-answer";
      button.textContent = String.fromCharCode(65 + choice) + " · " + text;
      button.addEventListener("click", function () {
        if (answered) return;
        if (!started) { started = true; track("ld_quiz_start", { content_id: mode }); }
        answered = true;
        var correct = choice === item.correct;
        if (correct) score++;
        Array.prototype.forEach.call(answers.children, function (node, i) { node.disabled = true; if (i === item.correct) node.classList.add("correct"); });
        if (!correct) button.classList.add("incorrect");
        feedback.textContent = (correct ? "¡Correcto! " : "Esta se escapó. ") + item.note;
        document.getElementById("quizProgress").textContent = "Pregunta " + (index + 1) + " de 3 · " + score + (score === 1 ? " acierto" : " aciertos");
        next.hidden = false; next.textContent = index === 2 ? "Ver mi resultado" : "Siguiente pregunta";
      });
      answers.appendChild(button);
    });
  }
  next.addEventListener("click", function () {
    if (!answered) return;
    if (index < 2) { index++; draw(); question.focus(); return; }
    question.textContent = score + " de 3. " + (score === 3 ? "¡Te vienes de copiloto!" : "Hay otra vuelta por Leonida pendiente.");
    answers.replaceChildren(); next.hidden = true;
    feedback.textContent = "Prueba el otro reto o abre el mapa. Tus respuestas no se guardan en un perfil.";
    track("ld_quiz_complete", { content_id: mode, score: score });
    document.getElementById("quizResult").hidden = false;
    question.focus();
  });
  document.querySelectorAll("[data-quiz-mode]").forEach(function (button) {
    button.addEventListener("click", function () {
      mode = button.dataset.quizMode; index = 0; score = 0; started = false;
      document.querySelectorAll("[data-quiz-mode]").forEach(function (b) { b.setAttribute("aria-pressed", String(b === button)); });
      document.getElementById("quizResult").hidden = true; draw();
    });
  });
  document.getElementById("quizCopy").addEventListener("click", function () {
    var text = "He sacado " + score + "/3 en el reto de " + mode + " de LeonidaDex. ¿Me superas? https://leonidadex.net/retos/";
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { feedback.textContent = "Resultado copiado. Tú eliges dónde compartirlo."; }).catch(function () { feedback.textContent = text; });
    else feedback.textContent = text;
  });
  draw();
})();
