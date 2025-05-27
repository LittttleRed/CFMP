import type { RecursivePartial, IOptions } from "tsparticles-engine"

export const particles_config: RecursivePartial<IOptions> = {
  background: { color: { value: "#181c2f" } },
  fpsLimit: 60,
  interactivity: {
   events: {
    onClick: { enable: true, mode: [ "push"] }, // 丰富点击效果
    onHover: { enable: true, mode: ["bubble","repulse"] },
    resize: true
  },
  modes: {
    bubble: { distance: 180, duration: 2, opacity: 0.8, size: 10 },
    push: { quantity: 4 },
    repulse: { distance: 120, duration: 0.6 },
    attract: { distance: 200, duration: 0.4, factor: 5 }, // 新增吸引模式
     // 如支持可加
  }
  },
  particles: {
    color: {
      value: [
        "#ff6b81",
        "#feca57",
        "#48dbfb",
        "#1dd1a1",
        "#5f27cd",
        "#00d2d3"
      ]
    },
    links: {
      color: "#fff",
      distance: 120,
      enable: true,
      opacity: 0.18,
      width: 1.2
    },
    collisions: { enable: false },
    move: {
      direction: "none",
      enable: true,
      outMode: "out",
      random: true,
      speed: 2.2,
      straight: false
    },
    number: {
      density: { enable: true, area: 900 },
      value: 60
    },
    opacity: {
      value: { min: 0.3, max: 0.8 },
       animation: { enable: true, speed: 0.7, minimumValue: 0.2, sync: false } // 闪烁
    },
    shape: { type: "circle" },
    size: {
      value: { min: 2, max: 6 },
      animation: { enable: true, speed: 2, minimumValue: 2, sync: false }
    }
  },
  detectRetina: true
}