<template>
  <ScrollContainer @scroll="handleScroll">
    <div
      class="home-container"
      ref="containerRef"
      @mousemove="handleContainerMouseMove"
    >
      <!-- Parallax Background Elements -->
      <div class="parallax-bg" :style="parallaxStyle">
        <!-- Chaotic Orbit System -->
        <div class="orbit-system">
          <div class="orbit-path path-1"></div>
          <div class="orbit-path path-2"></div>
          <div class="orbit-path path-3"></div>

          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="orb orb-3"></div>
        </div>
        <div class="grid-overlay" :style="gridGlowStyle"></div>
      </div>

      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="studio-name">
            <span class="text-gradient">JuFireX</span>
            <span class="studio-suffix">Studio</span>
          </h1>
          <div class="slogan-container">
            <p class="slogan-main">
              {{ $t("app.home.slogan", "日月出矣，而爝火不息") }}
            </p>
            <div class="slogan-divider"></div>
            <p class="slogan-sub">Crafting Worlds, One Pixel at a Time</p>
          </div>
          <div class="scroll-indicator">
            <span>Scroll to Explore</span>
            <n-icon size="20">
              <font-awesome-icon icon="chevron-down" />
            </n-icon>
          </div>
        </div>
      </section>

      <!-- Philosophy Section -->
      <section class="philosophy-section">
        <div class="content-wrapper">
          <n-grid x-gap="24" cols="1 m:2" responsive="screen">
            <n-grid-item>
              <div class="philosophy-text">
                <h2 class="section-title">Philosophy</h2>
                <p class="philosophy-desc">
                  In an era where giants shine like the sun and moon,
                  <span class="highlight">JuFireX (爝火)</span> represents the
                  eternal flame of creativity. Small, yet persistent. We
                  dedicate ourselves to the pure art of game development,
                  bringing unique experiences to players who seek something
                  different.
                </p>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="philosophy-visual">
                <div class="flame-symbol-wrapper">
                  <div class="flame-symbol">
                    <div class="flame-core"></div>
                    <div class="flame-outer"></div>
                    <div class="flame-icon-overlay">
                      <font-awesome-icon icon="fire" />
                    </div>
                  </div>
                </div>
              </div>
            </n-grid-item>
          </n-grid>
        </div>
      </section>

      <!-- Showcase Section (Refactored Style) -->
      <section class="showcase-section">
        <h2 class="section-title text-center mb-5">Featured Works</h2>
        <div class="showcase-list">
          <div
            v-for="(game, index) in games"
            :key="index"
            class="showcase-item"
          >
            <div class="content-wrapper">
              <n-grid
                x-gap="48"
                y-gap="24"
                cols="1 m:2"
                responsive="screen"
                class="showcase-grid"
              >
                <!-- Text Column (Alternates) -->
                <n-grid-item
                  :class="{ 'order-last': index % 2 !== 0 }"
                  class="showcase-text-col"
                >
                  <div class="showcase-text-content">
                    <div class="showcase-header">
                      <span class="showcase-number">0{{ index + 1 }}</span>
                      <h3 class="game-title">{{ game.title }}</h3>
                    </div>
                    <p class="game-desc">{{ game.desc }}</p>
                    <div class="game-meta">
                      <div class="game-tags">
                        <span class="tag">RPG</span>
                        <span class="tag">Action</span>
                      </div>
                      <n-button text class="explore-link" color="#003aff">
                        Explore
                        <n-icon class="ms-2">
                          <font-awesome-icon icon="arrow-right" />
                        </n-icon>
                      </n-button>
                    </div>
                  </div>
                </n-grid-item>

                <!-- Visual Column (Alternates) -->
                <n-grid-item class="showcase-visual-col">
                  <div class="showcase-visual">
                    <div
                      class="visual-bg"
                      :style="{ backgroundImage: `url(${game.image})` }"
                    ></div>
                    <div class="visual-overlay"></div>
                    <div class="visual-content">
                      <n-icon size="60" color="rgba(255,255,255,0.9)">
                        <font-awesome-icon :icon="game.icon" />
                      </n-icon>
                    </div>
                  </div>
                </n-grid-item>
              </n-grid>
            </div>
            <!-- Divider between items, except last -->
            <div
              v-if="index !== games.length - 1"
              class="section-divider"
            ></div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="home-footer">
        <div class="footer-content">
          <div class="footer-logo">JuFireX</div>
          <div class="social-links">
            <a
              href="https://github.com/JuFireX"
              target="_blank"
              class="social-link"
            >
              <n-icon size="24"
                ><font-awesome-icon :icon="['fab', 'github']"
              /></n-icon>
            </a>
            <a href="#" class="social-link">
              <n-icon size="24"
                ><font-awesome-icon :icon="['fab', 'twitter']"
              /></n-icon>
            </a>
            <a href="#" class="social-link">
              <n-icon size="24"
                ><font-awesome-icon :icon="['fab', 'discord']"
              /></n-icon>
            </a>
          </div>
          <p class="copyright">© 2024 JuFireX Studio. All rights reserved.</p>
        </div>
      </footer>
    </div>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { NGrid, NGridItem, NIcon, NButton } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { ScrollContainer } from "@/components/scroll-container";

const containerRef = ref<HTMLElement | null>(null);
const scrollY = ref(0);
const mouseX = ref(0);
const mouseY = ref(0);

const handleScroll = (e: Event) => {
  const target = e.target as HTMLElement;
  scrollY.value = target.scrollTop;
};

const handleContainerMouseMove = (e: MouseEvent) => {
  // Use clientX/Y directly for viewport-relative coordinates
  // But for maskImage which is relative to the element, we need relative coordinates
  // Since container is full screen, clientX/Y works, but we need to account for scroll if mask is fixed
  // Actually, grid-overlay is absolute positioned in container.
  // container is inside ScrollContainer.
  // We need mouse position relative to the grid-overlay.

  if (containerRef.value) {
    const rect = containerRef.value.getBoundingClientRect();
    mouseX.value = e.clientX - rect.left;
    // Calculate relative Y inside the parallax container
    // The parallax background moves by scrollY * 0.8
    // rect.top accounts for standard scroll position (negative as we scroll down)
    // We need to map viewport Y to the coordinate system of the grid-overlay
    mouseY.value = e.clientY - rect.top - scrollY.value * 0.8;
  }
};

const parallaxStyle = computed(() => {
  return {
    transform: `translateY(${scrollY.value * 0.8}px)`,
  };
});

const gridGlowStyle = computed(() => {
  // Always show a faint grid (white 5%), plus a brighter glow (white 20%) around mouse
  // Use mask-image to control opacity: black = opaque (visible), transparent = invisible
  // Center (mouse) should be full opacity (visible), edges should be lower opacity
  return {
    maskImage: `radial-gradient(circle 400px at ${mouseX.value}px ${mouseY.value}px, black 20%, rgba(0,0,0,0.15) 80%)`,
    WebkitMaskImage: `radial-gradient(circle 400px at ${mouseX.value}px ${mouseY.value}px, black 20%, rgba(0,0,0,0.15) 80%)`,
  };
});

const games = [
  {
    title: "Genshin Impact (Placeholder)",
    desc: "An open-world action RPG. Step into Teyvat, a vast world teeming with life and flowing with elemental energy. Explore seven nations, meet a diverse cast of characters.",
    icon: "gamepad",
    image:
      "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1000&auto=format&fit=crop",
  },
  {
    title: "Honkai: Star Rail (Placeholder)",
    desc: "A HoYoverse space fantasy RPG. Hop aboard the Astral Express and experience the galaxy's infinite wonders filled with adventure and thrills.",
    icon: "rocket",
    image:
      "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=1000&auto=format&fit=crop",
  },
  {
    title: "Zenless Zone Zero (Placeholder)",
    desc: "A brand new urban fantasy action game. Live dual identities, two opposing personas. Behind the peaceful surface of the city lies another reality.",
    icon: "bolt",
    image:
      "https://images.unsplash.com/photo-1555680202-c86f0e12f086?q=80&w=1000&auto=format&fit=crop",
  },
  {
    title: "JuFireX Impact (Coming Soon)",
    desc: "Our flagship title. A journey through the stars to find the eternal flame. Experience a narrative-driven adventure that challenges your perception of reality.",
    icon: "fire",
    image:
      "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?q=80&w=1000&auto=format&fit=crop",
  },
];
</script>

<style scoped>
/* Variables */
.home-container {
  --brand-blue: #003aff;
  --brand-blue-dim: #0026a3;
  --accent-orange: #ff3d00;
  --bg-dark: #0a0a0a;
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.1);
  --grid-color: rgba(255, 255, 255, 0.15); /* White grid */

  /* Reset padding from parent if needed, but better to just fill */
  margin: -24px;
  min-height: 100vh;
  background-color: var(--bg-dark);
  color: var(--text-primary);
  overflow: hidden;
  position: relative;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
}

/* Parallax Background with Three-Body Chaos */
.parallax-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%; /* Cover full scrollable height */
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
  background-size: 60px 60px; /* Slightly larger grid */
  /* Opacity controlled by mask in script */
}

.orbit-system {
  position: absolute;
  top: 40vh; /* Fixed position relative to top, keeping it in Hero area */
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
}

.orb {
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.6;
  mix-blend-mode: screen;
}

.orb-1 {
  width: 400px;
  height: 400px;
  margin-top: -200px;
  margin-left: -200px;
  background: var(--brand-blue);
  animation: orbit-1 20s infinite linear;
}

.orb-2 {
  width: 300px;
  height: 300px;
  margin-top: -150px;
  margin-left: -150px;
  background: purple;
  animation: orbit-2 25s infinite linear;
}

.orb-3 {
  width: 200px;
  height: 200px;
  margin-top: -100px;
  margin-left: -100px;
  background: var(--accent-orange);
  animation: orbit-3 15s infinite linear;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1;
  text-align: center;
}

.studio-name {
  font-size: 5rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 1rem;
  letter-spacing: -2px;
}

.text-gradient {
  background: linear-gradient(135deg, #fff 0%, var(--brand-blue) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.studio-suffix {
  font-weight: 300;
  color: var(--text-secondary);
  margin-left: 1rem;
  font-size: 3rem;
}

.slogan-container {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.slogan-main {
  font-size: 1.5rem;
  letter-spacing: 4px;
  text-transform: uppercase;
  font-weight: 300;
}

.slogan-divider {
  width: 60px;
  height: 2px;
  background: var(--accent-orange);
}

.slogan-sub {
  font-size: 1rem;
  color: var(--text-secondary);
  font-family: "Maple Mono", monospace;
}

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
  animation: bounce 2s infinite;
}

/* Philosophy Section */
.philosophy-section {
  position: relative;
  padding: 150px 24px;
  z-index: 1;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(10, 10, 10, 0.9) 20%,
    rgba(10, 10, 10, 0.9) 80%,
    transparent 100%
  );
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 3rem;
  margin-bottom: 3rem;
  font-weight: 800;
  letter-spacing: -1px;
}

.philosophy-desc {
  font-size: 1.5rem;
  line-height: 1.8;
  color: var(--text-secondary);
  font-weight: 300;
}

.highlight {
  color: var(--accent-orange);
  font-weight: 600;
}

/* Flame Symbol Redesign */
.flame-symbol-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.flame-symbol {
  position: relative;
  width: 200px; /* Increased width */
  height: 250px; /* Increased height */
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.flame-symbol:hover .flame-icon-overlay {
  transform: translate(-50%, -50%) scale(1.05);
  color: rgba(255, 255, 255, 0.3);
  filter: drop-shadow(0 0 30px var(--accent-orange));
}

.flame-core {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 140px;
  background: radial-gradient(circle at bottom, #fff, var(--accent-orange));
  border-radius: 50% 50% 20% 20%;
  filter: blur(30px); /* Increased blur */
  animation: flame-pulse 2s infinite alternate;
  opacity: 0.9;
  z-index: 1;
}

.flame-outer {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 220px;
  background: linear-gradient(to top, var(--brand-blue), transparent);
  border-radius: 50% 50% 30% 30%;
  filter: blur(40px);
  opacity: 0.5;
  animation: flame-sway 3s infinite ease-in-out;
  z-index: 0;
}

.flame-icon-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 200px; /* Massive icon */
  color: rgba(255, 255, 255, 0.2); /* Very transparent */
  z-index: 10;
  transition: all 0.5s ease;
  filter: drop-shadow(0 0 10px rgba(0, 0, 0, 0.5)); /* Shadow to define shape */
  /* backdrop-filter: blur(2px); */ /* Optional glass effect */
}

/* Showcase Section (Refactored) */
.showcase-section {
  padding: 50px 0 100px 0;
  position: relative;
  z-index: 1;
  overflow: hidden;
  mask-image: linear-gradient(to bottom, transparent 0%, black 150px);
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 150px);
}

.showcase-list {
  display: flex;
  flex-direction: column;
  gap: 100px; /* Space between items */
}

.showcase-item {
  position: relative;
}

.showcase-grid {
  align-items: center;
}

/* Order utility for alternating layout */
.order-last {
  order: 2;
}

/* Text Column Styling */
.showcase-text-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 1rem;
}

.showcase-header {
  display: flex;
  align-items: baseline;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--glass-border);
  padding-bottom: 1rem;
}

.showcase-number {
  font-family: "Maple Mono", monospace;
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.1);
  font-weight: 700;
  line-height: 1;
}

.game-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
  line-height: 1.1;
  background: linear-gradient(to right, #fff, rgba(255, 255, 255, 0.5));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.game-desc {
  font-size: 1.2rem;
  line-height: 1.8;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  font-weight: 300;
}

.game-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-tags {
  display: flex;
  gap: 0.8rem;
}

.tag {
  padding: 4px 12px;
  border: 1px solid var(--glass-border);
  border-radius: 2px;
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: "Maple Mono", monospace;
  background: rgba(255, 255, 255, 0.03);
}

.explore-link {
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.5px;
}

/* Visual Column Styling */
.showcase-visual {
  position: relative;
  height: 400px;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  transition: transform 0.5s ease;
  /* group: hover; This won't work in CSS directly, but nice thought */
}

.showcase-item:hover .showcase-visual {
  transform: translateY(-5px);
}

.visual-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transition: transform 0.8s ease;
}

.showcase-item:hover .visual-bg {
  transform: scale(1.05);
}

.visual-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0, 0, 0, 0.6) 100%
  );
  mix-blend-mode: multiply;
}

.visual-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.4s ease;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
}

.showcase-item:hover .visual-content {
  opacity: 1;
}

.section-divider {
  height: 1px;
  width: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--glass-border) 50%,
    transparent 100%
  );
  margin-top: 50px; /* Half of gap */
  opacity: 0.5;
}

/* Responsive */
@media (max-width: 768px) {
  .studio-name {
    font-size: 3rem;
  }

  .studio-suffix {
    font-size: 1.5rem;
    display: block;
    margin-left: 0;
    margin-top: 0.5rem;
  }

  .order-last {
    order: unset; /* Stack normally on mobile */
  }

  .showcase-visual {
    height: 250px;
    margin-bottom: 2rem;
  }

  .showcase-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .game-title {
    font-size: 2rem;
  }
}

/* Footer */
.home-footer {
  padding: 4rem 24px;
  background: black;
  border-top: 1px solid var(--glass-border);
  position: relative;
  z-index: 1;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.footer-logo {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -1px;
}

.social-links {
  display: flex;
  gap: 2rem;
}

.social-link {
  color: var(--text-secondary);
  transition: color 0.3s;
}

.social-link:hover {
  color: var(--brand-blue);
}

.copyright {
  color: #666;
  font-size: 0.8rem;
}

/* Chaotic Orbit Animations */
@keyframes orbit-1 {
  0% {
    transform: rotate(0deg) translateX(150px) rotate(0deg);
  }
  100% {
    transform: rotate(360deg) translateX(150px) rotate(-360deg);
  }
}

@keyframes orbit-2 {
  0% {
    transform: rotate(120deg) translateX(250px) rotate(-120deg);
  }
  100% {
    transform: rotate(480deg) translateX(250px) rotate(-480deg);
  }
}

@keyframes orbit-3 {
  0% {
    transform: rotate(240deg) translateX(100px) rotate(-240deg);
  }
  100% {
    transform: rotate(600deg) translateX(100px) rotate(-600deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.2;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.3);
  }
}

@keyframes bounce {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-10px);
  }
  60% {
    transform: translateX(-50%) translateY(-5px);
  }
}

@keyframes flame-pulse {
  0% {
    transform: translateX(-50%) scale(1);
    opacity: 0.8;
  }
  100% {
    transform: translateX(-50%) scale(1.1);
    opacity: 1;
  }
}

@keyframes flame-sway {
  0% {
    transform: translateX(-50%) rotate(-5deg);
  }
  50% {
    transform: translateX(-50%) rotate(5deg);
  }
  100% {
    transform: translateX(-50%) rotate(-5deg);
  }
}

/* Old responsive block removed */
</style>
