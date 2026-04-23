/* ============================================================
   Starfield canvas + image fallbacks
   ============================================================ */

function initStarfield() {
  const canvas = document.createElement('canvas');
  canvas.id = 'star-canvas';
  document.body.insertBefore(canvas, document.body.firstChild);

  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = document.body.scrollHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  /* Stars */
  const STAR_COUNT = 260;
  const stars = Array.from({ length: STAR_COUNT }, () => ({
    x:      Math.random(),
    y:      Math.random(),
    r:      Math.random() * 1.6 + 0.25,
    alpha:  Math.random() * 0.65 + 0.25,
    speed:  Math.random() * 0.006 + 0.0015,
    phase:  Math.random() * Math.PI * 2,
    hue:    Math.random() < 0.15 ? 220 : Math.random() < 0.08 ? 45 : 0,
  }));

  /* Constellation line groups (decorative, scattered across page) */
  const groups = Array.from({ length: 7 }, () => {
    const n = Math.floor(Math.random() * 4) + 3;
    return Array.from({ length: n }, () => ({ x: Math.random(), y: Math.random() }));
  });

  let tick = 0;

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    /* Constellation lines */
    groups.forEach(pts => {
      ctx.beginPath();
      ctx.strokeStyle = 'rgba(100, 149, 237, 0.1)';
      ctx.lineWidth = 0.6;
      pts.forEach((p, i) => {
        const px = p.x * canvas.width;
        const py = p.y * canvas.height;
        if (i === 0) ctx.moveTo(px, py);
        else         ctx.lineTo(px, py);
      });
      ctx.stroke();

      /* Small dot at each node */
      pts.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x * canvas.width, p.y * canvas.height, 1.2, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(180, 200, 255, 0.35)';
        ctx.fill();
      });
    });

    /* Stars */
    stars.forEach(s => {
      const a = s.alpha * (0.55 + 0.45 * Math.sin(tick * s.speed + s.phase));
      const px = s.x * canvas.width;
      const py = s.y * canvas.height;

      /* Core dot */
      ctx.beginPath();
      ctx.arc(px, py, s.r, 0, Math.PI * 2);
      if (s.hue === 45) {
        ctx.fillStyle = `rgba(255, 230, 140, ${a})`;
      } else if (s.hue === 220) {
        ctx.fillStyle = `rgba(180, 210, 255, ${a})`;
      } else {
        ctx.fillStyle = `rgba(255, 255, 255, ${a})`;
      }
      ctx.fill();

      /* Soft glow for larger stars */
      if (s.r > 1.1) {
        const gr = ctx.createRadialGradient(px, py, 0, px, py, s.r * 4);
        if (s.hue === 45) {
          gr.addColorStop(0, `rgba(255, 220, 100, ${a * 0.28})`);
        } else {
          gr.addColorStop(0, `rgba(160, 190, 255, ${a * 0.28})`);
        }
        gr.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.beginPath();
        ctx.arc(px, py, s.r * 4, 0, Math.PI * 2);
        ctx.fillStyle = gr;
        ctx.fill();
      }
    });

    tick++;
    requestAnimationFrame(draw);
  }

  draw();
}

/* ============================================================
   DOM ready
   ============================================================ */
$(document).ready(function () {
  initStarfield();

  /* Image fallbacks */
  $('.homeImg').on('error', function () {
    $(this).css('display', 'none');
  });

  $('.learnImg').on('error', function () {
    $(this).attr('alt', 'Image unavailable');
    $(this).css({ background: '#0c0c2a', height: '220px' });
  });

  $('.quizImg').on('error', function () {
    $(this).attr('alt', 'Image unavailable');
  });
});
