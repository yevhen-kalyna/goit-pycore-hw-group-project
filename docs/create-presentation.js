const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Icon imports
const {
  FaPython, FaTerminal, FaUsers, FaRobot, FaGithub,
  FaCheckCircle, FaCogs, FaRocket, FaLightbulb, FaCode,
  FaDatabase, FaShieldAlt, FaBolt, FaClipboardList,
  FaAddressBook, FaStickyNote, FaSearch, FaBirthdayCake
} = require("react-icons/fa");
const {
  HiChip, HiBeaker, HiTerminal
} = require("react-icons/hi");

// ═══════════════════════════════════════════════
// COLOR PALETTE — "Deep Ocean Tech"
// ═══════════════════════════════════════════════
const C = {
  darkBg: "0F172A",
  darkBg2: "1E293B",
  lightBg: "F8FAFC",
  lightBg2: "F1F5F9",
  primary: "0EA5E9",
  primaryDark: "0284C7",
  primaryLight: "38BDF8",
  cyan: "22D3EE",
  teal: "14B8A6",
  emerald: "10B981",
  textLight: "F1F5F9",
  textMuted: "B0BEC5",     // boosted contrast for readability
  textMutedLight: "64748B",  // muted text on light backgrounds
  textDark: "1E293B",
  textDark2: "334155",
  white: "FFFFFF",
  cardBg: "FFFFFF",
  cardBorder: "E2E8F0",
  orange: "F97316",
  yellow: "EAB308",
  purple: "8B5CF6",
  pink: "EC4899",
  green: "22C55E",
};

// ═══════════════════════════════════════════════
// ICON RENDERING
// ═══════════════════════════════════════════════
function renderIconSvg(IconComponent, color, size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// ═══════════════════════════════════════════════
// STYLE FACTORIES
// ═══════════════════════════════════════════════
const cardShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08
});

const subtleShadow = () => ({
  type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.06
});

// ═══════════════════════════════════════════════
// MAIN BUILD
// ═══════════════════════════════════════════════
async function buildPresentation() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "GoIT Team";
  pres.title = "CLI Personal Assistant — Pitch Deck";

  // Pre-render icons
  const icons = {
    python: await iconToBase64Png(FaPython, `#${C.primary}`, 256),
    terminal: await iconToBase64Png(FaTerminal, `#${C.cyan}`, 256),
    users: await iconToBase64Png(FaUsers, `#${C.primary}`, 256),
    robot: await iconToBase64Png(FaRobot, `#${C.cyan}`, 256),
    github: await iconToBase64Png(FaGithub, `#${C.textDark}`, 256),
    githubW: await iconToBase64Png(FaGithub, `#${C.textLight}`, 256),
    check: await iconToBase64Png(FaCheckCircle, `#${C.emerald}`, 256),
    cogs: await iconToBase64Png(FaCogs, `#${C.primary}`, 256),
    rocket: await iconToBase64Png(FaRocket, `#${C.orange}`, 256),
    lightbulb: await iconToBase64Png(FaLightbulb, `#${C.yellow}`, 256),
    code: await iconToBase64Png(FaCode, `#${C.primary}`, 256),
    database: await iconToBase64Png(FaDatabase, `#${C.teal}`, 256),
    shield: await iconToBase64Png(FaShieldAlt, `#${C.emerald}`, 256),
    bolt: await iconToBase64Png(FaBolt, `#${C.yellow}`, 256),
    clipboard: await iconToBase64Png(FaClipboardList, `#${C.primary}`, 256),
    addressBook: await iconToBase64Png(FaAddressBook, `#${C.primary}`, 256),
    note: await iconToBase64Png(FaStickyNote, `#${C.yellow}`, 256),
    search: await iconToBase64Png(FaSearch, `#${C.cyan}`, 256),
    birthday: await iconToBase64Png(FaBirthdayCake, `#${C.pink}`, 256),
    chip: await iconToBase64Png(HiChip, `#${C.purple}`, 256),
    beaker: await iconToBase64Png(HiBeaker, `#${C.teal}`, 256),
    terminalHi: await iconToBase64Png(HiTerminal, `#${C.cyan}`, 256),
    // White versions for dark backgrounds
    pythonW: await iconToBase64Png(FaPython, `#${C.white}`, 256),
    terminalW: await iconToBase64Png(FaTerminal, `#${C.white}`, 256),
    rocketW: await iconToBase64Png(FaRocket, `#${C.white}`, 256),
    usersW: await iconToBase64Png(FaUsers, `#${C.textMuted}`, 256),
    checkW: await iconToBase64Png(FaCheckCircle, `#${C.cyan}`, 256),
    codeW: await iconToBase64Png(FaCode, `#${C.primaryLight}`, 256),
    robotW: await iconToBase64Png(FaRobot, `#${C.primaryLight}`, 256),
    boltW: await iconToBase64Png(FaBolt, `#${C.yellow}`, 256),
    lightbulbW: await iconToBase64Png(FaLightbulb, `#${C.yellow}`, 256),
  };

  // ═══════════════════════════════════════════
  // СЛАЙД 1: ТИТУЛЬНИЙ (темний)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.darkBg };

    // Декоративна лінія зверху
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.primary }
    });

    // Іконки
    slide.addImage({ data: icons.terminalW, x: 3.3, y: 0.8, w: 0.6, h: 0.6 });
    slide.addImage({ data: icons.pythonW, x: 6.1, y: 0.8, w: 0.6, h: 0.6 });

    // Назва
    slide.addText("CLI Personal Assistant", {
      x: 0.5, y: 1.5, w: 9, h: 1.0,
      fontSize: 42, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "center", margin: 0
    });

    // Підзаголовок
    slide.addText("Управління контактами та нотатками", {
      x: 0.5, y: 2.5, w: 9, h: 0.5,
      fontSize: 18, fontFace: "Calibri",
      color: C.primaryLight, align: "center", margin: 0
    });

    // Розділювач
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 3.5, y: 3.2, w: 3, h: 0.02,
      fill: { color: C.textMuted }
    });

    // Учасники команди
    slide.addText([
      { text: "Yevhen Kalyna", options: { bold: true, color: C.textLight, fontSize: 14 } },
      { text: "  \u2014  Team Lead", options: { color: C.textMuted, fontSize: 12 } },
    ], { x: 0.5, y: 3.5, w: 9, h: 0.4, fontFace: "Calibri", align: "center", margin: 0 });

    slide.addText([
      { text: "Mykola Nedotopa", options: { bold: true, color: C.textLight, fontSize: 14 } },
      { text: "  \u2014  Developer", options: { color: C.textMuted, fontSize: 12 } },
    ], { x: 0.5, y: 3.9, w: 9, h: 0.4, fontFace: "Calibri", align: "center", margin: 0 });

    slide.addText([
      { text: "IYgit", options: { bold: true, color: C.textLight, fontSize: 14 } },
      { text: "  \u2014  Developer", options: { color: C.textMuted, fontSize: 12 } },
    ], { x: 0.5, y: 4.3, w: 9, h: 0.4, fontFace: "Calibri", align: "center", margin: 0 });

    // Футер
    slide.addText("GoIT Python Core  |  2026", {
      x: 0.5, y: 5.1, w: 9, h: 0.3,
      fontSize: 10, fontFace: "Calibri",
      color: C.textMuted, align: "center", margin: 0
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 2: ОГЛЯД ПРОЄКТУ (світлий)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.lightBg };

    // Тег секції
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 0.4, w: 1.4, h: 0.35,
      fill: { color: C.primary }, rectRadius: 0.05
    });
    slide.addText("ОГЛЯД", {
      x: 0.5, y: 0.4, w: 1.4, h: 0.35,
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    // Заголовок
    slide.addText("Що ми створили", {
      x: 0.5, y: 0.95, w: 9, h: 0.6,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.textDark, margin: 0
    });

    // Опис
    slide.addText("Інтерактивний CLI-помічник для управління контактами та нотатками з валідацією, пошуком і збереженням даних", {
      x: 0.5, y: 1.55, w: 6.5, h: 0.5,
      fontSize: 13, fontFace: "Calibri",
      color: C.textDark2, margin: 0
    });

    // Картки функцій — сітка 2x2
    const features = [
      { icon: icons.addressBook, title: "Управління контактами", desc: "Додавання, редагування, пошук\nз валідацією телефону, email, адреси", color: C.primary },
      { icon: icons.note, title: "Нотатки з тегами", desc: "Створення нотаток з тегами,\nсортування та пошук за змістом", color: C.yellow },
      { icon: icons.birthday, title: "Дні народження", desc: "Відстеження днів народження\nзі зсувом на вихідних", color: C.pink },
      { icon: icons.database, title: "Збереження даних", desc: "Автоматичне збереження\nта завантаження даних", color: C.teal },
    ];

    const cardW = 4.1;
    const cardH = 1.2;
    const startX = 0.5;
    const startY = 2.2;
    const gapX = 0.4;
    const gapY = 0.3;

    features.forEach((f, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const x = startX + col * (cardW + gapX);
      const y = startY + row * (cardH + gapY);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: cardW, h: cardH,
        fill: { color: C.cardBg },
        shadow: cardShadow(),
        line: { color: C.cardBorder, width: 0.5 }
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 0.06, h: cardH,
        fill: { color: f.color }
      });

      slide.addImage({ data: f.icon, x: x + 0.25, y: y + 0.3, w: 0.45, h: 0.45 });

      slide.addText(f.title, {
        x: x + 0.85, y: y + 0.15, w: cardW - 1.1, h: 0.35,
        fontSize: 14, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0
      });

      slide.addText(f.desc, {
        x: x + 0.85, y: y + 0.5, w: cardW - 1.1, h: 0.7,
        fontSize: 11, fontFace: "Calibri",
        color: C.textDark2, margin: 0
      });
    });

    // Примітка внизу
    slide.addText("Чому CLI?  Швидкий, легкий, без GUI overhead \u2014 фокус на основах Python", {
      x: 0.5, y: 4.85, w: 9, h: 0.35,
      fontSize: 11, fontFace: "Calibri", italic: true,
      color: C.textMutedLight, margin: 0
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 3: ТЕХНОЛОГІЧНИЙ СТЕК (темний)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.darkBg };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.cyan }
    });

    slide.addText("Технологічний стек", {
      x: 0.5, y: 0.35, w: 9, h: 0.7,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.white, margin: 0
    });

    slide.addText("Нуль runtime залежностей \u2014 побудовано повністю на Python stdlib", {
      x: 0.5, y: 1.0, w: 9, h: 0.4,
      fontSize: 13, fontFace: "Calibri", italic: true,
      color: C.textLight, margin: 0
    });

    // Технології
    const techs = [
      { icon: icons.pythonW, label: "Python 3.12", desc: "Сучасний Python\nз типізацією", accent: C.primary },
      { icon: icons.terminalW, label: "Інтерактивний REPL", desc: "Зручний командний\nінтерфейс помічника", accent: C.cyan },
      { icon: icons.checkW, label: "Strict Typing", desc: "mypy з\ndisallow_untyped_defs", accent: C.emerald },
      { icon: icons.boltW, label: "TDD підхід", desc: "Тести першими,\nпотім реалізація", accent: C.yellow },
    ];

    const techCardW = 2.0;
    const techCardH = 2.4;
    const techStartX = 0.5;
    const techY = 1.7;
    const techGap = 0.4;

    techs.forEach((t, i) => {
      const x = techStartX + i * (techCardW + techGap);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: techY, w: techCardW, h: techCardH,
        fill: { color: C.darkBg2 },
        shadow: subtleShadow()
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: techY, w: techCardW, h: 0.04,
        fill: { color: t.accent }
      });

      slide.addImage({ data: t.icon, x: x + 0.7, y: techY + 0.35, w: 0.6, h: 0.6 });

      slide.addText(t.label, {
        x, y: techY + 1.1, w: techCardW, h: 0.4,
        fontSize: 14, fontFace: "Calibri", bold: true,
        color: C.white, align: "center", margin: 0
      });

      slide.addText(t.desc, {
        x: x + 0.15, y: techY + 1.5, w: techCardW - 0.3, h: 0.7,
        fontSize: 11, fontFace: "Calibri",
        color: C.textMuted, align: "center", margin: 0
      });
    });

    // Статистика внизу
    const stats = [
      { value: "0", label: "Runtime залежностей" },
      { value: "100%", label: "Покриття типами" },
      { value: "8", label: "Паралельних CI jobs" },
    ];

    stats.forEach((s, i) => {
      const x = 1.0 + i * 3.0;
      slide.addText(s.value, {
        x, y: 4.5, w: 2.0, h: 0.5,
        fontSize: 28, fontFace: "Trebuchet MS", bold: true,
        color: C.cyan, align: "center", margin: 0
      });
      slide.addText(s.label, {
        x, y: 4.95, w: 2.0, h: 0.3,
        fontSize: 10, fontFace: "Calibri",
        color: C.textMuted, align: "center", margin: 0
      });
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 4: AI В РОЗРОБЦІ (світлий)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.lightBg };

    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 0.4, w: 1.1, h: 0.35,
      fill: { color: C.purple }, rectRadius: 0.05
    });
    slide.addText("AI", {
      x: 0.5, y: 0.4, w: 1.1, h: 0.35,
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    slide.addText("AI-інструменти в розробці", {
      x: 0.5, y: 0.95, w: 9, h: 0.6,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.textDark, margin: 0
    });

    slide.addText("AI як інструмент прискорення розробки, а не заміна розуміння коду", {
      x: 0.5, y: 1.55, w: 9, h: 0.4,
      fontSize: 13, fontFace: "Calibri", italic: true,
      color: C.textDark2, margin: 0
    });

    // Дві великі картки
    const aiCards = [
      {
        icon: icons.robot,
        title: "Claude Code (CLI)",
        items: [
          "Локальний pair-programming",
          "Написання та рефакторинг коду",
          "Code review перед створенням PR",
          "Обговорення архітектури",
        ],
        color: C.primary
      },
      {
        icon: icons.github,
        title: "GitHub Copilot",
        items: [
          "Автоматичний PR reviewer",
          "Перевірка якості коду",
          "Пропозиції щодо стилю",
          "Інтегрований у CI workflow",
        ],
        color: C.purple
      },
    ];

    aiCards.forEach((card, i) => {
      const x = 0.5 + i * 4.7;
      const y = 2.2;
      const w = 4.3;
      const h = 2.7;

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w, h,
        fill: { color: C.cardBg },
        shadow: cardShadow(),
        line: { color: C.cardBorder, width: 0.5 }
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w, h: 0.05,
        fill: { color: card.color }
      });

      slide.addImage({ data: card.icon, x: x + 0.3, y: y + 0.3, w: 0.45, h: 0.45 });

      slide.addText(card.title, {
        x: x + 0.9, y: y + 0.3, w: w - 1.2, h: 0.45,
        fontSize: 18, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0, valign: "middle"
      });

      const itemsText = card.items.map((item, idx) => ({
        text: item,
        options: {
          bullet: true,
          breakLine: idx < card.items.length - 1,
          fontSize: 13,
          color: C.textDark2,
          paraSpaceAfter: 6,
        }
      }));

      slide.addText(itemsText, {
        x: x + 0.3, y: y + 0.95, w: w - 0.6, h: 1.5,
        fontFace: "Calibri", margin: 0
      });
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 4.85, w: 9, h: 0.01,
      fill: { color: C.cardBorder }
    });
    slide.addText("Обидва інструменти доповнюють один одного: Claude для глибокої локальної роботи, Copilot для автоматичного рев\u2019ю PR", {
      x: 0.5, y: 4.95, w: 9, h: 0.3,
      fontSize: 11, fontFace: "Calibri", italic: true,
      color: C.textMutedLight, align: "center", margin: 0
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 5: АРХІТЕКТУРА (світлий)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.lightBg };

    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 0.4, w: 2.2, h: 0.35,
      fill: { color: C.teal }, rectRadius: 0.05
    });
    slide.addText("\u0410\u0420\u0425\u0406\u0422\u0415\u041A\u0422\u0423\u0420\u0410", {
      x: 0.5, y: 0.4, w: 2.2, h: 0.35,
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    slide.addText("Архітектура коду", {
      x: 0.5, y: 0.95, w: 9, h: 0.6,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.textDark, margin: 0
    });

    const leftX = 0.5;
    const rightX = 5.2;
    const colW = 4.3;

    // Ліва картка — Моделі
    slide.addShape(pres.shapes.RECTANGLE, {
      x: leftX, y: 1.75, w: colW, h: 3.3,
      fill: { color: C.cardBg },
      shadow: cardShadow(),
      line: { color: C.cardBorder, width: 0.5 }
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: leftX, y: 1.75, w: colW, h: 0.05,
      fill: { color: C.primary }
    });

    slide.addImage({ data: icons.code, x: leftX + 0.25, y: 1.95, w: 0.35, h: 0.35 });
    slide.addText("\u0406\u0454\u0440\u0430\u0440\u0445\u0456\u044f \u043c\u043e\u0434\u0435\u043b\u0435\u0439", {
      x: leftX + 0.7, y: 1.95, w: colW - 1, h: 0.35,
      fontSize: 16, fontFace: "Calibri", bold: true,
      color: C.textDark, margin: 0, valign: "middle"
    });

    const hierarchy = [
      { text: "Field \u2192 Phone / Email / Birthday / Address", sub: "Ієрархія класів з валідацією значень", indent: 0 },
      { text: "Record", sub: "Контейнер для полів контакту", indent: 0 },
      { text: "AddressBook (UserDict)", sub: "Dict-like сховище контактів", indent: 0 },
      { text: "NoteBook (UserDict)", sub: "Dict-like сховище нотаток з UUID ключами", indent: 0 },
    ];

    let hierY = 2.5;
    hierarchy.forEach(h => {
      const xOff = h.indent * 0.35;
      slide.addText(h.text, {
        x: leftX + 0.3 + xOff, y: hierY, w: colW - 0.6 - xOff, h: 0.25,
        fontSize: 11, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0
      });
      slide.addText(h.sub, {
        x: leftX + 0.3 + xOff, y: hierY + 0.22, w: colW - 0.6 - xOff, h: 0.22,
        fontSize: 9, fontFace: "Calibri",
        color: C.textMutedLight, margin: 0
      });
      hierY += 0.5;
    });

    // Права картка — Патерни
    slide.addShape(pres.shapes.RECTANGLE, {
      x: rightX, y: 1.75, w: colW, h: 3.3,
      fill: { color: C.cardBg },
      shadow: cardShadow(),
      line: { color: C.cardBorder, width: 0.5 }
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: rightX, y: 1.75, w: colW, h: 0.05,
      fill: { color: C.teal }
    });

    slide.addImage({ data: icons.cogs, x: rightX + 0.25, y: 1.95, w: 0.35, h: 0.35 });
    slide.addText("\u041a\u043b\u044e\u0447\u043e\u0432\u0456 \u043f\u0430\u0442\u0435\u0440\u043d\u0438", {
      x: rightX + 0.7, y: 1.95, w: colW - 1, h: 0.35,
      fontSize: 16, fontFace: "Calibri", bold: true,
      color: C.textDark, margin: 0, valign: "middle"
    });

    const patterns = [
      { title: "@input_error decorator", desc: "Один декоратор обробляє 3 типи помилок" },
      { title: "UserDict inheritance", desc: "Dict-like інтерфейс з інкапсульованою логікою" },
      { title: "Signal handling", desc: "SIGTERM/SIGHUP graceful shutdown" },
      { title: "casefold() для Unicode", desc: "Коректна обробка edge cases (\u00df\u2192ss)" },
      { title: "UUID4 для нотаток", desc: "Глобально унікальні, collision-proof ID" },
    ];

    let patY = 2.5;
    patterns.forEach(p => {
      slide.addText(p.title, {
        x: rightX + 0.3, y: patY, w: colW - 0.6, h: 0.25,
        fontSize: 11, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0
      });
      slide.addText(p.desc, {
        x: rightX + 0.3, y: patY + 0.22, w: colW - 0.6, h: 0.22,
        fontSize: 9, fontFace: "Calibri",
        color: C.textMutedLight, margin: 0
      });
      patY += 0.5;
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 6: ТЕХНІЧНІ HIGHLIGHTS (темний)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.darkBg };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.emerald }
    });

    slide.addText("Технічні переваги", {
      x: 0.5, y: 0.35, w: 9, h: 0.7,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.white, margin: 0
    });

    const highlights = [
      { icon: icons.checkW, title: "TDD з Auto-Xfail", desc: "Тести першими; NotImplementedError \u2192 xfail, а не failure", accent: C.emerald },
      { icon: icons.boltW, title: "Нуль залежностей", desc: "100% Python stdlib \u2014 не потрібен pip install", accent: C.yellow },
      { icon: icons.codeW, title: "Strict mypy Typing", desc: "disallow_untyped_defs = true для кожної функції", accent: C.primary },
      { icon: icons.lightbulbW, title: "Signal Handling", desc: "SIGTERM/SIGHUP graceful shutdown зі збереженням даних", accent: C.orange },
      { icon: icons.robotW, title: "AI-Powered Workflow", desc: "Claude + Copilot для розробки та рев\u2019ю", accent: C.purple },
      { icon: icons.checkW, title: "8 Parallel CI Jobs", desc: "Кожен тестовий модуль працює в окремому CI job", accent: C.cyan },
    ];

    const hlCardW = 2.8;
    const hlCardH = 1.8;
    const hlStartX = 0.5;
    const hlStartY = 1.3;
    const hlGapX = 0.3;
    const hlGapY = 0.3;

    highlights.forEach((h, i) => {
      const col = i % 3;
      const row = Math.floor(i / 3);
      const x = hlStartX + col * (hlCardW + hlGapX);
      const y = hlStartY + row * (hlCardH + hlGapY);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: hlCardW, h: hlCardH,
        fill: { color: C.darkBg2 }
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: hlCardW, h: 0.04,
        fill: { color: h.accent }
      });

      slide.addImage({ data: h.icon, x: x + 0.2, y: y + 0.25, w: 0.4, h: 0.4 });

      slide.addText(h.title, {
        x: x + 0.15, y: y + 0.8, w: hlCardW - 0.3, h: 0.35,
        fontSize: 13, fontFace: "Calibri", bold: true,
        color: C.white, margin: 0
      });

      slide.addText(h.desc, {
        x: x + 0.15, y: y + 1.15, w: hlCardW - 0.3, h: 0.5,
        fontSize: 10, fontFace: "Calibri",
        color: C.textMuted, margin: 0
      });
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 7: CI/CD PIPELINE (світлий)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.lightBg };

    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 0.4, w: 1.3, h: 0.35,
      fill: { color: C.emerald }, rectRadius: 0.05
    });
    slide.addText("CI/CD", {
      x: 0.5, y: 0.4, w: 1.3, h: 0.35,
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    slide.addText("CI/CD Pipeline", {
      x: 0.5, y: 0.95, w: 9, h: 0.6,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.textDark, margin: 0
    });

    // Кроки пайплайну
    const steps = [
      { label: "Ruff\nЛінтинг", color: C.primary },
      { label: "mypy\nТипізація", color: C.teal },
      { label: "8 Parallel\nTest Jobs", color: C.emerald },
      { label: "Summary\nКоментар", color: C.purple },
    ];

    const stepW = 1.8;
    const stepH = 1.2;
    const stepY = 1.9;
    const stepStartX = 0.7;
    const arrowW = 0.5;

    steps.forEach((s, i) => {
      const x = stepStartX + i * (stepW + arrowW);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: stepY, w: stepW, h: stepH,
        fill: { color: C.cardBg },
        shadow: cardShadow(),
        line: { color: s.color, width: 1.5 }
      });

      slide.addText(s.label, {
        x, y: stepY, w: stepW, h: stepH,
        fontSize: 13, fontFace: "Calibri", bold: true,
        color: C.textDark, align: "center", valign: "middle", margin: 0
      });

      if (i < steps.length - 1) {
        slide.addText("\u2192", {
          x: x + stepW, y: stepY, w: arrowW, h: stepH,
          fontSize: 24, fontFace: "Calibri", bold: true,
          color: C.textDark2, align: "center", valign: "middle", margin: 0
        });
      }
    });

    // Деталі внизу
    const ciDetails = [
      { title: "Авто-коментарі до PR", desc: "CI генерує таблицю результатів тестів як коментар до кожного PR" },
      { title: "Copilot Auto-Review", desc: "GitHub Copilot налаштований як автоматичний рев\u2019ювер для кожного PR" },
      { title: "Squash Merge", desc: "Чиста git-історія зі squash merges з feature-гілок через develop у main" },
    ];

    ciDetails.forEach((d, i) => {
      const x = 0.5 + i * 3.15;
      const y = 3.5;
      const w = 2.85;

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w, h: 1.6,
        fill: { color: C.cardBg },
        shadow: subtleShadow(),
        line: { color: C.cardBorder, width: 0.5 }
      });

      slide.addText(d.title, {
        x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.35,
        fontSize: 12, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0
      });

      slide.addText(d.desc, {
        x: x + 0.2, y: y + 0.55, w: w - 0.4, h: 0.9,
        fontSize: 10, fontFace: "Calibri",
        color: C.textDark2, margin: 0
      });
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 8: LIVE DEMO (темний)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.darkBg };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.orange }
    });

    slide.addImage({ data: icons.terminalW, x: 4.35, y: 0.6, w: 1.3, h: 1.3 });

    slide.addText("Live Demo", {
      x: 0.5, y: 2.0, w: 9, h: 0.7,
      fontSize: 40, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "center", margin: 0
    });

    slide.addText("Познайомтесь з Джоном, фрілансером, якому потрібно відстежувати контакти клієнтів та нотатки зустрічей", {
      x: 1.5, y: 2.8, w: 7, h: 0.5,
      fontSize: 14, fontFace: "Calibri", italic: true,
      color: C.textMuted, align: "center", margin: 0
    });

    const demoSteps = [
      "Додати контакти з валідацією",
      "Дні народження та email",
      "Пошук та перегляд контактів",
      "Нотатки з тегами",
      "Збереження даних (exit/restart)",
    ];

    const stepsText = demoSteps.map((step, idx) => ({
      text: `${idx + 1}.  ${step}`,
      options: {
        breakLine: idx < demoSteps.length - 1,
        fontSize: 14,
        color: C.textLight,
        paraSpaceAfter: 8,
      }
    }));

    slide.addText(stepsText, {
      x: 2.5, y: 3.5, w: 5, h: 1.8,
      fontFace: "Calibri", margin: 0
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 9: ВИКЛИКИ ТА УРОКИ (світлий)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.lightBg };

    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 0.4, w: 1.6, h: 0.35,
      fill: { color: C.orange }, rectRadius: 0.05
    });
    slide.addText("УРОКИ", {
      x: 0.5, y: 0.4, w: 1.6, h: 0.35,
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", valign: "middle", margin: 0
    });

    slide.addText("Виклики та уроки", {
      x: 0.5, y: 0.95, w: 9, h: 0.6,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.textDark, margin: 0
    });

    const challenges = [
      { title: "TDD дисципліна", desc: "Писати тести перед кодом було складно спочатку, але це ловило баги рано", color: C.emerald },
      { title: "Birthday edge cases", desc: "29 лютого, зсув вихідних, rollover року \u2014 складна логіка валідації", color: C.pink },
      { title: "Multi-word аргументи", desc: "Парсинг \u2018add-address John Kyiv, Street 1\u2019 потребував спеціальної обробки", color: C.primary },
      { title: "CI Pipeline", desc: "8 паралельних jobs з auto-updating summary comment (без дублів)", color: C.purple },
      { title: "Командний Git Workflow", desc: "Feature branches, PR reviews, squash merges \u2014 командна робота через Git", color: C.teal },
      { title: "AI як інструмент", desc: "Ефективне використання Claude та Copilot без заміни розуміння коду", color: C.orange },
    ];

    const chCardW = 2.8;
    const chCardH = 1.35;
    const chStartX = 0.5;
    const chStartY = 1.8;
    const chGapX = 0.3;
    const chGapY = 0.25;

    challenges.forEach((ch, i) => {
      const col = i % 3;
      const row = Math.floor(i / 3);
      const x = chStartX + col * (chCardW + chGapX);
      const y = chStartY + row * (chCardH + chGapY);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: chCardW, h: chCardH,
        fill: { color: C.cardBg },
        shadow: subtleShadow(),
        line: { color: C.cardBorder, width: 0.5 }
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 0.05, h: chCardH,
        fill: { color: ch.color }
      });

      slide.addText(ch.title, {
        x: x + 0.25, y: y + 0.15, w: chCardW - 0.4, h: 0.35,
        fontSize: 13, fontFace: "Calibri", bold: true,
        color: C.textDark, margin: 0
      });

      slide.addText(ch.desc, {
        x: x + 0.25, y: y + 0.55, w: chCardW - 0.4, h: 0.7,
        fontSize: 10, fontFace: "Calibri",
        color: C.textDark2, margin: 0
      });
    });

    slide.addText("Головне: TDD, CI/CD та командна робота \u2014 навички, які переносяться у реальні проєкти", {
      x: 0.5, y: 4.85, w: 9, h: 0.35,
      fontSize: 11, fontFace: "Calibri", italic: true,
      color: C.textMutedLight, align: "center", margin: 0
    });
  }

  // ═══════════════════════════════════════════
  // СЛАЙД 10: МАЙБУТНЄ ТА ДЯКУЄМО (темний)
  // ═══════════════════════════════════════════
  {
    const slide = pres.addSlide();
    slide.background = { color: C.darkBg };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.primary }
    });

    slide.addText("Що далі?", {
      x: 0.5, y: 0.35, w: 9, h: 0.7,
      fontSize: 32, fontFace: "Trebuchet MS", bold: true,
      color: C.white, margin: 0
    });

    // Плани на майбутнє
    const plans = [
      { icon: icons.database, label: "Міграція на SQLite" },
      { icon: icons.search, label: "Export CSV/JSON" },
      { icon: icons.robot, label: "Telegram Bot" },
      { icon: icons.terminalHi, label: "Кольоровий вивід" },
    ];

    plans.forEach((p, i) => {
      const x = 0.8 + i * 2.25;
      const y = 1.3;

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 2.0, h: 1.3,
        fill: { color: C.darkBg2 }
      });

      slide.addImage({ data: p.icon, x: x + 0.7, y: y + 0.15, w: 0.5, h: 0.5 });

      slide.addText(p.label, {
        x: x + 0.1, y: y + 0.75, w: 1.8, h: 0.4,
        fontSize: 11, fontFace: "Calibri", bold: true,
        color: C.textLight, align: "center", margin: 0
      });
    });

    // Дякуємо
    slide.addText("Дякуємо!", {
      x: 0.5, y: 3.0, w: 9, h: 0.8,
      fontSize: 44, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "center", margin: 0
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 3.5, y: 3.9, w: 3, h: 0.02,
      fill: { color: C.textMuted }
    });

    slide.addText("Запитання?", {
      x: 0.5, y: 4.1, w: 9, h: 0.5,
      fontSize: 18, fontFace: "Calibri",
      color: C.cyan, align: "center", margin: 0
    });

    slide.addText("github.com/yevhen-kalyna/goit-pycore-hw-group-project", {
      x: 0.5, y: 4.8, w: 9, h: 0.35,
      fontSize: 13, fontFace: "Calibri",
      color: C.primaryLight, align: "center", margin: 0,
      hyperlink: { url: "https://github.com/yevhen-kalyna/goit-pycore-hw-group-project" }
    });
  }

  // ═══════════════════════════════════════════
  // ЗАПИС ФАЙЛУ
  // ═══════════════════════════════════════════
  await pres.writeFile({ fileName: "/Users/yevhen/Projects/goit-pycore-hw-group-project/pitch-deck.pptx" });
  console.log("Презентацію створено: pitch-deck.pptx");
}

buildPresentation().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
