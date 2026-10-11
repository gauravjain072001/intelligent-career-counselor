const form = document.getElementById('careerForm');
const result = document.getElementById('result');
const roleResult = document.getElementById('roleResult');
const scoreResult = document.getElementById('scoreResult');
const roadmap = document.getElementById('roadmap');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    skills: document.getElementById('skills').value,
    interests: document.getElementById('interests').value,
    goals: document.getElementById('goals').value,
  };

  const response = await fetch('/api/career-plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  roleResult.textContent = `Recommended role: ${data.recommended_role}`;
  scoreResult.textContent = `Match score: ${data.score}`;
  roadmap.innerHTML = '';
  data.roadmap.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    roadmap.appendChild(li);
  });
  result.classList.remove('hidden');
});
